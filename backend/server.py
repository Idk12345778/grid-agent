import sys
import os
from pathlib import Path
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from mcp.server.transport_security import TransportSecuritySettings

# Ensure backend directory is in sys.path when running from any cwd
backend_dir = str(Path(__file__).parent.resolve())
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from mcp.server import MCPServer
from grid import Grid

mcp = MCPServer("Grid Server")

grid = Grid(5, 5)

@mcp.tool()
def move_up() -> bool:
    """Move the agent up by one unit on the grid. Returns True if successful."""
    return grid.move_up()

@mcp.tool()
def move_down() -> bool:
    """Move the agent down by one unit on the grid. Returns True if successful."""
    return grid.move_down()

@mcp.tool()
def move_left() -> bool:
    """Move the agent left by one unit on the grid. Returns True if successful."""
    return grid.move_left()

@mcp.tool()
def move_right() -> bool:
    """Move the agent right by one unit on the grid. Returns True if successful."""
    return grid.move_right()

@mcp.tool()
def get_position() -> dict:
    """Get the current (x, y) position of the agent on the grid."""
    return grid.get_position()


class PositionHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/position":
            position = grid.get_position()

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            self.wfile.write(json.dumps(position).encode("utf-8"))
    def log_message(self, format, *args):
        pass

def start_api():
    server = HTTPServer(("localhost", 8000), PositionHandler)
    server.serve_forever()

security = TransportSecuritySettings(
    allowed_hosts = [
        "grid-agent.onrender.com",
        "grid-agent.onrender.com:*"
    ],
)
if __name__ == "__main__":
    threading.Thread(target = start_api, daemon=True).start()
    mcp.run(
        transport = "streamable-http",
        host = "0.0.0.0",
        port = int(os.environ.get("PORT", 8001)), 
        transport_security = security,

    )