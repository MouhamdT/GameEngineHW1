"""Small local-only client for Epic's bundled Unreal MCP server.

Usage: python tools/unreal_mcp.py list_toolsets '{}'
       python tools/unreal_mcp.py call_tool @Saved/Automation/request.json
Tool calls are serialized; this helper never starts or edits an editor by itself.
"""

import argparse
import json
import urllib.request


class UnrealMCP:
    def __init__(self, port=8000):
        self.url = f"http://127.0.0.1:{int(port)}/mcp"
        self.session = None
        self.next_id = 0

    def request(self, method, params=None, notification=False):
        self.next_id += 1
        payload = {"jsonrpc": "2.0", "method": method}
        if not notification:
            payload["id"] = self.next_id
        if params is not None:
            payload["params"] = params
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if self.session:
            headers["Mcp-Session-Id"] = self.session
            headers["MCP-Protocol-Version"] = "2024-11-05"
        req = urllib.request.Request(
            self.url, json.dumps(payload).encode("utf-8"), headers, method="POST"
        )
        with urllib.request.urlopen(req, timeout=120) as response:
            self.session = response.headers.get("Mcp-Session-Id", self.session)
            if notification or response.status == 202:
                return None
            if "text/event-stream" in response.headers.get("Content-Type", ""):
                data = []
                for raw_line in response:
                    line = raw_line.decode("utf-8").rstrip("\r\n")
                    if line.startswith("data:"):
                        data.append(line[5:].lstrip())
                    elif not line and data:
                        message = json.loads("\n".join(data))
                        data = []
                        if message.get("id") == payload["id"]:
                            return self._result(message)
                raise RuntimeError("MCP stream ended without a matching response")
            return self._result(json.load(response))

    @staticmethod
    def _result(message):
        if "error" in message:
            raise RuntimeError(json.dumps(message["error"]))
        return message.get("result")

    def connect(self):
        result = self.request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "homework-editor-client", "version": "1.0"},
        })
        self.request("notifications/initialized", notification=True)
        return result

    def call(self, name, arguments):
        return self.request("tools/call", {"name": name, "arguments": arguments})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tool", help="Tool name, or initialize/tools-list")
    parser.add_argument("arguments", nargs="?", default="{}")
    args = parser.parse_args()
    if args.arguments.startswith("@"):
        with open(args.arguments[1:], encoding="utf-8") as stream:
            arguments = json.load(stream)
    else:
        arguments = json.loads(args.arguments)
    client = UnrealMCP()
    initialized = client.connect()
    if args.tool == "initialize":
        result = initialized
    elif args.tool == "tools-list":
        result = client.request("tools/list")
    else:
        result = client.call(args.tool, arguments)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
