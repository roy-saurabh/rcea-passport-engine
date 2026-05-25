from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .exceptions import (
    LimitationPropagationError,
    ReproducibilityError,
    SchemaValidationError,
    SuppressionLogError,
)
from .models import EvidenceFinding, EvidencePassport, Rule

try:
    import jsonschema
    _HAS_JSONSCHEMA = True
except ImportError:  # pragma: no cover
    _HAS_JSONSCHEMA = False


def validate_json_schema(instance: Any, schema_path: str | Path) -> None:
    if not _HAS_JSONSCHEMA:
        return
    with open(schema_path) as f:
        schema = json.load(f)
    try:
        jsonschema.validate(instance=instance, schema=schema)
    except jsonschema.ValidationError as e:
        raise SchemaValidationError(str(e)) from e


def validate_passport_schema(
    passport: EvidencePassport,
    schemas_dir: str | Path = "schemas",
) -> None:
    schemas_dir = Path(schemas_dir)
    data = json.loads(passport.model_dump_json())
    validate_json_schema(data, schemas_dir / "passport.schema.json")


def validate_limitation_propagation(
    passport: EvidencePassport,
    finding: EvidenceFinding,
    rule: Rule,
) -> None:
    if rule.limitation_propagation_required:
        for lim in finding.limitations:
            if lim not in passport.limitations:
                raise LimitationPropagationError(
                    f"Material limitation not propagated: '{lim}'"
                )


def validate_suppression_logging(passport: EvidencePassport, rule: Rule) -> None:
    logged_fields = {log.field for log in passport.suppression_log}
    for field in rule.suppressed_fields:
        if field not in logged_fields:
            raise SuppressionLogError(
                f"Suppressed field '{field}' has no suppression log entry"
            )


def _passport_hash(passport: EvidencePassport) -> str:
    data = json.loads(passport.model_dump_json())
    blob = json.dumps(data, sort_keys=True, default=str).encode()
    return hashlib.sha256(blob).hexdigest()


def validate_passport_reproducibility(
    passport_a: EvidencePassport,
    passport_b: EvidencePassport,
) -> None:
    ha = _passport_hash(passport_a)
    hb = _passport_hash(passport_b)
    if ha != hb:
        raise ReproducibilityError(f"Passport hashes differ: {ha} vs {hb}")
