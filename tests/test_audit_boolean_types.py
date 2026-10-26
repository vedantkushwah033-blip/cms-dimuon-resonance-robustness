"""Regression tests for strict JSON boolean validation in parity audits."""
from __future__ import annotations

import pytest

from scripts.audit_baseline_metadata import _boolean_matches


@pytest.mark.parametrize("value", [True])
def test_accepts_expected_json_boolean(value: bool) -> None:
    assert _boolean_matches(value, True)


@pytest.mark.parametrize("value", [1, "true", "True", None, 1.0, []])
def test_rejects_non_boolean_values_that_might_look_truthy(value: object) -> None:
    assert not _boolean_matches(value, True)


def test_false_is_not_true() -> None:
    assert not _boolean_matches(False, True)


def test_false_matches_false_only_as_a_boolean() -> None:
    assert _boolean_matches(False, False)
    assert not _boolean_matches(0, False)
