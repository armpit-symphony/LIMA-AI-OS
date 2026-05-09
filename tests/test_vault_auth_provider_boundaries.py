"""Boundary tests for future Vault/Auth providers and adapters."""

from dataclasses import fields
from pathlib import Path


LIMA_ROOT = Path(__file__).resolve().parents[1] / "lima"

PROTECTED_PATHS = (
    "guardian",
    "contracts",
    "persistence",
    "services",
    "io",
    "adapters",
)

FORBIDDEN_IMPORT_STRINGS = (
    "app.crud",
    "app.models",
    "app.services",
    "backend.app",
    "from app ",
    "import app",
    "ChatUser",
    "app.api.routes.chat",
    "chat.routes",
    "websocket",
    "SPARKBOT_",
    "vault.db",
    "sqlmodel",
    "SQLModel",
    "Sparkbot",
    "sparkbot",
)

FORBIDDEN_PROVIDER_METHODS = {
    "get_secret",
    "decrypt",
    "encrypt",
    "read_value",
    "write_value",
    "return_secret",
    "verify_pin",
    "check_pin",
    "login",
    "authenticate_live",
    "open_live_session",
    "enforce",
    "execute",
    "bypass",
}

FORBIDDEN_SECRET_FIELD_NAMES = {
    "raw_secret",
    "secret_value",
    "plaintext",
    "password",
    "token",
    "api_key",
    "private_key",
    "credential",
    "decrypted_value",
    "cleartext",
    "value",
}


def _protected_python_files() -> list[Path]:
    files: list[Path] = []
    for relative_path in PROTECTED_PATHS:
        root = LIMA_ROOT / relative_path
        if root.exists():
            files.extend(sorted(root.rglob("*.py")))
    return files


def _public_callables(protocol: type) -> set[str]:
    return {
        name
        for name, value in protocol.__dict__.items()
        if not name.startswith("_") and callable(value)
    }


def test_vault_auth_provider_paths_do_not_import_sparkbot_internals() -> None:
    violations: list[str] = []
    for path in _protected_python_files():
        text = path.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_IMPORT_STRINGS:
            if forbidden in text:
                violations.append(f"{path.relative_to(LIMA_ROOT)} contains {forbidden!r}")

    assert violations == []


def test_vault_auth_protocols_do_not_expose_live_behavior_methods() -> None:
    from lima.contracts import (
        AuthProviderProtocol,
        BreakglassProviderProtocol,
        VaultProviderProtocol,
    )

    protocols = (
        AuthProviderProtocol,
        VaultProviderProtocol,
        BreakglassProviderProtocol,
    )

    violations = {
        protocol.__name__: sorted(
            _public_callables(protocol) & FORBIDDEN_PROVIDER_METHODS
        )
        for protocol in protocols
    }

    assert violations == {
        "AuthProviderProtocol": [],
        "VaultProviderProtocol": [],
        "BreakglassProviderProtocol": [],
    }


def test_vault_auth_dataclasses_do_not_expose_raw_secret_fields() -> None:
    from lima.contracts import (
        AuthActor,
        AuthContext,
        AuthDecision,
        AuthRequirement,
        BreakglassSessionRef,
        VaultAccessDecision,
        VaultAccessRequest,
        VaultSecretRef,
    )

    dataclasses = (
        VaultSecretRef,
        VaultAccessRequest,
        VaultAccessDecision,
        BreakglassSessionRef,
        AuthActor,
        AuthContext,
        AuthRequirement,
        AuthDecision,
    )
    violations = {
        dataclass_type.__name__: sorted(
            {field.name for field in fields(dataclass_type)}
            & FORBIDDEN_SECRET_FIELD_NAMES
        )
        for dataclass_type in dataclasses
    }

    assert violations == {
        "VaultSecretRef": [],
        "VaultAccessRequest": [],
        "VaultAccessDecision": [],
        "BreakglassSessionRef": [],
        "AuthActor": [],
        "AuthContext": [],
        "AuthRequirement": [],
        "AuthDecision": [],
    }
