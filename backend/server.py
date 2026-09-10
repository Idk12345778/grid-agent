import sys
import os
from pathlib import Path
from mcp.server.transport_security import TransportSecuritySettings
from starlette.requests import Request
from starlette.responses import JSONResponse


# Ensure backend directory is in sys.path when running from any cwd
backend_dir = str(Path(__file__).parent.resolve())
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from mcp.server import MCPServer
from grid import Grid

mcp = MCPServer("Grid Server")

grid = Grid(5, 5)

@mcp.custom_route("/position", methods = ["GET"])
async def position(request: Request) :
    return JSONResponse(
        grid.get_position(),
        headers = {"Access-Control-Allow-Origin": "*"},
    )


@mcp.tool()
def move_up() -> bool:
    """Move the agent up by one unit on the 5x5 grid.
    Returns True if successful, False if the object is already at the top."""
    return grid.move_up()

@mcp.tool()
def move_down() -> bool:
    """Move the agent down by one unit on the 5x5 grid. 
    Returns True if successful, False if the object is already at the bottom."""
    return grid.move_down()

@mcp.tool()
def move_left() -> bool:
    """Move the agent left by one unit on the 5x5 grid. 
    Returns True if successful, False if the object is already at the left boundary."""
    return grid.move_left()

@mcp.tool()
def move_right() -> bool:
    """Move the agent right by one unit on the 5x5 grid. 
    Returns True if successful, False if the object is already at the right boundary."""
    return grid.move_right()

@mcp.tool()
def get_position() -> dict:
    """Get the current (x, y) position of the agent on the grid."""
    return grid.get_position()


security = TransportSecuritySettings(
    allowed_hosts = [
        "grid-agent.onrender.com",
        "grid-agent.onrender.com:*"
    ],
)
if __name__ == "__main__":
    mcp.run(
        transport = "streamable-http",
        host = "0.0.0.0",
        port = int(os.environ.get("PORT", 8001)), 
        transport_security = security,

    )