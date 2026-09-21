"""Reference MSR JSON schema validator; no network access is needed at runtime."""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator

SCHEMA_VERSION = "2.0.0"
SCHEMA_ID = "https://msrjson.org/schemas/msr-2.0.json"


@dataclass(frozen=True)
class ValidationError:
    """A deterministic, serializable schema validation error."""

    path: str
    message: str


class DuplicateKeyError(ValueError):
    """Raised when JSON contains an ambiguous duplicate object member."""


@dataclass(frozen=True)
class ValidationResult:
    """The outcome of validating one manifest."""

    errors: tuple[ValidationError, ...]

    @property
    def valid(self) -> bool:
        return not self.errors


def _schema() -> dict[str, Any]:
    payload = files("msr_validator").joinpath("schema", "msr-2.0.json").read_text(encoding="utf-8")
    schema = json.loads(payload, object_pairs_hook=_reject_duplicate_keys)
    if schema.get("$id") != SCHEMA_ID:
        raise RuntimeError("bundled schema does not have the canonical MSR JSON 2.0 identifier")
    Draft202012Validator.check_schema(schema)
    return schema


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON object member: {key!r}")
        result[key] = value
    return result


_VALIDATOR = Draft202012Validator(_schema())


def _load_manifest(manifest: Mapping[str, Any] | str | bytes | Path) -> Mapping[str, Any]:
    if isinstance(manifest, Mapping):
        return manifest
    if isinstance(manifest, Path):
        content = manifest.read_text(encoding="utf-8")
    elif isinstance(manifest, bytes):
        content = manifest.decode("utf-8")
    elif isinstance(manifest, str):
        content = manifest
    else:
        raise TypeError("manifest must be a mapping, JSON text, bytes, or pathlib.Path")
    loaded = json.loads(content, object_pairs_hook=_reject_duplicate_keys)
    if not isinstance(loaded, Mapping):
        raise ValueError("manifest root must be a JSON object")
    return loaded


def validate(
    manifest: Mapping[str, Any] | str | bytes | Path,
    *,
    schema_path: str | Path | None = None,
) -> ValidationResult:
    """Validate against pinned 2.0, or an explicit local draft schema."""

    data = _load_manifest(manifest)
    validator = _VALIDATOR
    if schema_path is not None:
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8"), object_pairs_hook=_reject_duplicate_keys)
        Draft202012Validator.check_schema(schema)
        if data.get("$schema") != schema.get("$id"):
            return ValidationResult((ValidationError("/$schema", "manifest $schema does not match selected schema $id"),))
        validator = Draft202012Validator(schema)
    errors = tuple(
        ValidationError(
            path="/" + "/".join(map(str, error.absolute_path)) if error.absolute_path else "/",
            message=error.message,
        )
        for error in sorted(validator.iter_errors(data), key=lambda error: list(error.absolute_path))
    )
    return ValidationResult(errors)
