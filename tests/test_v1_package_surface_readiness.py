"""Package surface readiness tests for V1 governed dry-run runtime exports."""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
import pkgutil
import tomllib


def test_v1_governed_dry_run_modules_are_inside_lima_package_surface() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    assert pyproject["tool"]["setuptools"]["packages"] == [
        "lima",
        "lima.contracts",
        "lima.governed_kernel",
    ]

    module_names = {module.name for module in pkgutil.walk_packages(["lima"], prefix="lima.")}
    assert "lima.kernel.v1_governed_preflight" in module_names
    assert "lima.adapters.v1_shell_runtime_adapter" in module_names
    assert "lima.adapters.v1_consumer_evidence_envelope" in module_names

    for module_name in (
        "lima.kernel.v1_governed_preflight",
        "lima.adapters.v1_shell_runtime_adapter",
        "lima.adapters.v1_consumer_evidence_envelope",
    ):
        module = import_module(module_name)
        assert module.__name__ == module_name


def test_v1_governed_dry_run_public_exports_exist_on_package_surface() -> None:
    kernel = import_module("lima.kernel")
    adapters = import_module("lima.adapters")

    for export_name in (
        "V1GovernedPreflightResult",
        "run_v1_governed_preflight",
    ):
        assert export_name in kernel.__all__
        assert hasattr(kernel, export_name)

    for export_name in (
        "V1ConsumerEvidenceEnvelope",
        "V1ConsumerEvidenceEnvelopeError",
        "V1ShellRuntimeInput",
        "V1ShellGovernedRuntimeResponse",
        "run_v1_shell_governed_preflight",
        "build_v1_consumer_evidence_envelope",
    ):
        assert export_name in adapters.__all__
        assert hasattr(adapters, export_name)