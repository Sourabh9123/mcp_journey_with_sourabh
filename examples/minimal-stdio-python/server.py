#!/usr/bin/env python3
"""Tiny educational MCP-style stdio server.

This intentionally avoids SDKs so learners can see JSON-RPC moving over stdin
and stdout. Use an official or well-maintained MCP SDK for real servers.
"""

import json
import sys
from typing import Any


PROTOCOL_VERSION = "2025-11-25"


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def send(message: dict[str, Any]) -> None:
    print(json.dumps(message, separators=(",", ":")), flush=True)


def result(request_id: Any, value: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": value}


def error(request_id: Any, code: int, message: str, data: Any = None) -> dict[str, Any]:
    body: dict[str, Any] = {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": code, "message": message},
    }
    if data is not None:
        body["error"]["data"] = data
    return body


def handle_initialize(request_id: Any) -> dict[str, Any]:
    return result(
        request_id,
        {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {
                "tools": {"listChanged": False},
                "resources": {"listChanged": False},
                "prompts": {"listChanged": False},
            },
            "serverInfo": {
                "name": "minimal-stdio-learning-server",
                "title": "Minimal stdio Learning Server",
                "version": "0.1.0",
            },
            "instructions": "Use resources for long docs. Use tools for actions.",
        },
    )


def handle_tools_list(request_id: Any) -> dict[str, Any]:
    return result(
        request_id,
        {
            "tools": [
                {
                    "name": "add",
                    "title": "Add Numbers",
                    "description": "Add two numbers and return the sum.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number"},
                            "b": {"type": "number"},
                        },
                        "required": ["a", "b"],
                        "additionalProperties": False,
                    },
                    "outputSchema": {
                        "type": "object",
                        "properties": {"sum": {"type": "number"}},
                        "required": ["sum"],
                    },
                }
            ]
        },
    )


def handle_tools_call(request_id: Any, params: dict[str, Any]) -> dict[str, Any]:
    if params.get("name") != "add":
        return error(request_id, -32602, "Unknown tool", {"name": params.get("name")})

    arguments = params.get("arguments", {})
    a = arguments.get("a")
    b = arguments.get("b")

    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        return error(
            request_id,
            -32602,
            "Invalid params",
            {"hint": "add requires numeric arguments: a and b"},
        )

    total = a + b
    return result(
        request_id,
        {
            "content": [{"type": "text", "text": f"{a} + {b} = {total}"}],
            "structuredContent": {"sum": total},
            "isError": False,
        },
    )


def handle_resources_list(request_id: Any) -> dict[str, Any]:
    return result(
        request_id,
        {
            "resources": [
                {
                    "uri": "docs://mcp/tool-design",
                    "name": "tool-design",
                    "title": "Tool Design Notes",
                    "description": "Why long documentation belongs in resources, not tool descriptions.",
                    "mimeType": "text/markdown",
                }
            ]
        },
    )


def handle_resources_read(request_id: Any, params: dict[str, Any]) -> dict[str, Any]:
    uri = params.get("uri")
    if uri != "docs://mcp/tool-design":
        return error(request_id, -32002, "Resource not found", {"uri": uri})

    return result(
        request_id,
        {
            "contents": [
                {
                    "uri": uri,
                    "mimeType": "text/markdown",
                    "text": "# Tool Design\n\nKeep tool descriptions short. Put long docs in resources.",
                }
            ]
        },
    )


def handle_prompts_list(request_id: Any) -> dict[str, Any]:
    return result(
        request_id,
        {
            "prompts": [
                {
                    "name": "explain_mcp_flow",
                    "title": "Explain MCP Flow",
                    "description": "Explain how the host, LLM, MCP client, and MCP server work together.",
                    "arguments": [],
                }
            ]
        },
    )


def handle_prompts_get(request_id: Any, params: dict[str, Any]) -> dict[str, Any]:
    if params.get("name") != "explain_mcp_flow":
        return error(request_id, -32602, "Unknown prompt", {"name": params.get("name")})

    return result(
        request_id,
        {
            "description": "Explain MCP flow.",
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": (
                            "Explain MCP in simple language. Make clear that the LLM "
                            "does not directly talk to the MCP server."
                        ),
                    },
                }
            ],
        },
    )


def dispatch(message: dict[str, Any]) -> dict[str, Any] | None:
    request_id = message.get("id")
    method = message.get("method")
    params = message.get("params") or {}

    if "id" not in message:
        log(f"notification received: {method}")
        return None

    if method == "initialize":
        return handle_initialize(request_id)
    if method == "tools/list":
        return handle_tools_list(request_id)
    if method == "tools/call":
        return handle_tools_call(request_id, params)
    if method == "resources/list":
        return handle_resources_list(request_id)
    if method == "resources/read":
        return handle_resources_read(request_id, params)
    if method == "prompts/list":
        return handle_prompts_list(request_id)
    if method == "prompts/get":
        return handle_prompts_get(request_id, params)

    return error(request_id, -32601, "Method not found", {"method": method})


def main() -> None:
    log("minimal stdio learning server started")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            message = json.loads(line)
        except json.JSONDecodeError as exc:
            send(error(None, -32700, "Parse error", {"detail": str(exc)}))
            continue

        response = dispatch(message)
        if response is not None:
            send(response)


if __name__ == "__main__":
    main()

