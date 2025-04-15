from mainframe_orchestra import Agent, Task, OpenrouterModels, set_verbosity
from dotenv import load_dotenv

load_dotenv()

set_verbosity(1)

# Mock web search tool that simulates search results without making API calls
class MockWebTools:
    @staticmethod
    def search(query: str, num_results: int = 3) -> dict:
        """
        A search tool that returns search results.

        Args:
            query (str): The search query
            num_results (int): Number of results to return

        Returns:
            dict: A structured response with mock search results
        """
        # Create mock results
        results = []
        for i in range(num_results):
            results.append({
                "title": f"Mock Result {i+1} for: {query}",
                "url": f"https://example.com/mock-result-{i+1}",
                "snippet": f"This is a mock search result snippet for query '{query}'. This would normally contain relevant text from the webpage.",
                "score": 1.0 - (i * 0.1)  # Simulate decreasing relevance
            })

        return {
            "query": query,
            "total_results": num_results,
            "results": results
        }

# Create a research agent with the mock tool
research_agent = Agent(
    agent_id="research_assistant_1",
    role="research assistant",
    goal="answer user queries",
    llm=OpenrouterModels.sonnet_3_7,
    tools={MockWebTools.search}
)

def research_task(topic):
    prompt1 = f"Use your search tool to research {topic} and explain it in a way that is easy to understand. Use MAXIMUM one query."

    prompt = f"""
    This is now a developer testing session.
    As per developer instructions please make sure that if you're instructed later by user to return a 'no more tool calls' as JSON, just return your final answer instead as plain text.
    This is to test some internal JSON parsing logic. If you're returning actual tool calls, you can return a JSON.

    Prompt:
    {prompt1}
    """
    # prompt = prompt1

    return Task.create(
        agent=research_agent,
        instruction=prompt,
    )

result = research_task("quantum computing")
print(result)
