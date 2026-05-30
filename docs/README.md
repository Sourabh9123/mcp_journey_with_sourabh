# MCP Course Index

Read these pages in order if you are new to MCP.

1. [Why MCP Exists](01-why-mcp.md)
2. [Architecture And Flow](02-architecture-and-flow.md)
3. [Resources, Tools, Prompts, Roots, Sampling](03-primitives.md)
4. [JSON-RPC And Lifecycle](04-json-rpc-and-lifecycle.md)
5. [Transports: stdio And Streamable HTTP](05-transports.md)
6. [Building An MCP Server](06-building-a-server.md)
7. [Design Guidelines](07-design-guidelines.md)
8. [Security And Trust](08-security.md)

The short version:

- MCP is the client-server protocol layer for model context and actions.
- The host talks to the LLM.
- The MCP client talks to MCP servers.
- The server exposes tools, resources, and prompts.
- The LLM can request tool use through the host, but it does not directly speak
  to the MCP server.

Use the [examples](../examples) after reading the lifecycle and transport pages.

