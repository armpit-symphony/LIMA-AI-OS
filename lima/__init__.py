"""LIMA Runtime governed-kernel release candidate package."""

from .release import PACKAGE_VERSION, get_release_candidate_manifest

__version__ = PACKAGE_VERSION

__all__ = ["contracts"]
