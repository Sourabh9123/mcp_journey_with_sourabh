# Design Guidelines

Good MCP servers are boring to call and easy to trust.

## Keep Tools Small

Prefer focused tools:

- `search_docs`
- `read_doc`
- `create_ticket`
- `get_ticket`

Avoid vague tools:

- `manage_everything`
- `run_command`
- `do_task`
- `api_call`

Small tools are easier for the model to choose, easier for the host to approve,
and easier for users to understand.

## Keep Descriptions Short

A tool description should explain:

- What the tool does.
- When to use it.
- Any important limit.

It should not contain full manuals, API docs, policy documents, or long examples.
Put those in resources.

Example:

```json
{
  "name": "create_refund",
  "description": "Create a refund for a settled charge. Read docs://payments/refunds before using for unfamiliar cases."
}
```

## Put Knowledge In Resources

Use resources for:

- Long documentation.
- API reference.
- Database schemas.
- Business rules.
- Examples.
- Change logs.

Then tools can refer to those resources by URI.

This gives the host a choice: include the resource only when needed instead of
always paying the context cost.

## Use Precise Schemas

Good schema:

```json
{
  "type": "object",
  "properties": {
    "charge_id": {
      "type": "string",
      "pattern": "^ch_[a-zA-Z0-9]+$"
    },
    "amount_cents": {
      "type": "integer",
      "minimum": 1
    },
    "reason": {
      "type": "string",
      "enum": ["duplicate", "fraudulent", "requested_by_customer"]
    }
  },
  "required": ["charge_id", "amount_cents", "reason"],
  "additionalProperties": false
}
```

Weak schema:

```json
{
  "type": "object",
  "properties": {
    "data": {
      "type": "object"
    }
  }
}
```

Precise schemas reduce ambiguity and bad calls.

## Separate Read From Write

Prefer:

- `get_ticket`
- `search_tickets`
- `create_ticket`
- `update_ticket_status`

Avoid one `ticket` tool that reads and writes depending on a mode argument.

Separate tools let the host apply different permissions. A read tool may be safe
to run automatically. A write tool may need confirmation.

## Make Dangerous Operations Obvious

Dangerous operations include:

- deleting data
- sending messages
- changing permissions
- deploying code
- running shell commands
- spending money
- exporting private data

The tool name and description should make the risk clear. The host should ask
for user confirmation before execution.

## Return Data The Model Can Use

If the result is only text, the model must parse it. Sometimes that is fine.

For multi-step workflows, return structured content too:

```json
{
  "content": [
    {
      "type": "text",
      "text": "Found 2 failed deployments."
    }
  ],
  "structuredContent": {
    "deployments": [
      {
        "id": "dep_123",
        "service": "billing",
        "status": "failed",
        "failed_at": "2026-05-30T12:10:00Z"
      }
    ]
  }
}
```

## Version Your Behavior

If a tool's behavior changes in a breaking way, do not silently change it.

Options:

- Add a new tool name, such as `search_docs_v2`.
- Add an explicit argument, such as `mode`.
- Keep the old behavior and expose a new resource explaining migration.

Stable behavior helps clients and models learn the server safely.

