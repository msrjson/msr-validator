import json
import pytest
from pathlib import Path

from msr_validator import SCHEMA_ID, SCHEMA_VERSION, validate


EXAMPLE = Path(__file__).parents[1] / "tests" / "fixtures" / "valid.json"


def test_reference_manifest_validates():
    result = validate(EXAMPLE)
    assert result.valid
    assert result.errors == ()
    assert SCHEMA_VERSION == "2.0.0"
    assert SCHEMA_ID == "https://msrjson.org/schemas/msr-2.0.json"


def test_unknown_property_is_rejected():
    manifest = json.loads(EXAMPLE.read_text())
    manifest["unexpected"] = True
    result = validate(manifest)
    assert not result.valid
    assert any("unexpected" in error.message for error in result.errors)


def test_duplicate_json_keys_are_rejected_before_schema_validation():
    raw = EXAMPLE.read_text().replace(
        '"name": "MSR JSON"', '"name": "tampered", "name": "MSR JSON"'
    )
    with pytest.raises(ValueError, match="duplicate JSON object member"):
        validate(raw)
