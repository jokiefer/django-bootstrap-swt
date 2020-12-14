from enum import Enum


class ModalSizeEnum(Enum):
    LARGE = "modal-lg"
    SMALL = "modal-sm"


class ButtonColorEnum(Enum):
    PRIMARY = "btn-primary"
    SECONDARY = "btn-secondary"
    INFO = "btn-info"
    SUCCESS = "btn-success"
    WARNING = "btn-warning"
    DANGER = "btn-danger"
    PRIMARY_OUTLINE = "btn-outline-primary"
    SECONDARY_OUTLINE = "btn-outline-secondary"
    INFO_OUTLINE = "btn-outline-info"
    SUCCESS_OUTLINE = "btn-outline-success"
    WARNING_OUTLINE = "btn-outline-warning"
    DANGER_OUTLINE = "btn-outline-danger"


class ButtonSizeEnum(Enum):
    SMALL = "btn-sm"
    LARGE = "btn-lg"


class LinkColorEnum(Enum):
    PRIMARY = "text-primary"
    SECONDARY = "text-secondary"
    INFO = "text-info"
    SUCCESS = "text-success"
    WARNING = "text-warning"
    DANGER = "text-danger"


class TooltipPlacementEnum(Enum):
    LEFT = "left"
    TOP = "top"
    RIGHT = "right"
    BOTTOM = "bottom"


class ProgressColorEnum(Enum):
    PRIMARY = None
    SUCCESS = "bg-success"
    INFO = "bg-info"
    WARNING = "bg-warning"
    DANGER = "bg-danger"


class BadgeColorEnum(Enum):
    PRIMARY = "badge-primary"
    SECONDARY = "badge-secondary"
    SUCCESS = "badge-success"
    DANGER = "badge-danger"
    WARNING = "badge-warning"
    INFO = "badge-info"
    LIGHT = "badge-light"
    DARK = "badge-dark"
