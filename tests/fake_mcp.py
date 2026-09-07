# -*- coding: utf-8 -*-
"""In-process fake Unity MCP HTTP for S00-c. No live Editor."""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from typing import Any


class FakeMCP:
    def __init__(self, mode: str = "notify_then_result") -> None:
        self.mode = mode
        self.calls: list[dict[str, Any]] = []
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, fmt: str, *args: Any) -> None:  # noqa: A003
                return

            def do_POST(self) -> None:  # noqa: N802
                length = int(self.headers.get("Content-Length") or "0")
                raw = self.rfile.read(length) if length else b"{}"
                try:
                    payload = json.loads(raw.decode("utf-8"))
                except json.JSONDecodeError:
                    payload = {}
                outer.calls.append(payload)
                method = payload.get("method") or ""
                req_id = payload.get("id")
                if method == "initialize":
                    body = json.dumps(
                        {
                            "jsonrpc": "2.0",
                            "id": req_id,
                            "result": {
                                "protocolVersion": "2025-03-26",
                                "capabilities": {},
                                "serverInfo": {"name": "fake-mcp", "version": "0"},
                            },
                        }
                    ).encode("utf-8")
                    self._send(body, "application/json")
                    return
                if method.startswith("notifications/"):
                    self.send_response(202)
                    self.end_headers()
                    return
                if method == "tools/list":
                    body = json.dumps(
                        {
                            "jsonrpc": "2.0",
                            "id": req_id,
                            "result": {"tools": [{"name": "vrc_audit"}]},
                        }
                    ).encode("utf-8")
                    self._send(body, "application/json")
                    return
                if outer.mode == "hang":
                    return
                if outer.mode == "rpc_error":
                    chunk = json.dumps(
                        {
                            "jsonrpc": "2.0",
                            "id": req_id,
                            "error": {"code": -32000, "message": "boom"},
                        }
                    )
                    self._send_sse([chunk])
                    return
                if outer.mode == "is_error":
                    chunk = json.dumps(
                        {
                            "jsonrpc": "2.0",
                            "id": req_id,
                            "result": {
                                "isError": True,
                                "content": [{"type": "text", "text": "NO_AVATAR"}],
                            },
                        }
                    )
                    self._send_sse([chunk])
                    return
                if outer.mode == "notify_only":
                    note = json.dumps(
                        {
                            "jsonrpc": "2.0",
                            "method": "notifications/progress",
                            "params": {"progress": 0.4},
                        }
                    )
                    self._send_sse([note])
                    return
                note = json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "method": "notifications/progress",
                        "params": {"progress": 0.4},
                    }
                )
                result = json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {"content": [{"type": "text", "text": "ok"}]},
                    }
                )
                self._send_sse([note, result])

            def _send(self, body: bytes, ctype: str) -> None:
                self.send_response(200)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(body)))
                self.send_header("mcp-session-id", "fake-session")
                self.end_headers()
                self.wfile.write(body)

            def _send_sse(self, chunks: list[str]) -> None:
                lines = "".join("data: %s\n\n" % c for c in chunks)
                self._send(lines.encode("utf-8"), "text/event-stream")

        self._httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.port = int(self._httpd.server_address[1])
        self.thread = Thread(target=self._httpd.serve_forever, daemon=True)

    @property
    def url(self) -> str:
        return "http://127.0.0.1:%d/mcp" % self.port

    def start(self) -> None:
        self.thread.start()

    def stop(self) -> None:
        self._httpd.shutdown()
        self._httpd.server_close()
