from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .decoder import DecodeInputError, as_dict, decode_barcodes

mcp = FastMCP(
    "barcodes-reader",
    instructions=(
        "Decode all barcodes in an image (including Data Matrix and many others). "
        "Use `read_barcodes` with either a local image path or base64-encoded image bytes."
    ),
)


@mcp.tool()
def read_barcodes(
    image_path: str | None = None,
    image_base64: str | None = None,
) -> dict:
    """Read all barcodes from one image.

    Args:
        image_path: Local filesystem path to image file. Use this for local MCP-hosted files.
        image_base64: Base64-encoded image bytes. Useful when the client has in-memory image data.

    Returns:
        A JSON object with `count` and `barcodes` fields.
    """

    try:
        decoded = decode_barcodes(image_path=image_path, image_base64=image_base64)
    except DecodeInputError as exc:
        return {
            "ok": False,
            "error": str(exc),
            "count": 0,
            "barcodes": [],
        }

    return {
        "ok": True,
        "count": len(decoded),
        "barcodes": as_dict(decoded),
    }


def main() -> None:
    """Run server over stdio transport."""

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
