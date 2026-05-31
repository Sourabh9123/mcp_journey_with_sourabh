# How To Read This Repository

This repository is meant to be read like a small course, not like random notes.
The best way to learn MCP is to move from the reason for the protocol, to the
architecture, to the wire messages, and only then to implementation.

## Recommended Sequence

### 1. Start With The Main Idea

Read:

- [README.md](README.md)
- [Diagrams And Flows](docs/00-diagrams-and-flows.md)
- [Why MCP Exists](docs/01-why-mcp.md)

Goal:

- Understand why MCP exists.
- Understand why MCP is more than wrapping an API function as a tool.
- Understand the problem MCP solves for many clients and many servers.
- See the full MCP flow visually before reading the detailed chapters.

Key sentence to remember:

> The LLM does not directly talk to an MCP server. The host uses an MCP client to
> talk to MCP servers.

### 2. Learn The Architecture

Read:

- [Architecture And Flow](docs/02-architecture-and-flow.md)

Goal:

- Understand the difference between host, LLM, MCP client, and MCP server.
- Understand the flow from user request to model reasoning to tool call.
- Understand that the host controls what is exposed and what is executed.

Do not skip this page. Most MCP confusion comes from mixing up these roles.

### 3. Learn The MCP Building Blocks

Read:

- [Resources, Tools, Prompts, Roots, Sampling, Elicitation](docs/03-primitives.md)

Goal:

- Know when to use a tool.
- Know when to use a resource.
- Know when to use a prompt.
- Understand why long documentation belongs in resources, not tool descriptions.

Simple rule:

| Need | Use |
| --- | --- |
| Perform an action | Tool |
| Read context | Resource |
| Reuse a workflow | Prompt |
| Share allowed project locations | Roots |
| Let a server ask the client for model help | Sampling |
| Ask the user for missing information | Elicitation |

### 4. Study The Wire Protocol

Read:

- [JSON-RPC And Lifecycle](docs/04-json-rpc-and-lifecycle.md)
- [Raw JSON-RPC transcript](examples/rpc-transcripts/basic-flow.md)

Goal:

- See what `initialize` looks like.
- See how the client lists tools, resources, and prompts.
- See how `tools/call` works.
- See the structure of success and error responses.

This is where MCP stops being abstract. You will see that MCP messages are just
structured JSON-RPC messages.

### 5. Learn The Transports

Read:

- [Transports: stdio And Streamable HTTP](docs/05-transports.md)

Goal:

- Understand why stdio is common for local development.
- Understand how JSON-RPC moves through stdin and stdout.
- Understand when Streamable HTTP is a better fit.
- Understand why stdout must contain only protocol messages in stdio servers.

### 6. Build The Mental Server

Read:

- [Building An MCP Server](docs/06-building-a-server.md)
- [Design Guidelines](docs/07-design-guidelines.md)

Goal:

- Learn how to decide which resources, tools, and prompts your server should expose.
- Learn how to design small, clear tools.
- Learn why precise JSON Schemas matter.
- Learn how to return useful structured results.

### 7. Run The Tiny Example

Read:

- [Minimal educational stdio server](examples/minimal-stdio-python/README.md)
- [server.py](examples/minimal-stdio-python/server.py)

Goal:

- See a simple stdin/stdout loop.
- Send one JSON-RPC message per line.
- Watch the server answer `initialize` and `tools/call`.

This example is intentionally small. It is useful for learning, but real MCP
servers should use an SDK.

### 8. Read Security Last, Then Again

Read:

- [Security And Trust](docs/08-security.md)

Goal:

- Understand that model output is not trusted.
- Understand prompt injection risk.
- Understand why hosts should confirm risky tool calls.
- Understand why servers must validate arguments and resource URIs.

After building your first server, read this page again.

## Fast Path

If you only have 30 minutes:

1. [README.md](README.md)
2. [Diagrams And Flows](docs/00-diagrams-and-flows.md)
3. [Architecture And Flow](docs/02-architecture-and-flow.md)
4. [Resources, Tools, Prompts, Roots, Sampling, Elicitation](docs/03-primitives.md)
5. [Raw JSON-RPC transcript](examples/rpc-transcripts/basic-flow.md)
6. [Transports: stdio And Streamable HTTP](docs/05-transports.md)

This gives you the core mental model quickly.

## Deep Path

If you want to learn properly:

1. Read every page in [docs/README.md](docs/README.md).
2. Read the [raw JSON-RPC transcript](examples/rpc-transcripts/basic-flow.md).
3. Run the [minimal stdio Python server](examples/minimal-stdio-python/README.md).
4. Design a fake MCP server on paper before coding:
   - list resources
   - list tools
   - list prompts
   - write input schemas
   - write example JSON-RPC messages
5. Compare your design with [Design Guidelines](docs/07-design-guidelines.md).
6. Check your design against [Security And Trust](docs/08-security.md).

## What To Focus On First

Focus on these ideas before SDK code:

- MCP is client-server, not model-server.
- The host mediates access.
- The MCP client discovers capabilities from the MCP server.
- Tools are actions.
- Resources are context.
- Prompts are reusable workflows.
- Elicitation lets a server ask the client for more user input.
- JSON-RPC is the message format.
- stdio is usually best for local learning.
- Streamable HTTP is usually best for remote servers.

## What Not To Do While Learning

Avoid these early mistakes:

- Do not put giant docs inside tool descriptions.
- Do not create one tool that does everything.
- Do not assume the MCP server sees the whole chat.
- Do not write normal logs to stdout in stdio servers.
- Do not trust tool arguments just because they came from a model.
- Do not start with a complex production server before understanding the message flow.

## Official References

Use this repository for plain-language learning. Use the official spec when you
need exact protocol details.

- Lifecycle: https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle
- Transports: https://modelcontextprotocol.io/specification/2025-11-25/basic/transports
- Tools: https://modelcontextprotocol.io/specification/2025-11-25/server/tools
- Resources: https://modelcontextprotocol.io/specification/2025-11-25/server/resources
- Prompts: https://modelcontextprotocol.io/specification/2025-11-25/server/prompts

## Suggested Reading Loop

Use this loop whenever a page feels abstract:

1. Read the explanation.
2. Find the matching JSON example.
3. Say which side sends it: client or server.
4. Say why it exists.
5. Say what can go wrong.

If you can explain those five things, you are learning MCP the right way.
