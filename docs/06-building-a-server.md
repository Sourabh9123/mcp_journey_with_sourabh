# Building An MCP Server

This page explains how to design an MCP server before writing code.

## Step 1: Pick The Server's Job

Write one sentence:

```text
This server helps AI clients work with ______________.
```

Examples:

- This server helps AI clients work with local project files.
- This server helps AI clients search company documentation.
- This server helps AI clients inspect deployments.
- This server helps AI clients query a read-only analytics database.

If the sentence has too many "and" parts, split the server.

## Step 2: Identify Resources

Ask: what context should the model be able to read?

Examples:

- `docs://index`
- `docs://service/{name}`
- `schema://database/public`
- `file:///{path}`
- `deployments://service/{name}/latest`

Resources should be stable, readable, and permission-checked.

Use resources for long or detailed information. Do not bury that information in
tool descriptions.

## Step 3: Identify Tools

Ask: what actions should the model be able to request?

Examples:

- `search_docs`
- `get_deployment`
- `run_readonly_sql`
- `create_ticket`
- `summarize_log_window`

For each tool, define:

- What it does.
- What it never does.
- Input JSON Schema.
- Output shape.
- Permissions needed.
- Whether user confirmation is needed.
- Failure modes.

## Step 4: Identify Prompts

Ask: what repeatable workflows should users be able to select?

Examples:

- `debug_failed_deployment`
- `write_release_notes`
- `review_api_change`
- `explain_schema`

Prompts are a good way to package a workflow without making one giant tool.

## Step 5: Choose A Transport

Use stdio when:

- The server runs locally.
- You are learning.
- You are building a command-line integration.
- The server needs local files or local tools.

Use Streamable HTTP when:

- The server is remote.
- Many users connect to it.
- You need web authentication.
- You need independent deployment and scaling.

## Step 6: Use An SDK For Real Servers

The raw JSON-RPC examples in this repository are educational. For real servers,
prefer an MCP SDK in your language because it handles protocol details such as:

- message parsing
- initialization
- capability declarations
- pagination
- content block formatting
- error responses
- transport details

The goal of the examples here is to make the protocol visible, not to replace an
SDK.

## Step 7: Implement The Basic Handlers

A small server usually needs handlers for:

- `initialize`
- `tools/list`
- `tools/call`
- `resources/list`
- `resources/read`
- `resources/templates/list`
- `prompts/list`
- `prompts/get`

Not every server needs every feature. If the server only exposes tools, declare
only `tools`.

## Step 8: Return Useful Results

Tool results can include human-readable text and structured content.

Human-readable result:

```json
{
  "content": [
    {
      "type": "text",
      "text": "Found 3 matching documents."
    }
  ],
  "isError": false
}
```

Structured result:

```json
{
  "content": [
    {
      "type": "text",
      "text": "Found 3 matching documents."
    }
  ],
  "structuredContent": {
    "matches": [
      {
        "title": "Refund Policy",
        "uri": "docs://payments/refunds",
        "score": 0.91
      }
    ]
  },
  "isError": false
}
```

Use structured content when the caller may need to inspect, filter, or pass the
data into another step.

## Step 9: Handle Errors Clearly

Bad errors:

```text
failed
something went wrong
```

Better errors:

```json
{
  "jsonrpc": "2.0",
  "id": 8,
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": {
      "missing": ["query"],
      "hint": "search_docs requires a non-empty query string."
    }
  }
}
```

The model and user can recover better when the error says what was wrong.

## Step 10: Test With A Client Or Inspector

At minimum, verify:

- The server initializes.
- The declared capabilities match the handlers.
- Tool schemas are valid.
- Tool calls reject invalid arguments.
- Resource reads cannot escape allowed boundaries.
- Logs go to stderr for stdio.
- stdout contains only JSON-RPC messages for stdio.
- HTTP servers validate origin and auth.

