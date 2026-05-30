# Transports: stdio And Streamable HTTP

MCP is transport-aware but message-format consistent. The JSON-RPC message shape
stays the same, while the way messages move differs.

The two standard transports in the current MCP spec are:

- `stdio`
- Streamable HTTP

Custom transports are possible, but they must preserve MCP's JSON-RPC message
format and lifecycle rules.

## stdio

stdio is the most common transport for local development.

In stdio:

- The client launches the server as a subprocess.
- The client writes JSON-RPC messages to the server's stdin.
- The server writes JSON-RPC messages to stdout.
- Each message is one line.
- Messages must not contain embedded newlines.
- The server can write logs to stderr.
- The server must not write non-MCP text to stdout.

That last rule matters a lot. This is valid on stdout:

```json
{"jsonrpc":"2.0","id":1,"result":{"tools":[]}}
```

This is not valid on stdout:

```text
Starting server...
{"jsonrpc":"2.0","id":1,"result":{"tools":[]}}
```

The client expects stdout to contain only protocol messages. Put logs on stderr.

## stdio Mental Model

```text
Host app
  |
  | starts subprocess
  v
MCP server process

Client writes to server stdin:
  {"jsonrpc":"2.0","id":1,"method":"initialize",...}

Server writes to stdout:
  {"jsonrpc":"2.0","id":1,"result":...}

Server writes logs to stderr:
  indexed 20 files
```

stdio is great for:

- local tools
- filesystem access
- IDE integrations
- developer machines
- quick learning
- servers distributed as command-line programs

stdio is less ideal when:

- many users need the same remote service
- authentication is web-based
- the server must scale independently
- clients are browsers or remote agents

## Streamable HTTP

Streamable HTTP is for remote or independently hosted MCP servers.

In Streamable HTTP:

- The server exposes a single MCP endpoint, such as `/mcp`.
- Client-to-server messages use HTTP `POST`.
- The POST body is one JSON-RPC request, response, or notification.
- The client sends an `Accept` header that supports `application/json` and
  `text/event-stream`.
- The server can reply with one JSON response or open an SSE stream.
- The client may use HTTP `GET` to listen for server messages.
- Sessions may be tracked with `MCP-Session-Id`.
- HTTP requests after initialization should include `MCP-Protocol-Version`.

Simple request:

```http
POST /mcp HTTP/1.1
Host: example.com
Accept: application/json, text/event-stream
Content-Type: application/json
MCP-Protocol-Version: 2025-11-25

{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
```

Simple response:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{"jsonrpc":"2.0","id":2,"result":{"tools":[]}}
```

## Why Streamable HTTP Can Use SSE

Some server work is not instant. The server may need to stream progress,
notifications, or a delayed response. For that, it can return
`text/event-stream` and send Server-Sent Events containing JSON-RPC messages.

Example SSE event body:

```text
event: message
data: {"jsonrpc":"2.0","id":2,"result":{"tools":[]}}
```

The client still receives JSON-RPC messages. SSE is only the delivery container.

## Session Management

A Streamable HTTP server may assign a session ID during initialization:

```http
MCP-Session-Id: 550e8400-e29b-41d4-a716-446655440000
```

If the server returns this header, the client must include it in later requests:

```http
MCP-Session-Id: 550e8400-e29b-41d4-a716-446655440000
```

This helps the server connect multiple HTTP requests to the same logical MCP
session.

## Security For HTTP

For Streamable HTTP:

- Validate the `Origin` header to reduce DNS rebinding risk.
- Bind local HTTP servers to `127.0.0.1`, not `0.0.0.0`, unless you really mean
  to expose them.
- Use proper authentication for remote servers.
- Treat session IDs like secrets.
- Validate every tool argument and resource URI.

## stdio vs Streamable HTTP

| Question | Prefer stdio | Prefer Streamable HTTP |
| --- | --- | --- |
| Is the server local to one user? | Yes | Maybe |
| Is this for local development? | Yes | Maybe |
| Is the server shared by many users? | No | Yes |
| Do you need normal web auth? | No | Yes |
| Do you want a CLI-style server? | Yes | No |
| Do you need independent service scaling? | No | Yes |

## Legacy HTTP+SSE

Older MCP versions used an HTTP+SSE transport shape. Current MCP uses
Streamable HTTP instead. If you are reading older tutorials, check which
protocol version and transport they use.

