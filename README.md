#  Multi-Agent Historical Intelligence System
AI Multi-Agent System for Foreign Monarchy Historical Analysis
##  Project Overview

This project presents a Multi-Agent Artificial Intelligence System designed to analyze and generate historical knowledge related to foreign monarchies and global historical events.

The system applies modern AI agent orchestration concepts using a Parent Agent + Sub-Agent Architecture.
Each agent is responsible for specific cognitive tasks such as query understanding, historical data retrieval, and narrative generation.

This project demonstrates real-world applications of:

Multi-Agent Systems (MAS)

Distributed AI Reasoning

Tool-Augmented LLM Agents

Historical Knowledge Synthesis

###  Objectives

Develop a scalable AI Multi-Agent architecture

Demonstrate agent collaboration and workflow orchestration

Apply AI to historical domain knowledge

Build production-style AI system structure

Deploy using Google Cloud compatible environment

###  System Architecture
User Query
    ↓
Parent Agent (Coordinator / Planner)
    ↓
Sub Agent 1 — Historical Research Agent
    ↓
Sub Agent 2 — Report Generator Agent
    ↓
Final Historical Narrative Output

###  Agent Roles
###  Parent Agent

Responsible for:

Query interpretation

Task decomposition

Agent orchestration

Iteration control

###  Historical Research Sub-Agent

Responsible for:

Searching historical knowledge

Extracting key facts

Structuring historical timeline

###  Report Generator Sub-Agent

Responsible for:

Transforming data into readable narrative

Generating structured historical reports

Ensuring language quality

⚙ Technology Stack
Category	Technology
Language	Python 3.12
AI Framework	Google ADK
LLM Model	Gemini
Cloud	Google Cloud Platform
Logging	Google Cloud Logging
Environment	CloudShell / Local Python

###  Installation
#### 1️ Clone Repository
git clone <your-repo-url>
cd your-project

#### 2️ Install Dependencies
pip install -r requirements.txt

#### 3️ Setup Environment Variables

Create .env file inside agent folders:

GOOGLE_API_KEY=your_key_here
PROJECT_ID=your_project_id

▶ Running the System

Run Parent Agent:

python parent_and_subagents/agent.py


Run Workflow Agent:

python workflow_agents/agent.py

###  Agent Iteration Control

The system uses controlled agent iteration:

max_iterations = 3


This prevents infinite agent loops while maintaining reasoning depth.

###  Key AI Concepts Demonstrated

Multi-Agent Coordination

Tool-Augmented LLM Reasoning

Hierarchical Agent Control

AI Workflow Orchestration

Iterative Reasoning Loops

Prompt-Driven Task Execution

###  Example Query
Tell me about a foreign queen and her historical impact.

Output:

Historical background

Timeline events

Political impact

Historical legacy

###  Future Improvements

Add Vector Database Memory

Add Retrieval-Augmented Generation (RAG)

Add Web Search Tool Integration

Deploy as API Service

Add Frontend Dashboard

###  Research Value

This project demonstrates practical implementation of:

Distributed AI Systems

Autonomous Agent Collaboration

Knowledge-Oriented LLM Systems

AI Historical Reasoning Models

###  Author

Industrial Physics & IoT Engineering Student
AI Systems & Multi-Agent Architecture Research Focus

###  License

Educational / Research Use

###  Academic Contribution

This project can be extended into:

AI Senior Project

Multi-Agent Research Paper

Applied AI Thesis

Intelligent Knowledge System Prototype

