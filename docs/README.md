# MCP Course Index

Read these pages in order if you are new to MCP.

1. [Diagrams And Flows](00-diagrams-and-flows.md)
2. [Why MCP Exists](01-why-mcp.md)
3. [Architecture And Flow](02-architecture-and-flow.md)
4. [Resources, Tools, Prompts, Roots, Sampling](03-primitives.md)
5. [JSON-RPC And Lifecycle](04-json-rpc-and-lifecycle.md)
6. [Transports: stdio And Streamable HTTP](05-transports.md)
7. [Building An MCP Server](06-building-a-server.md)
8. [Design Guidelines](07-design-guidelines.md)
9. [Security And Trust](08-security.md)

The short version:

- MCP is the client-server protocol layer for model context and actions.
- The host talks to the LLM.
- The MCP client talks to MCP servers.
- The server exposes tools, resources, and prompts.
- The LLM can request tool use through the host, but it does not directly speak
  to the MCP server.

Use the [examples](../examples) after reading the lifecycle and transport pages.
