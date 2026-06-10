from __future__ import annotations

import ast
import pathlib


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FREEZE_DOC_PATH = REPO_ROOT / "docs" / "readiness" / "LIMA_PUBLIC_API_FREEZE_CANDIDATE.md"
KERNEL_INIT_PATH = REPO_ROOT / "lima" / "kernel" / "__init__.py"


def _freeze_text() -> str:
    return FREEZE_DOC_PATH.read_text(encoding="utf-8")


def _kernel_all_exports() -> tuple[str, ...]:
    module = ast.parse(KERNEL_INIT_PATH.read_text(encoding="utf-8"))
    for node in module.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    assert isinstance(node.value, ast.List)
                    exports: list[str] = []
                    for item in node.value.elts:
                        assert isinstance(item, ast.Constant)
                        assert isinstance(item.value, str)
                        exports.append(item.value)
                    return tuple(exports)
    raise AssertionError("lima.kernel.__all__ not found")


def test_public_api_freeze_candidate_doc_exists() -> None:
    assert FREEZE_DOC_PATH.exists()
    assert KERNEL_INIT_PATH.exists()


def test_candidate_names_intended_public_import_paths() -> None:
    text = _freeze_text()

    assert "`from lima.kernel import <exported-name>`" in text
    assert "`from lima.kernel import LimaKernel`" in text
    assert "`import lima` is allowed for package import proof." in text
    assert "top-level `lima` is not a runtime consumer API" in text


def test_candidate_documents_all_current_lima_kernel_exports() -> None:
    text = _freeze_text()

    for exported_name in _kernel_all_exports():
        assert f"`{exported_name}`" in text


def test_candidate_contains_dry_run_and_non_executing_language() -> None:
    text = _freeze_text()

    for required in (
        "dry-run-only evaluator",
        "`executable: false`",
        "`execution_allowed: false`",
        "`side_effects_allowed: false`",
        "`dispatch_allowed: false`",
        "`persistence_allowed: false`",
        "`dry_run: true`",
        "`model_calls_executed: false`",
        "`physical_world_executed: false`",
    ):
        assert required in text


def test_candidate_names_all_required_consumer_families() -> None:
    text = _freeze_text()

    for consumer in ("Sparkbot", "Arc Bot", "LIMA Robo OS", "LIMA Office", "future shells"):
        assert consumer in text


def test_candidate_forbids_runtime_integration_and_live_surfaces() -> None:
    text = _freeze_text()

    for forbidden in (
        "runtime integration",
        "consumer wiring",
        "provider/model routing",
        "model calls",
        "real Guardian authority",
        "approval enforcement",
        "HumanInput bridge activation",
        "storage/persistence runtime",
        "browser/file/network actions",
        "external sends",
        "live discovery",
        "scanning",
        "pairing",
        "credential use",
        "device control",
        "robotics",
        "drones",
        "physical-world behavior",
    ):
        assert forbidden in text


def test_candidate_references_package_proof_prerequisites() -> None:
    text = _freeze_text()

    assert "controlled build-backend verification complete" in text
    assert "wheel/sdist proof complete outside the repository" in text
    assert "isolated install/import proof complete with `--no-index`" in text
    assert "package proof ledger complete" in text


def test_static_coverage_does_not_import_consumer_repos_or_execute_package_work() -> None:
    source = pathlib.Path(__file__).read_text(encoding="utf-8")

    forbidden = (
        "Sparkbot" + "_shell",
        "Arc" + "-Bot-shell",
        "LIMA" + "-Office",
        "import " + "subprocess",
        "import " + "socket",
        "import " + "threading",
        "pip " + "install",
        "python -m " + "build",
    )
    for item in forbidden:
        assert item not in source


def test_candidate_recommends_independent_audit_next() -> None:
    text = _freeze_text()

    assert "`static-lima-public-api-freeze-candidate-coverage`" in text
