from enum import Enum


class State(Enum):
    OPENED = 'opened'
    CLOSED = 'closed'
    FLAGGED = 'flagged'
    QUESTIONED = 'questioned'
