"""Tools available to the research agents.

Exposes the repo's existing local tools to LangChain (wrapping does not
change their behavior) and adds a web search tool. The search provider is
isolated behind the `web_search` function so it can be swapped (e.g. to
Tavily) without touching any agent code.
"""

from ddgs import DDGS
from langchain_core.tools import tool

from multiagent import tools as _local

local_tools = [
    tool(_local.calculate),
    tool(_local.get_current_time),
    tool(_local.text_stats),
    tool(_local.estimate_tokens),
    tool(_local.pick_random),
]


@tool
def web_search(query: str) -> str:
    """Search the web for current information on a topic.
    Use whenever you need facts, news, documentation, or sources beyond your training data.
    Returns titles, URLs, and snippets — always cite the URLs you use."""
    try:
        results = DDGS().text(query, max_results=5)
    except Exception as error:
        return f"Search failed: {error}"
    if not results:
        return "No results found for that query."
    return "\n\n".join(
        f"{r.get('title', 'Untitled')}\n{r.get('href', '')}\n{r.get('body', '')}"
        for r in results
    )
