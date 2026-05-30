# Minimal Educational stdio Server

This folder contains a tiny MCP-like stdio server written with only the Python
standard library.

It is for learning the wire shape. It is not a production MCP server.

For real projects, use an MCP SDK. An SDK will handle protocol details more
completely and track spec changes better than a hand-written JSON loop.

## Run

From this folder:

```bash
python3 server.py
```

Then paste one JSON-RPC message per line into stdin.

Example initialize request:

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"manual-client","version":"0.1.0"}}}
```

Example tool call:

```json
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"add","arguments":{"a":2,"b":5}}}
```

Remember: with stdio, stdout must contain only JSON-RPC messages. This example
writes logs to stderr.

