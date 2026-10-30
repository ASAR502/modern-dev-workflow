"""The supervisor graph: a supervisor agent routing to specialist agents."""

from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor

from .config import MODEL_NAME
from .tools import local_tools, web_search

RESEARCHER_PROMPT = (
    "You are the researcher on a research team. Gather current, factual information "
    "using the web_search tool — search multiple angles of the assigned topic. Use the "
    "local tools (calculate, get_current_time, text_stats, estimate_tokens, pick_random) "
    "whenever an exact value is needed instead of guessing. Report your findings as "
    "concise notes, always including the source URLs you used."
)

ANALYST_PROMPT = (
    "You are the analyst on a research team. You receive raw research notes from the "
    "researcher. Synthesize them: deduplicate, resolve contradictions, discard weak or "
    "unsourced claims, and extract the key facts and insights. Output a tight, organized "
    "analysis — not prose for the end user."
)

WRITER_PROMPT = (
    "You are the writer on a research team. You receive a synthesized analysis and turn "
    "it into the final report for the user: a short summary, the key findings as clear "
    "sections or bullets, and a sources list with URLs. Write in plain, readable language."
)

SUPERVISOR_PROMPT = (
    "You are the supervisor of a research team with three specialists: "
    "researcher (gathers information via web search), analyst (synthesizes raw findings), "
    "and writer (produces the final report). Delegate work to them to answer the user's "
    "request — typically researcher first, then analyst, then writer. Never answer "
    "research questions yourself. When the writer has produced the report, the task is done."
)


def build_graph():
    """Build and compile the supervisor graph with in-memory session history."""
    model = ChatOpenAI(model=MODEL_NAME)

    researcher = create_react_agent(
        model,
        tools=[web_search, *local_tools],
        name="researcher",
        prompt=RESEARCHER_PROMPT,
    )
    analyst = create_react_agent(
        model,
        tools=[],
        name="analyst",
        prompt=ANALYST_PROMPT,
    )
    writer = create_react_agent(
        model,
        tools=[],
        name="writer",
        prompt=WRITER_PROMPT,
    )

    supervisor = create_supervisor(
        agents=[researcher, analyst, writer],
        model=model,
        prompt=SUPERVISOR_PROMPT,
    )
    return supervisor.compile(checkpointer=InMemorySaver())
