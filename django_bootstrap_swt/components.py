import uuid
from abc import ABC

from django.contrib.gis.geos import Polygon
from django.template.loader import render_to_string
from django_bootstrap_swt.enums import ButtonColorEnum, TooltipPlacementEnum, ProgressColorEnum, BadgeColorEnum, \
    LinkColorEnum, ButtonSizeEnum, ModalSizeEnum


PATH_TO_TEMPLATES = "django_bootstrap_swt/components/"


class AbstractPermissionComponent(ABC):
    """
    This class is used adds the needs_perm attribute to a component
    """
    def __init__(self, needs_perm: str = None):
        self.needs_perm = needs_perm


class AbstractButton(ABC):
    """
    This class is used to group other Button representing components
    """
    pass


class BootstrapComponent:
    def __init__(self, path_to_templates: str = PATH_TO_TEMPLATES, template_name: str = None):
        self.path_to_templates = path_to_templates
        self.template_name = template_name

    def __str__(self) -> str:
        return self.render()

    def __add__(self, other) -> str:
        return self.render() + other

    def __radd__(self, other) -> str:
        return other + self.render()

    def __iadd__(self, other) -> str:
        return other + self.render()

    def __repr__(self) -> str:
        return self.render()

    def render(self, safe: bool = False) -> str:
        """
        Renders a template with self.__dict__ as context
        :return:
        rendered template as string | SafeString
        """
        safe_string = render_to_string(template_name=self.path_to_templates + self.template_name, context=self.__dict__)
        if safe:
            return safe_string
        # render_to_string() returns a SafeString, which implements it's own __add__ function.
        # If we don't convert the SafeString to a normal str instance, we cant concatenate BootstrapComponent directly
        # with our custom __add__, __iadd__, ... functions
        byte_safe_string = str.encode(safe_string, encoding='utf-8')
        return byte_safe_string.decode(encoding='utf-8')


class Tooltip(BootstrapComponent):
    def __init__(self, title: str, sourounded_component: str, placement: TooltipPlacementEnum = None):
        super().__init__(template_name="tooltip.html")
        self.title = title
        self.sourounded_component = sourounded_component
        self.placement = placement


class TooltipSouroundedComponent(BootstrapComponent):
    def __init__(self, tooltip: str = None, tooltip_placement: TooltipPlacementEnum = None, template_name: str = None):
        super(TooltipSouroundedComponent, self).__init__(template_name=template_name,
                                                         path_to_templates=PATH_TO_TEMPLATES)
        self.tooltip = tooltip
        self.tooltip_placement = tooltip_placement

    def render(self, safe: bool = False) -> str:
        self_rendered = super(TooltipSouroundedComponent, self).render(safe=safe)
        if self.tooltip:
            return Tooltip(title=self.tooltip, sourounded_component=self_rendered,
                           placement=self.tooltip_placement).render(safe=safe)
        return self_rendered


class ProgressBar(BootstrapComponent):
    def __init__(self, progress: int = 0, color: ProgressColorEnum = None, animated: bool = True,
                 striped: bool = True):
        super().__init__(template_name="progressbar.html")
        self.progress = progress
        self.color = color
        self.animated = animated
        self.striped = striped


class Badge(TooltipSouroundedComponent):
    def __init__(self, value: str, color: BadgeColorEnum = BadgeColorEnum.INFO, pill: bool = False, *args, **kwargs):
        super().__init__(template_name='badge.html', *args, **kwargs)
        self.value = value
        self.color = color
        self.pill = pill


class Link(TooltipSouroundedComponent, AbstractPermissionComponent):
    def __init__(self, url: str, value: str, color: LinkColorEnum = None, open_in_new_tab: bool = False,
                 dropdown_item: bool = False, *args, **kwargs):
        super().__init__(template_name="link.html", *args, **kwargs)
        self.url = url
        self.value = value
        self.color = color
        self.open_in_new_tab = open_in_new_tab
        self.dropdown_item = dropdown_item


