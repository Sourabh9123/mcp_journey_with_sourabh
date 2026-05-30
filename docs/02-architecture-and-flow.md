# Architecture And Flow

MCP has a few roles. Mixing them up is the most common beginner confusion.

## The Roles

```text
User
  |
  v
Host application
  |                      Local process or remote service
  | contains             |
  v                      v
LLM <---- host ----> MCP client <---- JSON-RPC ----> MCP server
```

The host application is the product the user sees. It might be an editor, chat
app, agent runtime, desktop app, or internal tool.

The MCP client is usually inside the host. It knows how to connect to MCP
servers, initialize them, list their capabilities, call tools, and read
resources.

The MCP server is the integration boundary. It exposes tools, resources, and
prompts. It might run locally over stdio or remotely over Streamable HTTP.

The LLM is not the MCP client. The LLM does not open a socket to your MCP server
or write JSON-RPC to stdin. The host and MCP client do that.

## The Normal Flow

Here is the lifecycle in simple language:

1. The host starts or connects to an MCP server.
2. The MCP client sends `initialize`.
3. The server replies with its protocol version, capabilities, and server info.
4. The client sends `notifications/initialized`.
5. The client asks what tools, resources, and prompts exist.
6. The host decides what descriptions or context to show the LLM.
7. The user asks something.
8. The LLM may decide a tool call is needed.
9. The host asks the MCP client to call that tool.
10. The MCP client sends `tools/call` to the server.
11. The server executes the tool and returns a result.
12. The host gives the result back to the LLM.
13. The LLM writes the final answer for the user.

## Important Boundary

The server usually receives only structured protocol calls, such as:

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "method": "tools/call",
  "params": {
    "name": "search_docs",
    "arguments": {
      "query": "how do migrations work?"
    }
  }
}
```

It does not automatically receive the whole user conversation. If a server needs
context, the client must pass it intentionally through arguments, resources,
roots, or other negotiated protocol features.

## Who Decides What?

The model can suggest or choose a tool call based on what the host made visible
to it. The host still controls execution:

- Which servers are connected.
- Which tools are exposed to the model.
- Whether the user must confirm a call.
- Whether a call is allowed.
- What arguments are sent.
- What result is shown back to the model.

This is why MCP is not "the model has direct access to everything". It is a
protocol layer that lets the host mediate access.

## Discovery Flow

After initialization, the client can ask the server what it has:

```text
Client -> Server: tools/list
Server -> Client: list of tool names, descriptions, and input schemas

Client -> Server: resources/list
Server -> Client: list of available resources and metadata

Client -> Server: prompts/list
Server -> Client: list of reusable prompt templates
```

The host may then include selected tool descriptions in the LLM request, show
resources in a picker, or expose prompts as commands.

## Tool Call Flow

```text
User: "Find recent failed deployments and summarize the cause."

Host gives LLM available tool info:
  - search_deployments
  - get_deployment_log

LLM asks host to call:
  search_deployments({ "status": "failed" })

Host checks policy and maybe asks user.

MCP client sends:
  tools/call search_deployments

MCP server returns:
  failed deployment records

Host gives results to LLM.

LLM writes:
  "The latest failures were caused by missing environment variables..."
```

The MCP server did the external work. The model reasoned over the result. The
host controlled the bridge.

