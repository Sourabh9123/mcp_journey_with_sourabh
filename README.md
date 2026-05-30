# MCP Learning Notes

This repository is a simple, detailed learning path for the Model Context Protocol
(MCP). It explains MCP in plain language first, then shows the actual JSON-RPC
messages that move between a client and server.

The important idea:

> The LLM does not directly talk to an MCP server. The host application talks to
> the LLM, an MCP client talks to MCP servers, and the host decides what context
> and tool results are given back to the model.

MCP is not only "wrap this API as a function". It is a protocol for discovering
tools, resources, prompts, capabilities, transports, and result formats in a
standard way so many clients and many servers can work together.

## Learning Path

Start here:

- [Docs course index](docs/README.md)
- [Examples index](examples/README.md)

Core chapters:

1. [Why MCP Exists](docs/01-why-mcp.md)
2. [Architecture And Flow](docs/02-architecture-and-flow.md)
3. [Resources, Tools, Prompts, Roots, Sampling](docs/03-primitives.md)
4. [JSON-RPC And Lifecycle](docs/04-json-rpc-and-lifecycle.md)
5. [Transports: stdio And Streamable HTTP](docs/05-transports.md)
6. [Building An MCP Server](docs/06-building-a-server.md)
7. [Design Guidelines](docs/07-design-guidelines.md)
8. [Security And Trust](docs/08-security.md)

Examples:

- [Raw JSON-RPC transcript](examples/rpc-transcripts/basic-flow.md)
- [Minimal educational stdio server](examples/minimal-stdio-python/README.md)

## What MCP Gives You

MCP gives an AI application a common way to ask external servers:

- What tools can you call?
- What resources can you read?
- What prompt templates can a user choose?
- What input schema does each tool need?
- What result format should the client expect?
- What protocol version and optional features do you support?
- How do we communicate: local stdio, remote HTTP, or another transport?

Without MCP, every integration becomes a custom plugin shape. With MCP, the
same client can connect to a filesystem server, database server, browser server,
Git server, internal API server, or documentation server using one protocol.

## The Core Roles

| Role | What it does |
| --- | --- |
| Host | The AI app the user interacts with, such as an IDE, desktop assistant, or chat app. |
| LLM | The language model that reasons over the user request and available context. |
| MCP client | The protocol component inside the host that connects to MCP servers. |
| MCP server | A separate process or service that exposes tools, resources, and prompts. |

The model may decide that a tool should be called, but the client performs the
actual protocol call. The server receives protocol messages from the client, not
free-form private conversation with the model.

## Good MCP Design In One Page

- Use **tools** for actions: search, create, update, run, query, send.
- Use **resources** for context: docs, files, schemas, records, examples.
- Use **prompts** for reusable user-selected workflows.
- Keep tool descriptions short and clear.
- Do not put huge documentation inside tool docstrings. Put detailed reference
  material in resources, then expose a tool that acts on specific inputs.
- Give every tool a precise JSON Schema.
- Return structured content when the caller needs machine-readable results.
- Treat tool execution as untrusted input and output until validated.
- Ask for human confirmation before risky or irreversible operations.

## Current Spec Notes

These notes follow the official MCP specification pages for the latest published
version shown there at the time of writing, `2025-11-25`. Older clients and
servers may still use earlier protocol versions, so version negotiation matters.

Official references:

- https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle
- https://modelcontextprotocol.io/specification/2025-11-25/basic/transports
- https://modelcontextprotocol.io/specification/2025-11-25/server/tools
- https://modelcontextprotocol.io/specification/2025-11-25/server/resources
- https://modelcontextprotocol.io/specification/2025-11-25/server/prompts
