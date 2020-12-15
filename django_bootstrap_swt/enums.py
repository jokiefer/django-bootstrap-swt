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


class BackgroundColorEnum(Enum):
    PRIMARY = "bg-primary"
    SECONDARY = "bg-secondary"
    SUCCESS = "bg-success"
    DANGER = "bg-danger"
    WARNING = "bg-warning"
    INFO = "bg-info"
    LIGHT = "bg-light"
    DARK = "bg-dark"
    WHITE = "bg-white"


class TextColorEnum(Enum):
    PRIMARY = "text-primary"
    SECONDARY = "text-secondary"
    SUCCESS = "text-success"
    DANGER = "text-danger"
    WARNING = "text-warning"
    INFO = "text-info"
    LIGHT = "text-light"
    DARK = "text-dark"
    MUTED = "text-muted"
    WHITE = "text-white"


class BorderColorEnum(Enum):
    PRIMARY = "border-primary"
    SECONDARY = "border-secondary"
    SUCCESS = "border-success"
    DANGER = "border-danger"
    WARNING = "border-warning"
    INFO = "border-info"
    LIGHT = "border-light"
    DARK = "border-dark"
    WHITE = "border-white"


class DataToggleEnum(Enum):
    COLLAPSE = "collapse"
    MODAL = "modal"
