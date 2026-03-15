from __future__ import annotations

import sys
import types

import pytest

from barcodes_reader_mcp.decoder import DecodeInputError, decode_barcodes


class _Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class _Detection:
    def __init__(self) -> None:
        self.format = "DataMatrix"
        self.text = "hello"
        self.position = [_Point(0, 0), _Point(10, 0), _Point(10, 10), _Point(0, 10)]


class _FakeImage:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_requires_exactly_one_input() -> None:
    with pytest.raises(DecodeInputError):
        decode_barcodes()


def test_decode_with_stubbed_dependencies(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("barcodes_reader_mcp.decoder._load_image", lambda **_: _FakeImage())

    fake_module = types.SimpleNamespace(read_barcodes=lambda img: [_Detection()])
    monkeypatch.setitem(sys.modules, "zxingcpp", fake_module)

    results = decode_barcodes(image_base64="Zm9v")

    assert len(results) == 1
    assert results[0].format == "DataMatrix"
    assert results[0].text == "hello"
    assert results[0].position[0] == {"x": 0, "y": 0}
