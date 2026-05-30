# JSON-RPC And Lifecycle

MCP messages are JSON-RPC 2.0 messages. JSON-RPC gives MCP a small, predictable
wire format for requests, responses, notifications, and errors.

## Request

A request has an `id`. The receiver must send a response with the same `id`.

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

## Response

A successful response has `result`.

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": []
  }
}
```

## Notification

A notification has no `id`. The receiver does not send a response.

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}
```

## Error

An error response has `error` instead of `result`.

```json
{
  "jsonrpc": "2.0",
  "id": 9,
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": {
      "reason": "Missing required argument: query"
    }
  }
}
```

Common JSON-RPC error codes:

| Code | Meaning |
| --- | --- |
| `-32700` | Parse error |
| `-32600` | Invalid request |
| `-32601` | Method not found |
| `-32602` | Invalid params |
| `-32603` | Internal error |

MCP also defines some feature-specific errors, such as resource not found.

## Lifecycle

An MCP connection has three broad phases:

1. Initialization.
2. Operation.
3. Shutdown.

Initialization must happen first. The client and server agree on the protocol
version and capabilities before normal requests begin.

## Step 1: Client Sends initialize

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-11-25",
    "capabilities": {
      "roots": {
        "listChanged": true
      },
      "sampling": {}
    },
    "clientInfo": {
      "name": "learning-client",
      "title": "Learning Client",
      "version": "0.1.0"
    }
  }
}
```

This says:

- I am the client.
- I support protocol version `2025-11-25`.
- These are my client capabilities.
- Here is my client name and version.

## Step 2: Server Replies

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-11-25",
    "capabilities": {
      "tools": {
        "listChanged": true
      },
      "resources": {
        "subscribe": true,
        "listChanged": true
      },
      "prompts": {
        "listChanged": true
      },
      "logging": {}
    },
    "serverInfo": {
      "name": "learning-server",
      "title": "Learning Server",
      "version": "0.1.0"
    },
    "instructions": "Use resources for detailed documentation and tools for actions."
  }
}
```

This says:

- I can speak this protocol version.
- I expose tools, resources, prompts, and logging.
- Here is my server identity.
- Here are optional instructions that may help the client or model.

## Step 3: Client Sends initialized

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}
```

Now normal operation can begin.

## Step 4: Client Discovers Server Features

List tools:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {}
}
```

List resources:

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "resources/list",
  "params": {}
}
```

List prompts:

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "prompts/list",
  "params": {}
}
```

## Capability Negotiation

Capabilities prevent guessing. If the server did not declare `resources`, the
client should not call `resources/list`. If the client did not declare a feature,
the server should not assume it exists.

Examples:

- Server capability `tools`: client can list and call tools.
- Server capability `resources`: client can list and read resources.
- Server capability `prompts`: client can list and get prompts.
- Server capability `logging`: server can send structured log messages.
- Client capability `roots`: server can ask which roots are available.
- Client capability `sampling`: server can ask client for LLM sampling.

## Shutdown

MCP does not need a special JSON-RPC shutdown message in the common lifecycle.
The underlying transport closes:

- stdio: the process exits or streams close.
- HTTP: the session may be deleted or expire.

Servers should clean up resources when the connection or session ends.

