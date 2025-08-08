from google.adk.agents import LlmAgent, SequentialAgent
model = "gemini-2.0-flash"
 
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams
from dotenv import load_dotenv
import os
 
load_dotenv()
 
github_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {
                "GITHUB_TOKEN": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"),
                "GITHUB_USERNAME": os.getenv("GITHUB_USERNAME")
            }
        }
    )
)
 
# Step 1 – List repos and choose one
repo_selector = LlmAgent(
    name="repo_selector",
    model=model,
    instruction="""
You are a repository selector.
From the list of repos, pick the one specified by the user.
Return ONLY the repo name exactly (in the form owner/repo).
""",
    tools=[github_toolset],
    output_key="selected_repo"
)
 
# Step 2 – File Fetcher
file_reader = LlmAgent(
    name="file_reader",
    model=model,
    instruction="""
Use the GitHub MCP tool to list and read files from the selected repo.
Focus on `.py`, `.js`, and `.ts` files only.
Return file names and contents in JSON format.
""",
    tools=[github_toolset],
    output_key="repo_files"
)
 
# Step 3 – Bug Finder
bug_finder = LlmAgent(
    name="bug_finder",
    model=model,
    instruction="""
You are a static code analysis AI.
Scan the provided code for:
- Security risks (SQL injection, eval usage, etc.)
- TODO / FIXME comments
- Potential bugs
Output findings as a list of dictionaries:
[{"file": "...", "line": N, "issue": "..."}]
""",
    output_key="issues_found"
)
 
 
# Step 4 – Issue Creator
issue_creator = LlmAgent(
    name="issue_creator",
    model=model,
    instruction="""
For each issue found, create a GitHub issue in the selected repo.
Use 'create_issue' tool from GitHub MCP.
Format:
Title = short summary
Body = detailed description with file + line number.
""",
    tools=[github_toolset]
)
 
 
# ✅ Correct chaining
root_agent = SequentialAgent(
    name="bug_finder_bot",
    description="Selects repo → Reads files → Scans for issues → Creates GitHub issues",
    sub_agents=[repo_selector, file_reader, bug_finder, issue_creator]
)
 
 