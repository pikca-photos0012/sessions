from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams
 
 
mcp_toolset=MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="http://localhost:8080/mcp"
    ),
    tool_filter=["brave_web_search"]
)
 
root_agent=LlmAgent(
    name="smart_assistant",
    model="gemini-1.5-flash",
    instruction=""" Helpful assistant who repond cutomer query using mcp toolset
        """,
    tools=[mcp_toolset]
)
 