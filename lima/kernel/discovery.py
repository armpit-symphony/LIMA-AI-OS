"""Deterministic simulated discovery adapter for the non-executing kernel lane."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Final, Mapping


SIMULATED_CONNECTION_TYPES: Final[frozenset[str]] = frozenset({"wifi", "ble", "lan", "iot"})
SIMULATED_DISCOVERY_MODES: Final[frozenset[str]] = frozenset(
    {"simulated", "simulation", "dry_run", "dry-run", "fixture", "synthetic"}
)
LIVE_DISCOVERY_MODES: Final[frozenset[str]] = frozenset(
    {
        "authenticated",
        "connect",
        "connection",
        "discover",
        "discovery",
        "enumerate",
        "live",
        "local",
        "pair",
        "pairing",
        "probe",
        "scan",
    }
)
CONNECTION_MARKERS: Final[frozenset[str]] = frozenset(
    {"auto-connect", "autoconnect", "connect", "connection", "open session", "session"}
)
PAIRING_MARKERS: Final[frozenset[str]] = frozenset({"pair", "pairing"})
CREDENTIAL_MARKERS: Final[frozenset[str]] = frozenset(
    {
        "api_key",
        "apikey",
        "authorization",
        "credential",
        "credentials",
        "header",
        "key",
        "password",
        "pin",
        "secret",
        "token",
    }
)
PHYSICAL_MARKERS: Final[frozenset[str]] = frozenset(
    {
        "actuate",
        "actuator",
        "device_control",
        "drone",
        "hardware",
        "motor",
        "move",
        "physical",
        "robot",
        "robotics",
    }
)
SYNTHETIC_SURFACE_FIXTURES: Final[dict[str, tuple[str, str]]] = {
    "wifi": ("simulated-wifi-preview", "Simulated WiFi preview"),
    "ble": ("simulated-ble-preview", "Simulated BLE preview"),
    "lan": ("simulated-lan-preview", "Simulated LAN preview"),
    "iot": ("simulated-iot-preview", "Simulated IoT preview"),
}


@dataclass(frozen=True)
class DiscoveryAdapterManifest:
    """Static manifest for the simulated adapter."""

    adapter_id: str = "simulated-discovery-adapter"
    adapter_type: str = "simulated_discovery_adapter"
    adapter_version: str = "0.1"
    supported_connection_types: tuple[str, ...] = ("wifi", "ble", "lan", "iot")
    supported_discovery_modes: tuple[str, ...] = ("simulated", "simulation", "dry_run")
    required_capabilities: tuple[str, ...] = ("connection_discovery",)
    supports_simulation: bool = True
    supports_live_discovery: bool = False
    supports_connection_attempt: bool = False
    supports_pairing: bool = False
    supports_credentials: bool = False
    supports_physical_world: bool = False
    risk_tier: str = "low_simulated_only"
    requires_guardian: bool = True
    requires_human_approval: bool = False
    redaction_policy: tuple[str, ...] = (
        "no_passwords",
        "no_tokens",
        "no_credentials",
        "no_pairing_codes",
        "no_raw_scan_dumps",
        "no_physical_location",
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DiscoveryAdapterRequest:
    """Synthetic request metadata accepted by the simulated adapter."""

    request_id: str
    actor_id: str
    shell_id: str
    session_id: str | None = None
    source_surface: Mapping[str, Any] = field(default_factory=dict)
    target_hint: str | None = None
    connection_type: str = "wifi"
    discovery_mode: str = "simulated"
    dry_run: bool = True
    simulated_only: bool = True
    credential_ref: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DiscoveryAdapterSurface:
    """Synthetic, inert surface returned by the simulated adapter."""

    surface_id: str
    connection_type: str
    redacted_label: str
    discovery_mode: str = "simulated"
    synthetic: bool = True
    inert: bool = True
    simulated: bool = True
    connectable: bool = False
    controllable: bool = False
    physical_world: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DiscoveryAdapterEvent:
    """Redacted in-memory event-style metadata returned with adapter results."""

    event_id: str
    request_id: str
    adapter_id: str
    event_type: str
    state: str
    redacted_summary: str
    durable: bool = False
    in_memory_only: bool = True
    contains_secret: bool = False
    contains_raw_scan_dump: bool = False
    contains_physical_location: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DiscoveryAdapterResult:
    """Dry-run-only simulated discovery adapter result."""

    request_id: str
    adapter_id: str
    adapter_type: str
    state: str
    redacted_summary: str
    event_refs: tuple[str, ...]
    surfaces: tuple[DiscoveryAdapterSurface, ...] = ()
    blocked_reason: str | None = None
    dry_run: bool = True
    simulated_only: bool = True
    executable: bool = False
    execution_allowed: bool = False
    side_effects_allowed: bool = False
    dispatch_allowed: bool = False
    persistence_allowed: bool = False
    live_discovery_executed: bool = False
    connection_attempted: bool = False
    pairing_attempted: bool = False
    credentials_used: bool = False
    session_opened: bool = False
    device_control_executed: bool = False
    physical_world_executed: bool = False
    events: tuple[DiscoveryAdapterEvent, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class SimulatedDiscoveryAdapter:
    """In-process simulated adapter that never performs discovery or connection work."""

    def __init__(self, manifest: DiscoveryAdapterManifest | None = None) -> None:
        self._manifest = manifest or DiscoveryAdapterManifest()

    @property
    def manifest(self) -> DiscoveryAdapterManifest:
        return self._manifest

    def simulate(
        self, request: DiscoveryAdapterRequest | Mapping[str, Any]
    ) -> DiscoveryAdapterResult:
        adapter_request = _coerce_request(request)
        blocked_reason = _blocked_reason(adapter_request)
        if blocked_reason:
            return self._blocked(adapter_request, blocked_reason)

        connection_type = _normalized_connection_type(adapter_request.connection_type)
        surface_id, label = SYNTHETIC_SURFACE_FIXTURES[connection_type]
        surface = DiscoveryAdapterSurface(
            surface_id=surface_id,
            connection_type=connection_type,
            redacted_label=label,
            metadata={
                "synthetic_fixture": True,
                "no_live_discovery": True,
                "no_connection_attempt": True,
            },
        )
        event_refs = ("discovery-adapter-event:1", "discovery-adapter-event:2")
        events = (
            _event(
                event_refs[0],
                adapter_request,
                self._manifest.adapter_id,
                "discovery_adapter_simulation_requested",
                "proposed",
                f"simulated_discovery:{connection_type}:requested",
            ),
            _event(
                event_refs[1],
                adapter_request,
                self._manifest.adapter_id,
                "discovery_adapter_simulation_completed",
                "proposed",
                f"simulated_discovery:{connection_type}:synthetic_surfaces_returned",
            ),
        )
        return DiscoveryAdapterResult(
            request_id=adapter_request.request_id,
            adapter_id=self._manifest.adapter_id,
            adapter_type=self._manifest.adapter_type,
            state="proposed",
            redacted_summary=f"simulated_discovery:{connection_type}:proposed",
            event_refs=event_refs,
            surfaces=(surface,),
            events=events,
            metadata={
                "deterministic": True,
                "synthetic_surfaces_only": True,
                "adapter_manifest_version": self._manifest.adapter_version,
            },
        )

    def _blocked(
        self, request: DiscoveryAdapterRequest, blocked_reason: str
    ) -> DiscoveryAdapterResult:
        event_refs = ("discovery-adapter-event:1", "discovery-adapter-event:2")
        events = (
            _event(
                event_refs[0],
                request,
                self._manifest.adapter_id,
                "discovery_adapter_simulation_requested",
                "blocked",
                "simulated_discovery:block_requested",
            ),
            _event(
                event_refs[1],
                request,
                self._manifest.adapter_id,
                _blocked_event_type(blocked_reason),
                "blocked",
                f"simulated_discovery:blocked:{blocked_reason}",
            ),
        )
        return DiscoveryAdapterResult(
            request_id=request.request_id,
            adapter_id=self._manifest.adapter_id,
            adapter_type=self._manifest.adapter_type,
            state="blocked",
            redacted_summary=f"simulated_discovery:blocked:{blocked_reason}",
            event_refs=event_refs,
            blocked_reason=blocked_reason,
            events=events,
            metadata={
                "deterministic": True,
                "synthetic_surfaces_only": True,
                "adapter_manifest_version": self._manifest.adapter_version,
            },
        )


def _coerce_request(request: DiscoveryAdapterRequest | Mapping[str, Any]) -> DiscoveryAdapterRequest:
    if isinstance(request, DiscoveryAdapterRequest):
        return request
    if not isinstance(request, Mapping):
        raise TypeError("request must be DiscoveryAdapterRequest or mapping")
    return DiscoveryAdapterRequest(
        request_id=_non_empty_text(request.get("request_id"), "request_id"),
        actor_id=_non_empty_text(request.get("actor_id"), "actor_id"),
        shell_id=_non_empty_text(request.get("shell_id"), "shell_id"),
        session_id=request.get("session_id") if isinstance(request.get("session_id"), str) else None,
        source_surface=_mapping(request.get("source_surface", {}), "source_surface"),
        target_hint=request.get("target_hint") if isinstance(request.get("target_hint"), str) else None,
        connection_type=str(request.get("connection_type", "wifi")),
        discovery_mode=str(request.get("discovery_mode", "simulated")),
        dry_run=request.get("dry_run", True) is True,
        simulated_only=request.get("simulated_only", True) is True,
        credential_ref=(
            request.get("credential_ref") if isinstance(request.get("credential_ref"), str) else None
        ),
        metadata=_mapping(request.get("metadata", {}), "metadata"),
    )


def _blocked_reason(request: DiscoveryAdapterRequest) -> str | None:
    if request.dry_run is not True:
        return "dry_run_required"
    if request.simulated_only is not True:
        return "simulated_only_required"
    mode = _normalized_mode(request.discovery_mode)
    if mode in LIVE_DISCOVERY_MODES or mode not in SIMULATED_DISCOVERY_MODES:
        return "live_discovery_mode_blocked"
    if request.credential_ref is not None:
        return "credential_ref_not_supported"
    if _contains_marker(request.metadata, CREDENTIAL_MARKERS) or _contains_marker(
        request.target_hint, CREDENTIAL_MARKERS
    ):
        return "raw_credential_like_field_blocked"
    if _contains_marker(request.metadata, CONNECTION_MARKERS) or _contains_marker(
        request.target_hint, CONNECTION_MARKERS
    ):
        return "connection_attempt_blocked"
    if _contains_marker(request.metadata, PAIRING_MARKERS) or _contains_marker(
        request.target_hint, PAIRING_MARKERS
    ):
        return "pairing_blocked"
    if _contains_marker(request.metadata, PHYSICAL_MARKERS) or _contains_marker(
        request.target_hint, PHYSICAL_MARKERS
    ):
        return "physical_world_request_blocked"
    connection_type = _normalized_connection_type(request.connection_type)
    if connection_type not in SIMULATED_CONNECTION_TYPES:
        return "unsupported_simulated_connection_type"
    return None


def _blocked_event_type(blocked_reason: str) -> str:
    if "credential" in blocked_reason:
        return "discovery_adapter_redaction_failed"
    if "connection" in blocked_reason or "live_discovery" in blocked_reason:
        return "discovery_adapter_connection_blocked"
    if "pairing" in blocked_reason:
        return "discovery_adapter_pairing_blocked"
    if "physical" in blocked_reason:
        return "discovery_adapter_physical_endpoint_blocked"
    return "discovery_adapter_live_discovery_blocked"


def _event(
    event_id: str,
    request: DiscoveryAdapterRequest,
    adapter_id: str,
    event_type: str,
    state: str,
    redacted_summary: str,
) -> DiscoveryAdapterEvent:
    return DiscoveryAdapterEvent(
        event_id=event_id,
        request_id=request.request_id,
        adapter_id=adapter_id,
        event_type=event_type,
        state=state,
        redacted_summary=redacted_summary,
        metadata={
            "source_surface": _safe_surface_name(request.source_surface),
            "in_memory_only": True,
        },
    )


def _normalized_connection_type(value: str) -> str:
    return value.strip().lower().replace("-", "_")


def _normalized_mode(value: str) -> str:
    return value.strip().lower().replace(" ", "_")


def _safe_surface_name(surface: Mapping[str, Any]) -> str:
    value = surface.get("surface") or surface.get("source") or "unknown"
    if not isinstance(value, str) or not value.strip():
        return "unknown"
    return value.strip()[:80]


def _contains_marker(value: Any, markers: frozenset[str]) -> bool:
    if isinstance(value, Mapping):
        return any(
            _contains_marker(nested_key, markers) or _contains_marker(nested_value, markers)
            for nested_key, nested_value in value.items()
        )
    if isinstance(value, (list, tuple, set, frozenset)):
        return any(_contains_marker(item, markers) for item in value)
    if not isinstance(value, str):
        return False
    folded = value.strip().lower()
    words = tuple(
        part for part in "".join(char.lower() if char.isalnum() else " " for char in folded).split()
    )
    joined = "".join(words)
    return any(marker in folded or marker in words or marker == joined for marker in markers)


def _non_empty_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field_name} must be a mapping")
    return dict(value)
