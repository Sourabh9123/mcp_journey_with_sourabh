# Resources, Tools, Prompts, Roots, Sampling

MCP has several primitives. They solve different problems. A strong MCP server
uses the right primitive for the right job.

## Tools

Tools are callable actions.

Use a tool when something needs to happen:

- Query a database.
- Search an index.
- Create a ticket.
- Send a message.
- Run a build.
- Convert a file.
- Fetch a record by ID.

A tool has:

- `name`: stable identifier used by the protocol.
- `title`: optional display name for humans.
- `description`: short explanation of what it does.
- `inputSchema`: JSON Schema for arguments.
- Optional `outputSchema`: JSON Schema for structured results.
- Optional annotations and metadata.

Tools are generally model-controlled. That means the model can decide a tool is
useful based on the user's request, but the host still mediates the actual call.

Good tool:

```json
{
  "name": "search_docs",
  "title": "Search Documentation",
  "description": "Search the product documentation for pages matching a query.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Search query in natural language."
      },
      "limit": {
        "type": "integer",
        "minimum": 1,
        "maximum": 10,
        "default": 5
      }
    },
    "required": ["query"]
  }
}
```

Bad tool:

```json
{
  "name": "do_everything",
  "description": "Can search docs, deploy services, delete records, create tickets, update users, and run scripts. Here are 500 lines of documentation..."
}
```

The bad tool is hard for a model to choose safely and hard for a user to trust.

## Resources

Resources are readable context.

Use a resource when the model needs information but no action should happen:

- Project README.
- API documentation.
- Database schema.
- File contents.
- Current app configuration.
- Logs.
- Knowledge base article.
- Example code.

A resource has a URI, metadata, and content that can be read by the client.
Resource contents may be text or base64-encoded binary data.

Example resource:

```json
{
  "uri": "docs://payments/refunds",
  "name": "refunds",
  "title": "Refund Policy",
  "description": "Rules and API behavior for creating refunds.",
  "mimeType": "text/markdown"
}
```

Read result:

```json
{
  "contents": [
    {
      "uri": "docs://payments/refunds",
      "mimeType": "text/markdown",
      "text": "# Refund Policy\n\nRefunds must reference a settled charge..."
    }
  ]
}
```

## Do Not Put Huge Docs In Tool Descriptions

Tool descriptions are hints for choosing and using tools. They should be short.

If a tool needs lots of background, put that background in resources.

Prefer this:

- Resource: `docs://payments/refunds`
- Tool: `create_refund`
- Prompt: `review_refund_request`

Instead of this:

- Tool: `create_refund` with 800 lines of refund policy inside the description.

Why:

- Long descriptions waste model context.
- They make tool lists noisy.
- They are harder to update.
- They blur the difference between "context" and "action".
- They increase the chance that the model misses the exact input schema.

## Resource Templates

Resource templates are parameterized resources. They let the server say:

```json
{
  "uriTemplate": "docs://service/{name}",
  "name": "service_docs",
  "description": "Documentation for a named internal service.",
  "mimeType": "text/markdown"
}
```

The client can use the template to read resources such as:

```text
docs://service/billing
docs://service/search
docs://service/auth
```

This is useful when the possible resources are too many to list one by one.

## Prompts

Prompts are reusable templates exposed by the server.

Use prompts for workflows the user may choose:

- "Review this code."
- "Create a bug report from these logs."
- "Explain this database schema."
- "Generate a migration plan."

Prompts are generally user-controlled. They are often shown as commands,
templates, or menu items in the host UI.

Example prompt:

```json
{
  "name": "debug_failed_job",
  "title": "Debug Failed Job",
  "description": "Guide the model through analyzing a failed background job.",
  "arguments": [
    {
      "name": "job_id",
      "description": "The failed job ID.",
      "required": true
    }
  ]
}
```

When the client asks for the prompt, the server returns messages:

```json
{
  "description": "Debug a failed background job.",
  "messages": [
    {
      "role": "user",
      "content": {
        "type": "text",
        "text": "Analyze failed job job_123. Start by reading logs and identifying the first error."
      }
    }
  ]
}
```

## Roots

Roots are a client feature. They tell a server what filesystem roots or project
locations the client has made available.

For example, an IDE might tell a filesystem server:

```text
You may work inside /home/me/project-a
You may work inside /home/me/project-b
```

The server should not assume it can access any path on the machine. Roots help
define the intended working boundary.

## Sampling

Sampling is a client feature that lets a server ask the client to request an LLM
completion.

This is advanced. The important mental model is:

- The server still does not directly call the model.
- The server asks the client for sampling.
- The client decides whether and how to involve the model.

This keeps model access inside the host's policy and permission layer.

## Quick Choice Guide

| Need | Use |
| --- | --- |
| The model needs to perform an action | Tool |
| The model needs to read context | Resource |
| The user wants a reusable workflow | Prompt |
| The server needs allowed project locations | Roots |
| The server needs the client to ask an LLM something | Sampling |

