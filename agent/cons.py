from model_utils import Choices

CREATOR_GROUP_NAME = "Creator"
PARTICIPANT_GROUP_NAME = "Participant"

CREATOR_GROUP_ID = 1
PARTICIPANT_GROUP_ID = 2

GROUPS = Choices((1, "creator", "Creator"), (2, "participant", "Participant"))
