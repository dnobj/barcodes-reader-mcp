# barcodes-reader-mcp

A Python MCP server (stdio transport) that decodes **all barcodes detected in a single image**, including:

- Data Matrix
- QR Code
- EAN / UPC
- Code 39 / 93 / 128
- PDF417
- Aztec
- and other formats supported by `zxing-cpp`

## Why this design

This implementation uses the current official Python MCP SDK (`mcp`) with a tool-first interface, which matches current MCP client expectations for tool invocation over stdio.

## Tool

### `read_barcodes`

Inputs (exactly one required):

- `image_path: str` – local path to an image file
- `image_base64: str` – base64-encoded image bytes

Returns:

```json
{
  "ok": true,
  "count": 2,
  "barcodes": [
    {
      "format": "DataMatrix",
      "text": "ABC123",
      "position": [{"x":0,"y":0},{"x":10,"y":0},{"x":10,"y":10},{"x":0,"y":10}]
    }
  ]
}
```

## Install

```bash
pip install -e .
```

## Run (stdio)

```bash
barcodes-reader-mcp
```

## Example MCP client config

```json
{
  "mcpServers": {
    "barcodes-reader": {
      "command": "barcodes-reader-mcp"
    }
  }
}
```
