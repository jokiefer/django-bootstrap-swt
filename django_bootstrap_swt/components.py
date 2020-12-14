import uuid
from django.contrib.gis.geos import Polygon
from django.template.loader import render_to_string
from django_bootstrap_swt.enums import ButtonColorEnum, TooltipPlacementEnum, ProgressColorEnum, BadgeColorEnum, \
    LinkColorEnum, ButtonSizeEnum, ModalSizeEnum


PATH_TO_TEMPLATES = "django_bootstrap_swt/components/"


class BootstrapComponent:
    template_name = None

    def __str__(self) -> str:
        return self.render()

    def __add__(self, other) -> str:
        return self.render() + str(other)

    def __radd__(self, other) -> str:
        return str(other) + self.render()

    def __iadd__(self, other) -> str:
        return str(other) + self.render()

    def __and__(self, other) -> str:
        return self.render() + str(other)

    def __iand__(self, other) -> str:
        return str(other) + self.render()

    def __repr__(self) -> str:
        return self.render()

    def render(self, safe: bool = False) -> str:
        """
        Renders a template with self.__dict__ as context
        :return:
        rendered template as string | SafeString
        """
        safe_string = render_to_string(template_name=PATH_TO_TEMPLATES + self.template_name, context=self.__dict__)
        if safe:
            return safe_string
        # render_to_string() returns a SafeString, which implements it's own __add__ function.
        # If we don't convert the SafeString to a normal str instance, we cant concatenate BootstrapComponent directly
        # with our custom __add__, __iadd__, ... functions
        byte_safe_string = str.encode(safe_string, encoding='utf-8')
        return byte_safe_string.decode(encoding='utf-8')


class ProgressBar(BootstrapComponent):
    template_name = "progressbar.html"

    def __init__(self, progress: int = 0, color: ProgressColorEnum = ProgressColorEnum.PRIMARY, animated: bool = True,
                 striped: bool = True):
        self.progress = progress
        self.color = color
        self.animated = animated
        self.striped = striped


class Badge(BootstrapComponent):
    template_name = "badge.html"

    def __init__(self, value: str, badge_color: BadgeColorEnum = BadgeColorEnum.INFO, badge_pill: bool = False,
                 tooltip: str = '', tooltip_placement: str = 'left',):
        self.value = value
        self.badge_color = badge_color
        self.badge_pill = badge_pill
        self.tooltip = tooltip
        self.tooltip_placement = tooltip_placement


class Link(BootstrapComponent):
    template_name = "link.html"

    def __init__(self, url: str, value: str, color: LinkColorEnum = None, needs_perm: str = None,
                 tooltip: str = None, tooltip_placement: TooltipPlacementEnum = None, open_in_new_tab: bool = False,
                 dropdown_item: bool = False):
        self.url = url
        self.value = value
        self.color = color
        self.tooltip = tooltip
        self.tooltip_placement = tooltip_placement.value if tooltip_placement and tooltip else None
        self.needs_perm = needs_perm
        self.open_in_new_tab = open_in_new_tab
        self.dropdown_item = 'dropdown-item' if dropdown_item else ''


class Modal(BootstrapComponent):
    template_name = "modal.html"

    def __init__(self, title: str, modal_body: str, btn_value: str, btn_tooltip: str = None,
                 btn_color: ButtonColorEnum = ButtonColorEnum.INFO, modal_footer: str = None,
                 fade: bool = True, size: ModalSizeEnum = None, fetch_url: str = None):
        self.title = title
        self.modal_body = modal_body
        self.modal_footer = modal_footer
        self.fade = fade
        self.size = size
        self.modal_id = 'id_' + str(uuid.uuid4())
        self.fetch_url = fetch_url
        self.template_name = "modal_ajax.html" if self.fetch_url else "modal.html"
        self.button = Button(value=btn_value, color=btn_color, data_toggle='modal', data_target=f'{self.modal_id}',
                             tooltip=btn_tooltip)