class LinkButton(AbstractButton, TooltipSouroundedComponent, AbstractPermissionComponent):
    def __init__(self, url: str, value: str, color: ButtonColorEnum, size: ButtonSizeEnum = None, *args, **kwargs):
        super().__init__(template_name="link.html", *args, **kwargs)
        self.url = url
        self.value = value
        self.is_btn = True
        self.color = color
        self.size = size.value if size else None


class Button(AbstractButton, TooltipSouroundedComponent, AbstractPermissionComponent):
    def __init__(self, value: str, color: ButtonColorEnum, size: ButtonSizeEnum = None, data_toggle: str = None,
                 data_target: str = None, aria_expanded: str = None, aria_controls: str = None, *args, **kwargs):
        super().__init__(template_name='button.html', *args, **kwargs)
        self.value = value
        self.color = color
        self.size = size
        self.data_toggle = data_toggle
        self.data_target = data_target
        self.aria_expanded = aria_expanded
        self.aria_controls = aria_controls


class Modal(BootstrapComponent):
    def __init__(self, title: str, modal_body: str, btn_value: str, btn_color: ButtonColorEnum,
                 modal_footer: str = None, fade: bool = True, size: ModalSizeEnum = None, fetch_url: str = None):
        super().__init__(template_name="modal.html")
        self.title = title
        self.modal_body = modal_body
        self.modal_footer = modal_footer
        self.fade = fade
        self.size = size
        self.modal_id = 'id_' + str(uuid.uuid4())
        self.fetch_url = fetch_url
        self.template_name = "modal_ajax.html" if self.fetch_url else "modal.html"
        self.button = Button(value=btn_value, color=btn_color, data_toggle='modal', data_target=f'{self.modal_id}')


class Accordion(BootstrapComponent):
    def __init__(self, accordion_title: str, accordion_title_center: str = '', accordion_title_right: str = '',
                 accordion_body: str = None, fetch_url: str = None):
        super().__init__(template_name='accordion_ajax.html')
        self.accordion_title = accordion_title
        self.accordion_title_center = accordion_title_center
        self.accordion_title_right = accordion_title_right
        self.accordion_body = accordion_body
        self.fetch_url = fetch_url
        self.template_name = 'accordion_ajax.html' if self.fetch_url else 'accordion.html'
        self.accordion_id = 'id_' + str(uuid.uuid4())


class ButtonGroup(BootstrapComponent):
    def __init__(self, aria_label: str, buttons: [AbstractButton]):
        super().__init__(template_name='button_group.html')
        self.aria_label = aria_label
        self.buttons = [button.render() for button in buttons]


class Dropdown(BootstrapComponent):
    def __init__(self, value: str, items: [Link], color: ButtonColorEnum = ButtonColorEnum.INFO, tooltip: str = None,
                 tooltip_placement: TooltipPlacementEnum = None, header: str = None):
        super().__init__(template_name='dropdown.html')
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
    def __init__(self, card_body: str, btn_value: str, collapsible_id: str = None):
        super().__init__(template_name='collapsible.html')
        self.card_body = card_body
        self.collapsible_id = collapsible_id if collapsible_id else 'id_' + str(uuid.uuid4())
        self.button = Button(value=btn_value, data_toggle='collapse', data_target=f'#{self.collapsible_id}',
                             aria_expanded='false', aria_controls=self.collapsible_id).render()


class LeafletClient(BootstrapComponent):
    def __init__(self, polygon: Polygon, add_polygon_as_layer: bool = True, height: str = '50vh',
                 min_height: str = '200px'):
        super().__init__(template_name='leaflet_client.html')
        self.polygon = polygon
        self.add_polygon_as_layer = add_polygon_as_layer
        self.height = height
        self.min_height = min_height
        self.map_id = 'id_' + str(uuid.uuid4()).replace("-", "_")


class ListGroupItem(BootstrapComponent):
    def __init__(self, left: str = '', center: str = None, right: str = ''):
        super().__init__(template_name='list_group_item.html')
        self.left = left
        self.center = center
        self.right = right


class ListGroup(BootstrapComponent):
    def __init__(self, items: [ListGroupItem]):
        super().__init__(template_name='list_group.html')
        self.items = [item.render() for item in items]
