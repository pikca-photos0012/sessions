import os
import subprocess

# Set environment variables
os.environ["BRAVE_API_KEY"] = "BSA4xt2pMJU1b2EVRXflCjaKmx6Fly5"
os.environ["BRAVE_MCP_TRANSPORT"] = "http"
os.environ["BRAVE_MCP_HTTP_PORT"] = "9000"

# Run the Brave MCP server using npx with shell=True
subprocess.run("npx -y @brave/brave-search-mcp-server", shell=True)
