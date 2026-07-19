"""Prove the v0.1 governed-kernel wheel from a clean consumer environment."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import venv
import zipfile


EXPECTED_NAME = "lima-runtime"
EXPECTED_VERSION = "0.1.0rc1"
FORBIDDEN_WHEEL_PREFIXES = (
    "lima/adapters/",
    "lima/guardian/",
    "lima/harness/",
    "lima/io/",
    "lima/kernel/",
    "lima/packs/",
    "lima/persistence/",
    "lima/services/",
    "lima/shells/",
    "lima/spine/",
)


def _wheel_metadata(wheel: Path) -> tuple[str, str, tuple[str, ...], tuple[str, ...]]:
    with zipfile.ZipFile(wheel) as archive:
        members = tuple(archive.namelist())
        metadata_paths = [
            name for name in members if name.endswith(".dist-info/METADATA")
        ]
        if len(metadata_paths) != 1:
            raise AssertionError("wheel must contain exactly one METADATA file")
        metadata = archive.read(metadata_paths[0]).decode("utf-8")

    fields: dict[str, list[str]] = {}
    for line in metadata.splitlines():
        if ": " not in line:
            continue
        key, value = line.split(": ", 1)
        fields.setdefault(key, []).append(value)
    return (
        fields.get("Name", [""])[0],
        fields.get("Version", [""])[0],
        tuple(fields.get("Requires-Dist", [])),
        members,
    )


def _consumer_program() -> str:
    return textwrap.dedent(
        """
        import importlib.metadata
        import importlib.util
        import json
        import socket

        original_connect = socket.socket.connect

        def block_network(*args, **kwargs):
            raise AssertionError("network access is outside the v0.1 RC boundary")

        socket.socket.connect = block_network

        import lima
        from lima.runtime import run_governed_request

        assert importlib.metadata.version("lima-runtime") == "0.1.0rc1"
        assert lima.__version__ == "0.1.0rc1"
        manifest = lima.get_release_candidate_manifest()
        assert manifest["supported_entrypoints"] == [
            "lima.runtime.run_governed_request"
        ]
        assert manifest["supported_consumers"] == ["sparkbot", "arc-bot"]
        assert manifest["execution_allowed"] is False
        assert manifest["side_effects_allowed"] is False
        assert manifest["production_ready"] is False
        excluded_packages = (
            "lima.adapters",
            "lima.guardian",
            "lima.harness",
            "lima.io",
            "lima.kernel",
            "lima.packs",
            "lima.persistence",
            "lima.services",
            "lima.shells",
            "lima.spine",
        )
        for package in excluded_packages:
            assert importlib.util.find_spec(package) is None

        requests = (
            {
                "request_id": "sparkbot-rc-install-proof",
                "consumer": "sparkbot",
                "surface": "decision_preview",
                "actor_id": "consumer-proof",
                "normalized_request": {"intent": "preview LIMA status"},
                "requested_action": "preview status",
                "action_category": "preview",
                "tool_name": "sparkbot_decision_preview",
            },
            {
                "request_id": "arc-rc-install-proof",
                "consumer": "arc-bot",
                "surface": "governed_preflight",
                "actor_id": "consumer-proof",
                "normalized_request": {"intent": "preview Arc status"},
                "requested_action": "preview status",
                "action_category": "status",
                "tool_name": "arc_status_preview",
            },
        )
        decisions = [run_governed_request(request) for request in requests]
        for decision in decisions:
            assert decision.status == "allowed_dry_run"
            assert decision.executable is False
            assert decision.execution_allowed is False
            assert decision.side_effects_allowed is False
            assert decision.audit_event.execution_allowed is False
            assert decision.audit_event.side_effects_allowed is False

        blocked_categories = (
            "provider_call",
            "model_call",
            "tool_execution",
            "connector_call",
            "browser_network",
            "physical_world",
        )
        for index, category in enumerate(blocked_categories):
            decision = run_governed_request(
                {
                    "request_id": f"blocked-{index}",
                    "consumer": "consumer-proof",
                    "surface": "release_candidate",
                    "actor_id": "consumer-proof",
                    "normalized_request": {"intent": category},
                    "requested_action": category,
                    "action_category": category,
                    "tool_name": None,
                }
            )
            assert decision.status == "denied"
            assert decision.allowed is False
            assert decision.execution_allowed is False
            assert decision.side_effects_allowed is False

        socket.socket.connect = original_connect
        print(
            json.dumps(
                {
                    "installed_version": lima.__version__,
                    "consumers": [decision.consumer for decision in decisions],
                    "decision_statuses": [decision.status for decision in decisions],
                    "blocked_categories": list(blocked_categories),
                    "network_calls": 0,
                    "provider_calls": 0,
                    "tool_calls": 0,
                    "connector_calls": 0,
                    "robotics_calls": 0,
                    "execution_allowed": False,
                    "side_effects_allowed": False,
                },
                sort_keys=True,
            )
        )
        """
    )


def prove(wheel: Path, second_wheel: Path | None = None) -> dict[str, object]:
    wheel = wheel.resolve()
    if not wheel.is_file():
        raise FileNotFoundError(wheel)

    name, version, requirements, members = _wheel_metadata(wheel)
    if name != EXPECTED_NAME:
        raise AssertionError(f"unexpected wheel name: {name}")
    if version != EXPECTED_VERSION:
        raise AssertionError(f"unexpected wheel version: {version}")
    if requirements:
        raise AssertionError(f"runtime dependencies are not allowed: {requirements}")

    unexpected_members = sorted(
        member
        for member in members
        if member.startswith(FORBIDDEN_WHEEL_PREFIXES)
    )
    if unexpected_members:
        raise AssertionError(f"forbidden wheel members: {unexpected_members}")
    wheel_sha256 = hashlib.sha256(wheel.read_bytes()).hexdigest()
    second_wheel_sha256: str | None = None
    if second_wheel is not None:
        second_wheel = second_wheel.resolve()
        if not second_wheel.is_file():
            raise FileNotFoundError(second_wheel)
        second_wheel_sha256 = hashlib.sha256(second_wheel.read_bytes()).hexdigest()
        if second_wheel_sha256 != wheel_sha256:
            raise AssertionError(
                "fixed-epoch release-candidate wheel builds are not deterministic"
            )

    with tempfile.TemporaryDirectory(prefix="lima-v0-1-rc-proof-") as temp_dir:
        temp = Path(temp_dir)
        environment = temp / "consumer-venv"
        venv.EnvBuilder(with_pip=True, clear=True).create(environment)
        python = environment / (
            "Scripts/python.exe" if os.name == "nt" else "bin/python"
        )
        subprocess.run(
            [
                str(python),
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                "--no-deps",
                str(wheel),
            ],
            cwd=temp,
            check=True,
        )
        child_environment = dict(os.environ)
        child_environment.pop("PYTHONPATH", None)
        completed = subprocess.run(
            [str(python), "-I", "-c", _consumer_program()],
            cwd=temp,
            env=child_environment,
            check=True,
            capture_output=True,
            text=True,
        )

    consumer_evidence = json.loads(completed.stdout.strip())
    return {
        "wheel": wheel.name,
        "wheel_sha256": wheel_sha256,
        "second_wheel_sha256": second_wheel_sha256,
        "deterministic_second_build": second_wheel_sha256 == wheel_sha256,
        "metadata_name": name,
        "metadata_version": version,
        "runtime_dependencies": list(requirements),
        "clean_install": True,
        "consumer_evidence": consumer_evidence,
        "forbidden_wheel_members": unexpected_members,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wheel", type=Path, required=True)
    parser.add_argument("--second-wheel", type=Path)
    arguments = parser.parse_args()
    print(json.dumps(prove(arguments.wheel, arguments.second_wheel), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
