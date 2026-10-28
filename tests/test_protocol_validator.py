import subprocess
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "scripts" / "validate_confirmatory_protocol.py"
DRAFT = REPO_ROOT / "configs" / "confirmatory_global_calibration_protocol.yaml"


def valid_protocol():
    return {
        "protocol_version": "1.0",
        "status": "frozen",
        "research_question": "Does the full procedure control its global null rejection rate?",
        "estimand": {
            "name": "global_null_rejection_probability",
            "definition": "P_H0(T_max >= c) for the complete frozen procedure",
            "nominal_alpha": 0.05,
        },
        "analysis": {
            "mass_range_GeV": [10.0, 80.0],
            "histogram_bins": 700,
            "local_test_statistic": "prespecified one-sided likelihood-ratio statistic",
            "global_statistic": "maximum local statistic across all declared scan positions",
            "scan_windows": [{"width_GeV": 2.0, "step_GeV": 0.5}],
            "likelihood": "extended binned Poisson likelihood",
            "nuisance_parameter_policy": "profile all declared nuisance parameters",
            "fit_range_policy": "fit over the full declared mass range",
        },
        "background_models": [
            {
                "id": "model_a",
                "functional_form": "declared smooth family A",
                "parameter_bounds": {"p1": [0.1, 10.0]},
                "role": "fixed comparator",
            }
        ],
        "model_selection": {
            "enabled": False,
            "algorithm": "none",
            "tie_breaking": "not-applicable",
        },
        "generators": {
            "development": ["dev_a"],
            "calibration": ["cal_a"],
            "held_out_evaluation": ["heldout_b"],
            "held_out_outside_candidate_family": True,
        },
        "calibration": {
            "threshold_method": "empirical quantile of calibration maximum-statistic distribution",
            "quantile_convention": "nearest-rank ceiling convention, specified before generation",
            "calibration_replicates": 10000,
            "evaluation_replicates_per_scenario": 10000,
            "confidence_interval": "two-sided Clopper-Pearson exact binomial interval",
            "primary_comparison": "difference in held-out global rejection rates versus fixed comparator",
        },
        "failure_policy": {
            "definition": "fit does not converge or returns invalid likelihood",
            "primary_handling": "count unusable replicates separately and apply the prespecified conservative rule",
            "sensitivity_analysis": "report bounds under alternative failure handling",
        },
        "randomness": {
            "seed_strategy": "fixed recorded seeds per partition and scenario",
            "independent_streams_for_partitions": True,
        },
        "artifacts": {
            "per_replicate_schema": "versioned JSONL schema",
            "environment_lock": "hash-pinned requirements file",
            "manifest": "input, config, code, seed, and output manifest",
            "output_checksums": "SHA-256 for all final artifacts",
        },
        "gates": {
            "real_data_baseline_parity": "passed",
            "literature_novelty_review": "completed",
            "expert_protocol_review": "completed",
            "confirmatory_execution_authorized": True,
        },
    }


def run_validator(path):
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(path)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_current_draft_fails_closed():
    result = run_validator(DRAFT)
    assert result.returncode == 2
    assert "BLOCKED:" in result.stdout
    assert "status must be 'frozen'" in result.stdout
    assert "real_data_baseline_parity" in result.stdout


def test_complete_protocol_passes_structural_gate(tmp_path):
    protocol_path = tmp_path / "valid_protocol.yaml"
    protocol_path.write_text(yaml.safe_dump(valid_protocol(), sort_keys=False), encoding="utf-8")

    result = run_validator(protocol_path)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "STRUCTURAL GATE PASSED" in result.stdout


def test_overlapping_generator_partitions_are_rejected(tmp_path):
    protocol = valid_protocol()
    protocol["generators"]["held_out_evaluation"] = ["cal_a"]
    protocol_path = tmp_path / "overlap_protocol.yaml"
    protocol_path.write_text(yaml.safe_dump(protocol, sort_keys=False), encoding="utf-8")

    result = run_validator(protocol_path)

    assert result.returncode == 2
    assert "generator partitions calibration and held_out_evaluation overlap" in result.stdout
