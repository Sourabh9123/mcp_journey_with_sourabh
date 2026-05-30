# Diagrams And Flows

This page gives you visual maps for MCP. Read it before the deep chapters, then
come back to it after reading the JSON-RPC examples.

GitHub renders these diagrams with Mermaid. If your editor does not render
Mermaid, read the labels from top to bottom.

## 1. The Big Picture

The most important MCP idea is the boundary between the model and the server.

```mermaid
flowchart LR
    User[User] --> Host[Host application]
    Host --> LLM[LLM]
    Host --> Client[MCP client]
    Client <-->|JSON-RPC over transport| Server[MCP server]
    Server --> Systems[Files, APIs, DBs, docs, tools]

    LLM -. does not directly call .-> Server
```

Meaning:

- The user talks to the host application.
- The host talks to the LLM.
- The MCP client inside the host talks to MCP servers.
- The server exposes tools, resources, and prompts.
- The LLM may request a tool call, but the host and MCP client execute the MCP
  protocol call.

## 2. Startup vs Runtime

MCP has two different moments that are easy to mix up:

- **Startup**: the client discovers what the server can do.
- **Runtime**: the user asks something, the model requests a tool call, and the
  client calls the server.

Startup:

```text
          Startup
             |
             v

MCP Client ---------> MCP Server
    |                    |
    |<---- Tool List ----|
    |
    v
Store Tool Metadata
```

Runtime:

```text
          Runtime
             |
             v

User
 |
 v
LLM
 |
 | Tool Call Request
 v
MCP Client
 |
 v
MCP Server
 |
 | Tool Result
 v
MCP Client
 |
 v
LLM
 |
 v
User
```

What this teaches:

- Tool discovery happens before the user asks for a tool call.
- The client stores tool metadata such as names, descriptions, and schemas.
- At runtime, the LLM asks for a tool call through the host.
- The MCP client calls the MCP server and gives the result back to the LLM.
- The user only sees the final answer unless the host UI also shows tool steps.

## 3. Startup And Initialization

Before the client can call tools or read resources, the connection is
initialized.

```mermaid
sequenceDiagram
    participant H as Host
    participant C as MCP Client
    participant S as MCP Server

    H->>C: Start or connect to server
    C->>S: initialize(protocolVersion, clientInfo, capabilities)
    S-->>C: protocolVersion, serverInfo, capabilities, instructions
    C->>S: notifications/initialized
    C-->>H: Server is ready
```

What this teaches:

- The client starts the protocol with `initialize`.
- The server declares what it supports.
- The client sends `notifications/initialized`.
- Normal requests begin after initialization.

## 4. Discovery Flow

MCP servers are discoverable. The client does not need to hard-code every tool
or resource before connecting.

```mermaid
sequenceDiagram
    participant C as MCP Client
    participant S as MCP Server
    participant H as Host
    participant M as LLM

    C->>S: tools/list
    S-->>C: tool names, descriptions, schemas
    C->>S: resources/list
    S-->>C: resource URIs and metadata
    C->>S: prompts/list
    S-->>C: prompt templates
    C-->>H: Available server features
    H-->>M: Selected tool/resource/prompt context
```

What this teaches:

- The MCP server tells the client what exists.
- The host chooses what to expose to the model.
- The model sees descriptions and context selected by the host, not a raw server
  connection.

## 5. Tool Call Flow

Tools are actions. A model can decide a tool is useful, but the host still
controls execution.

```mermaid
sequenceDiagram
    participant U as User
    participant H as Host
    participant M as LLM
    participant C as MCP Client
    participant S as MCP Server
    participant API as External System

    U->>H: Ask for something that needs action
    H->>M: User request plus selected tool descriptions
    M-->>H: Request tool call with arguments
    H->>H: Validate policy and maybe ask user
    H->>C: Call tool
    C->>S: tools/call(name, arguments)
    S->>API: Perform action or query
    API-->>S: Result
    S-->>C: Tool result
    C-->>H: Tool result
    H->>M: Tool result as context
    M-->>H: Final answer
    H-->>U: Response
```

What this teaches:

- `tools/call` is sent by the MCP client, not directly by the LLM.
- The host can block, approve, or modify what happens.
- Tool results go back to the model through the host.

## 6. Resource Read Flow

Resources are context. Reading a resource should not perform a risky action.

