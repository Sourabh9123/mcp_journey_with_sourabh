# Raw JSON-RPC Transcript: Basic MCP Flow

This transcript shows the shape of messages between an MCP client and server.
It is not a full production session, but it is enough to see the protocol.

## 1. Initialize

Client to server:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-11-25",
    "capabilities": {},
    "clientInfo": {
      "name": "example-client",
      "title": "Example Client",
      "version": "0.1.0"
    }
  }
}
```

Server to client:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-11-25",
    "capabilities": {
      "tools": {
        "listChanged": false
      },
      "resources": {
        "listChanged": false
      },
      "prompts": {
        "listChanged": false
      }
    },
    "serverInfo": {
      "name": "example-learning-server",
      "title": "Example Learning Server",
      "version": "0.1.0"
    },
    "instructions": "Use resources for long documentation. Use tools only for actions."
  }
}
```

Client to server:

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}
```

## 2. List Tools

Client to server:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {}
}
```

Server to client:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "add",
        "title": "Add Numbers",
        "description": "Add two numbers and return the sum.",
        "inputSchema": {
          "type": "object",
          "properties": {
            "a": {
              "type": "number"
            },
            "b": {
              "type": "number"
            }
          },
          "required": ["a", "b"],
          "additionalProperties": false
        },
        "outputSchema": {
          "type": "object",
          "properties": {
            "sum": {
              "type": "number"
            }
          },
          "required": ["sum"]
        }
      }
    ]
  }
}
```

## 3. Call Tool

Client to server:

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "add",
    "arguments": {
      "a": 2,
      "b": 5
    }
  }
}
```

Server to client:

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "2 + 5 = 7"
      }
    ],
    "structuredContent": {
      "sum": 7
    },
    "isError": false
  }
}
```

## 4. List Resources

Client to server:

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "resources/list",
  "params": {}
}
```

Server to client:

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "result": {
    "resources": [
      {
        "uri": "docs://mcp/tool-design",
        "name": "tool-design",
        "title": "Tool Design Notes",
        "description": "Guidance for keeping tools small and moving long docs into resources.",
        "mimeType": "text/markdown"
      }
    ]
  }
}
```

## 5. Read Resource

Client to server:

```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "method": "resources/read",
  "params": {
    "uri": "docs://mcp/tool-design"
  }
}
```

Server to client:

```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "result": {
    "contents": [
      {
        "uri": "docs://mcp/tool-design",
        "mimeType": "text/markdown",
        "text": "# Tool Design\n\nKeep tools focused. Put long documentation in resources."
      }
    ]
  }
}
```

## 6. List Prompts

Client to server:

```json
{
  "jsonrpc": "2.0",
  "id": 6,
  "method": "prompts/list",
  "params": {}
}
```

Server to client:

```json
{
  "jsonrpc": "2.0",
  "id": 6,
  "result": {
    "prompts": [
      {
        "name": "explain_mcp_flow",
        "title": "Explain MCP Flow",
        "description": "Create a beginner-friendly explanation of host, client, server, and LLM flow.",
        "arguments": []
      }
    ]
  }
}
```

## 7. Get Prompt

Client to server:

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "method": "prompts/get",
  "params": {
    "name": "explain_mcp_flow",
    "arguments": {}
  }
}
```

Server to client:

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "result": {
    "description": "Explain MCP flow.",
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "Explain MCP using simple language. Emphasize that the LLM talks through the host and MCP client, not directly to the MCP server."
        }
      }
    ]
  }
}
```

