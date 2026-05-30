# Why MCP Exists

MCP stands for Model Context Protocol. It is a standard way for AI applications
to connect models with external context and actions.

At first MCP can look unnecessary. You might ask:

> Why not just wrap my API function as a tool and give it to the LLM?

For a small demo, that is often enough. If you own the model call, own the app,
own the API, and only have one or two functions, a direct tool wrapper can be
fine.

MCP becomes useful when integrations need to be reusable, discoverable, safer,
and independent from one specific app or model provider.

## The Problem Without MCP

Imagine five AI apps and ten useful systems:

- local files
- GitHub
- Postgres
- Slack
- Google Drive
- browser automation
- internal company APIs
- documentation search
- ticketing systems
- deployment tools

Without a shared protocol, each AI app needs custom integration code for each
system. Each integration invents its own way to describe tools, pass arguments,
return errors, load documentation, ask for permissions, stream progress, and
handle auth.

That creates repeated work:

- Every app needs its own plugin format.
- Every server needs custom adapters for every app.
- Tool descriptions become inconsistent.
- Long docs get stuffed into function descriptions.
- The model sees actions but not enough reliable context.
- Security and permissions are handled differently everywhere.

MCP tries to make this boring in a good way. One server can expose its abilities
once, and many MCP clients can understand it.

## What MCP Standardizes

MCP standardizes the conversation between an MCP client and MCP server:

- Initialization and protocol version negotiation.
- Capability negotiation: which features each side supports.
- Listing and calling tools.
- Listing and reading resources.
- Listing and getting prompt templates.
- Notifications when lists or resources change.
- Transport rules for local and remote communication.
- JSON-RPC request, response, notification, and error structure.

The protocol does not decide how your user interface must look. It also does not
force one model provider. It defines the client-server layer below the AI app.

## Why A Protocol Is Better Than A Function List

A function list tells the model, "Here are some functions you may call."

MCP tells the host application:

- How to discover the function list from an external server.
- How to describe each function with a schema.
- How to discover resources separately from actions.
- How to expose reusable prompt templates.
- How to negotiate optional features.
- How to transport messages over stdio or HTTP.
- How to keep the server separate from the model provider.

That separation matters. Your database MCP server does not need to know whether
the host uses Claude, GPT, Gemini, a local model, or a future model. It speaks
MCP to the client.

## When A Direct Tool Wrapper Is Enough

Use a direct tool wrapper when:

- You are building a small single-app prototype.
- The tool only exists for one model call path.
- There is no need for external discovery.
- You do not need resources or prompt templates.
- You control both the host and the API.

This is like writing one adapter directly into your app.

## When MCP Is Worth It

Use MCP when:

- You want one integration to work in multiple MCP-capable clients.
- You want to expose more than actions, such as docs, files, schemas, and prompt templates.
- You want tools to be discoverable at runtime.
- You want a local server process that can be launched by a client.
- You want remote servers over HTTP.
- You want clear protocol boundaries for permissions, auth, and auditing.
- You want to separate the integration from the model provider.

MCP is especially helpful for learning and production systems where the same
external capability should not be rewritten again and again.

## A Simple Analogy

Think about USB. You could wire every keyboard differently, but that would make
every computer and every keyboard a custom project. USB gives both sides a
standard contract.

MCP plays a similar role for AI context and actions. The client knows how to ask
what is available. The server knows how to answer. The model gets useful context
through the host, but it does not need to speak the server's private API.