```mermaid
sequenceDiagram
    participant H as Host
    participant M as LLM
    participant C as MCP Client
    participant S as MCP Server

    H->>M: User request
    M-->>H: Needs more context
    H->>C: Read selected resource URI
    C->>S: resources/read(uri)
    S-->>C: Resource contents
    C-->>H: Text or binary content
    H->>M: Resource content as context
    M-->>H: Answer using resource
```

What this teaches:

- Use resources for docs, schemas, files, and examples.
- Long background material belongs in resources, not tool descriptions.
- The host chooses which resource content enters the model context.

## 7. Tool, Resource, Or Prompt?

Use this decision flow when designing a server.

```mermaid
flowchart TD
    Need[What does the model or user need?]
    Need --> Action{Does something need to happen?}
    Action -->|Yes| Tool[Use a tool]
    Action -->|No| Context{Does the model need information?}
    Context -->|Yes| Resource[Use a resource]
    Context -->|No| Workflow{Is it a reusable workflow?}
    Workflow -->|Yes| Prompt[Use a prompt]
    Workflow -->|No| NoMCP[Maybe MCP is not needed here]

    Tool --> ToolExamples[Search, create, update, run, query]
    Resource --> ResourceExamples[Docs, files, schemas, records, examples]
    Prompt --> PromptExamples[Review code, debug logs, write release notes]
```

What this teaches:

- Tools are for actions.
- Resources are for context.
- Prompts are for reusable workflows.

## 8. stdio Transport

stdio is common for local development. The server is usually a subprocess.

```mermaid
flowchart LR
    Client[MCP client process] -->|writes JSON-RPC lines to stdin| Server[MCP server subprocess]
    Server -->|writes JSON-RPC lines to stdout| Client
    Server -->|writes logs to stderr| Logs[Developer logs]
```

Rules:

- One JSON-RPC message per line.
- stdin receives client messages.
- stdout sends server protocol messages.
- stderr is for logs.
- Do not print normal logs to stdout.

## 9. Streamable HTTP Transport

Streamable HTTP is useful for remote or independently hosted MCP servers.

```mermaid
sequenceDiagram
    participant C as MCP Client
    participant S as HTTP MCP Server

    C->>S: POST /mcp initialize
    S-->>C: JSON response, optional MCP-Session-Id
    C->>S: POST /mcp tools/list
    S-->>C: JSON response or SSE stream
    C->>S: POST /mcp tools/call
    S-->>C: JSON response or streamed JSON-RPC messages
```

What this teaches:

- The JSON-RPC message shape stays the same.
- HTTP is the delivery mechanism.
- Servers may use sessions.
- SSE can stream messages when work takes time.

## 10. Safety Flow For Risky Tools

Risky tools should go through policy checks and user approval.

```mermaid
flowchart TD
    ModelCall[Model requests tool call] --> IsRisky{Is the tool risky?}
    IsRisky -->|No| Validate[Validate arguments]
    IsRisky -->|Yes| ShowUser[Show tool name and arguments to user]
    ShowUser --> Approved{User approves?}
    Approved -->|No| Stop[Do not call tool]
    Approved -->|Yes| Validate
    Validate --> Allowed{Arguments and permissions valid?}
    Allowed -->|No| Reject[Return clear error]
    Allowed -->|Yes| Execute[Client calls MCP server]
    Execute --> Result[Return result to host and model]
```

Risky tools include:

- deleting data
- deploying code
- sending messages
- changing permissions
- running shell commands
- spending money
- exporting private data

## 11. One Full Learning Map

Use this map to connect the course pages.

```mermaid
flowchart TD
    Start[README] --> ReadGuide[How To Read]
    ReadGuide --> Diagrams[Diagrams And Flows]
    Diagrams --> Why[Why MCP Exists]
    Why --> Architecture[Architecture And Flow]
    Architecture --> Primitives[Resources, Tools, Prompts]
    Primitives --> Lifecycle[JSON-RPC And Lifecycle]
    Lifecycle --> Transports[stdio And Streamable HTTP]
    Transports --> Build[Building A Server]
    Build --> Design[Design Guidelines]
    Design --> Security[Security And Trust]
    Lifecycle --> Transcript[Raw JSON-RPC Transcript]
    Transports --> Example[Minimal stdio Server]
```

If you get lost, return to this page and identify where you are in the flow.
