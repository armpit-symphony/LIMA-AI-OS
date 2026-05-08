"""Import-boundary checks for future lima.guardian code."""

from pathlib import Path


FORBIDDEN_GUARDIAN_IMPORT_STRINGS = (
    "app.crud",
    "app.models",
    "app.services",
    "backend.app",
)


def test_lima_guardian_does_not_import_sparkbot_backend_modules() -> None:
    guardian_root = Path(__file__).resolve().parents[1] / "lima" / "guardian"
    assert guardian_root.exists()

    violations: list[str] = []
    for path in sorted(guardian_root.rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_GUARDIAN_IMPORT_STRINGS:
            if forbidden in text:
                violations.append(f"{path.relative_to(guardian_root)} contains {forbidden!r}")

    assert violations == []
