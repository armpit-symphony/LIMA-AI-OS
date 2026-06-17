"""Non-production adapter skeletons for LIMA-owned input boundaries."""

from .sparkbot_humaninput import (
    SparkbotChatInputPayload,
    SparkbotHumanInputAdapter,
    SparkbotMeetingInputPayload,
    SparkbotOperatorInputPayload,
    SparkbotVoiceInputPayload,
)
from .v1_consumer_integration_compatibility import (
    V1ConsumerIntegrationCompatibilityError,
    validate_v1_consumer_integration_compatibility_freeze,
)

__all__ = [
    "SparkbotChatInputPayload",
    "SparkbotHumanInputAdapter",
    "SparkbotMeetingInputPayload",
    "SparkbotOperatorInputPayload",
    "SparkbotVoiceInputPayload",
    "V1ConsumerIntegrationCompatibilityError",
    "validate_v1_consumer_integration_compatibility_freeze",
]
