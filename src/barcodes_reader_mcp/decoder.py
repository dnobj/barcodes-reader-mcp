from __future__ import annotations

import base64
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class BarcodeResult:
    """Normalized decoded barcode result."""

    format: str
    text: str
    position: list[dict[str, int]]


class DecodeInputError(ValueError):
    """Raised when no valid image input can be decoded."""


def _load_image(*, image_path: str | None, image_base64: str | None):
    if bool(image_path) == bool(image_base64):
        raise DecodeInputError("Provide exactly one of `image_path` or `image_base64`.")

    from PIL import Image

    if image_path:
        path = Path(image_path).expanduser().resolve()
        if not path.exists() or not path.is_file():
            raise DecodeInputError(f"Image path does not exist or is not a file: {path}")
        return Image.open(path)

    try:
        image_bytes = base64.b64decode(image_base64, validate=True)
    except Exception as exc:  # pragma: no cover - library-specific
        raise DecodeInputError("`image_base64` must be valid base64 data.") from exc

    try:
        return Image.open(BytesIO(image_bytes))
    except Exception as exc:  # pragma: no cover - library-specific
        raise DecodeInputError("Base64 payload is not a readable image.") from exc


def decode_barcodes(*, image_path: str | None = None, image_base64: str | None = None) -> list[BarcodeResult]:
    """Decode all barcodes in an image."""

    with _load_image(image_path=image_path, image_base64=image_base64) as image:
        import zxingcpp

        detections = zxingcpp.read_barcodes(image)

    results: list[BarcodeResult] = []
    for detection in detections:
        position = [{"x": point.x, "y": point.y} for point in detection.position]
        results.append(
            BarcodeResult(
                format=str(detection.format),
                text=detection.text,
                position=position,
            )
        )

    return results


def as_dict(results: list[BarcodeResult]) -> list[dict[str, Any]]:
    return [{"format": r.format, "text": r.text, "position": r.position} for r in results]
