import os
import logging
from datetime import datetime
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.agents import SequentialAgent, ParallelAgent, LoopAgent
from google.adk.models import Gemini
from google.genai import types

from google.adk.tools.tool_context import ToolContext
from google.adk.tools import exit_loop
from google.adk.tools.langchain_tool import LangchainTool

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper


# =========================
# SYSTEM SETUP
# =========================

logging.basicConfig(level=logging.INFO)
load_dotenv()

MODEL = os.getenv("MODEL", "gemini-1.5-pro")
RETRY = types.HttpRetryOptions(initial_delay=1, attempts=6)

wiki_api = WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=4000)
wiki_tool = LangchainTool(tool=WikipediaQueryRun(api_wrapper=wiki_api))


# =========================
# TOOLS
# =========================

def save_state(tool_context: ToolContext, key: str, text: str):
    existing = tool_context.state.get(key, [])
    if not isinstance(existing, list):
        existing = []

    timestamp = datetime.now().strftime("%H:%M")
    existing.append(f"[{timestamp}] {text}")

    tool_context.state[key] = existing
    return {"status": "ok"}


def add_search_query(tool_context: ToolContext, bucket: str, query: str):
    q = tool_context.state.get(bucket, [])
    if not isinstance(q, list):
        q = []

    q.append(query)
    tool_context.state[bucket] = q
    return {"status": "ok"}


def get_last_query(tool_context: ToolContext, bucket: str):
    q = tool_context.state.get(bucket, [])
    if isinstance(q, list) and q:
        return {"query": q[-1]}
    return {"query": tool_context.state.get("topic", "")}


def write_report(tool_context: ToolContext, report_text: str):
    folder = "council_reports"
    os.makedirs(folder, exist_ok=True)

    topic = tool_context.state.get("topic", "history")
    clean_topic = "".join(c for c in topic if c.isalnum() or c in " _-")

    filename = f"{clean_topic}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    path = os.path.join(folder, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(report_text)

    return {"status": "saved", "file": path}


# =========================
# AGENTS
# =========================

archivist = Agent(
    name="archivist",
    model=Gemini(model=MODEL, retry_options=RETRY),
    instruction="""
You are the Historical Archivist.

Ask the user which historical leader or event should be investigated.

Store into state key 'topic'.
Also generate starter search queries:
positive_queries
negative_queries
""",
    tools=[save_state],
)


legacy_analyst = Agent(
    name="legacy_analyst",
    model=Gemini(model=MODEL, retry_options=RETRY),
    instruction="""
Topic: {topic?}

1. Get latest query from positive_queries
2. Search Wikipedia
3. Extract achievements, legacy, positive influence
4. Save into positive_evidence
""",
    tools=[get_last_query, wiki_tool, save_state],
)


controversy_analyst = Agent(
    name="controversy_analyst",
    model=Gemini(model=MODEL, retry_options=RETRY),
    instruction="""
Topic: {topic?}

1. Get latest query from negative_queries
2. Search Wikipedia
3. Extract controversies, criticism, negative effects
4. Save into negative_evidence
""",
    tools=[get_last_query, wiki_tool, save_state],
)


balance_examiner = Agent(
    name="balance_examiner",
    model=Gemini(model=MODEL, retry_options=RETRY),
    instruction="""
Check positive_evidence and negative_evidence.

If either side < 2 entries:
Add new search query using add_search_query.
DO NOT exit loop.

If balanced:
Use exit_loop tool.
""",
    tools=[add_search_query, save_state, exit_loop],
)


chronicle_writer = Agent(
    name="chronicle_writer",
    model=Gemini(model=MODEL, retry_options=RETRY),
    instruction="""
Create a neutral historical analysis report using:

topic
positive_evidence
negative_evidence

Then save using write_report tool.
""",
    tools=[write_report],
)


# =========================
# WORKFLOW
# =========================

research_parallel = ParallelAgent(
    name="research_parallel",
    sub_agents=[legacy_analyst, controversy_analyst],
)

review_loop = LoopAgent(
    name="review_loop",
    sub_agents=[research_parallel, balance_examiner],
    max_iterations=5,
)

history_pipeline = SequentialAgent(
    name="history_pipeline",
    sub_agents=[review_loop, chronicle_writer],
)


root_agent = Agent(
    name="entry_agent",
    model=Gemini(model=MODEL, retry_options=RETRY),
    instruction="""
Start investigation session.
Ask user for historical topic.
Then send to history_pipeline.
""",
    sub_agents=[history_pipeline],
)


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    print("Historical Council System Ready")

    topic_input = input("Enter historical topic: ")

    initial_state = {
        "topic": topic_input,
        "positive_queries": [f"{topic_input} achievements", f"{topic_input} legacy"],
        "negative_queries": [f"{topic_input} controversy", f"{topic_input} criticism"],
        "positive_evidence": [],
        "negative_evidence": [],
    }

    root_agent.run(input=topic_input, state=initial_state)

    print("Report generated.")