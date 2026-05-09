"""Non-production adapter skeletons for LIMA-owned input boundaries."""

from .sparkbot_humaninput import (
    SparkbotChatInputPayload,
    SparkbotHumanInputAdapter,
    SparkbotMeetingInputPayload,
    SparkbotOperatorInputPayload,
    SparkbotVoiceInputPayload,
)

__all__ = [
    "SparkbotChatInputPayload",
    "SparkbotHumanInputAdapter",
    "SparkbotMeetingInputPayload",
    "SparkbotOperatorInputPayload",
    "SparkbotVoiceInputPayload",
]
