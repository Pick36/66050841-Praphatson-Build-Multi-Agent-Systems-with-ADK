import os
import logging
import google.cloud.logging

from callback_logging import log_query_to_model, log_model_response
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.agents import SequentialAgent, LoopAgent, ParallelAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.langchain_tool import LangchainTool
from google.adk.models import Gemini
from google.genai import types
from google.adk.tools import exit_loop

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper


# =========================
# SYSTEM SETUP
# =========================

cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

load_dotenv()

model_name = os.getenv("MODEL")
print(model_name)

RETRY_OPTIONS = types.HttpRetryOptions(initial_delay=1, attempts=6)

wiki_tool = LangchainTool(
    tool=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
)


# =========================
# TOOLS
# =========================

def append_to_state(tool_context: ToolContext, field: str, response: str):
    existing_state = tool_context.state.get(field, [])
    tool_context.state[field] = existing_state + [response]
    logging.info(f"[Added to {field}] {response}")
    return {"status": "success"}


def write_file(tool_context: ToolContext, directory: str, filename: str, content: str):
    target_path = os.path.join(directory, filename)
    os.makedirs(os.path.dirname(target_path), exist_ok=True)

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)

    return {"status": "success"}


# =========================
# INVESTIGATION AGENTS
# =========================

admirer = Agent(
    name="admirer",
    model=Gemini(model=model_name, retry_options=RETRY_OPTIONS),
    description="Research positive historical aspects",
    instruction="""
TOPIC: { TOPIC? }

You are the supporter side.

Search Wikipedia using:
- achievements
- legacy
- contributions

Save results into pos_data using append_to_state.
""",
    tools=[wiki_tool, append_to_state],
)

critic = Agent(
    name="critic",
    model=Gemini(model=model_name, retry_options=RETRY_OPTIONS),
    description="Research negative historical aspects",
    instruction="""
TOPIC: { TOPIC? }

You are the critic side.

Search Wikipedia using:
- controversy
- criticism
- failure

Save results into neg_data using append_to_state.
""",
    tools=[wiki_tool, append_to_state],
)


investigation_team = ParallelAgent(
    name="investigation_team",
    sub_agents=[admirer, critic],
)


# =========================
# JUDGE LOOP
# =========================

judge = Agent(
    name="judge",
    model=Gemini(model=model_name, retry_options=RETRY_OPTIONS),
    description="Check balance of evidence",
    instruction="""
POSITIVE DATA:
{ pos_data? }

NEGATIVE DATA:
{ neg_data? }

RULES:
- Each side must have at least 2 entries
- If not balanced → DO NOT exit loop
- If balanced → MUST call exit_loop tool
""",
    tools=[append_to_state, exit_loop],
)


trial_loop = LoopAgent(
    name="trial_loop",
    sub_agents=[investigation_team, judge],
    max_iterations=2,
)


# =========================
# FINAL VERDICT WRITER
# =========================

verdict_writer = Agent(
    name="verdict_writer",
    model=Gemini(model=model_name, retry_options=RETRY_OPTIONS),
    description="Write final neutral historical report",
    instruction="""
TOPIC: { TOPIC? }

POSITIVE:
{ pos_data? }

NEGATIVE:
{ neg_data? }

Create neutral balanced historical analysis.

Then save using write_file:
directory = historical_reports
filename = TOPIC.txt
content = report
""",
    tools=[write_file],
)


# =========================
# MAIN WORKFLOW
# =========================

historical_court = SequentialAgent(
    name="historical_court",
    sub_agents=[
        trial_loop,
        verdict_writer
    ],
)


# =========================
# ROOT AGENT
# =========================

root_agent = Agent(
    name="historical_court_entry",
    model=Gemini(model=model_name, retry_options=RETRY_OPTIONS),
    description="Start historical court analysis",
    instruction="""
Ask user for historical person or event.

Store into TOPIC using append_to_state.

Then transfer to historical_court.
""",
    tools=[append_to_state],
    sub_agents=[historical_court],
)