class Accordion(BootstrapComponent):
    template_name = 'accordion_ajax.html'

    def __init__(self, accordion_title: str, accordion_title_center: str = '', accordion_title_right: str = '',
                 accordion_body: str = None, fetch_url: str = None):
        self.accordion_title = accordion_title
        self.accordion_title_center = accordion_title_center
        self.accordion_title_right = accordion_title_right
        self.accordion_body = accordion_body
        self.fetch_url = fetch_url
        self.template_name = 'accordion_ajax.html' if self.fetch_url else 'accordion.html'
        self.accordion_id = 'id_' + str(uuid.uuid4())


class AbstractButton(BootstrapComponent):
    pass


class LinkButton(AbstractButton):
    template_name = "link.html"

    def __init__(self, url: str, value: str, color: ButtonColorEnum = ButtonColorEnum.INFO,
                 needs_perm: str = None, tooltip: str = None, tooltip_placement: TooltipPlacementEnum = None,
                 size: ButtonSizeEnum = None):
        self.url = url
        self.value = value
        self.color = 'btn ' + color.value if color else None
        self.tooltip = tooltip
        self.tooltip_placement = tooltip_placement.value if tooltip_placement and tooltip else None
        self.needs_perm = needs_perm
        self.size = size.value if size else None


class Button(AbstractButton):
    template_name = 'button.html'

    def __init__(self, value: str, color: ButtonColorEnum = ButtonColorEnum.INFO, data_toggle: str = None,
                 data_target: str = None, aria_expanded: str = None, aria_controls: str = None, tooltip: str = None):
        self.value = value
        self.color = color
        self.data_toggle = data_toggle
        self.data_target = data_target
        self.aria_expanded = aria_expanded
        self.aria_controls = aria_controls
        self.tooltip = tooltip


class ButtonGroup(BootstrapComponent):
    template_name = 'button_group.html'

    def __init__(self, aria_label: str, buttons: [AbstractButton]):
        self.aria_label = aria_label
        self.buttons = [button.render() for button in buttons]


class Dropdown(BootstrapComponent):
    template_name = 'dropdown.html'

    def __init__(self, value: str, items: [Link], color: ButtonColorEnum = ButtonColorEnum.INFO, tooltip: str = None,
                 tooltip_placement: TooltipPlacementEnum = None, header: str = None):
        self.value = value
        self.color = color
        self.items = []
        for item in items:
            item.dropdown_item = 'dropdown-item'
            self.items.append(item.render())
        self.tooltip = tooltip
        self.tooltip_placement = tooltip_placement.value if tooltip_placement and tooltip else None
        self.header = header
        self.dropdown_id = 'id_' + str(uuid.uuid4())


class Collapsible(BootstrapComponent):
    template_name = 'collapsible.html'

    def __init__(self, card_body: str, btn_value: str, collapsible_id: str = None):
        self.card_body = card_body
        self.collapsible_id = collapsible_id if collapsible_id else 'id_' + str(uuid.uuid4())
        self.button = Button(value=btn_value, data_toggle='collapse', data_target=f'#{self.collapsible_id}',
                             aria_expanded='false', aria_controls=self.collapsible_id).render()


class LeafletClient(BootstrapComponent):
    template_name = 'leaflet_client.html'

    def __init__(self, polygon: Polygon, add_polygon_as_layer: bool = True, height: str = '50vh',
                 min_height: str = '200px'):
        self.polygon = polygon
        self.add_polygon_as_layer = add_polygon_as_layer
        self.height = height
        self.min_height = min_height
        self.map_id = 'id_' + str(uuid.uuid4()).replace("-", "_")


class ListGroupItem(BootstrapComponent):
    template_name = 'list_group_item.html'

    def __init__(self, left: str = '', center: str = None, right: str = ''):
        self.left = left
        self.center = center
        self.right = right


class ListGroup(BootstrapComponent):
    template_name = 'list_group.html'

    def __init__(self, items: [ListGroupItem]):
        self.items = [item.render() for item in items]
