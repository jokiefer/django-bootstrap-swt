import uuid
from abc import ABC

from django.contrib.gis.geos import Polygon
from django.template.loader import render_to_string
from django_bootstrap_swt.enums import ButtonColorEnum, TooltipPlacementEnum, ProgressColorEnum, BadgeColorEnum, \
    ButtonSizeEnum, ModalSizeEnum, TextColorEnum, BackgroundColorEnum, BorderColorEnum, DataToggleEnum

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
    def __init__(self, url: str, value: str, color: TextColorEnum = None, open_in_new_tab: bool = False,
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
    def __init__(self, value: str, color: ButtonColorEnum = None, size: ButtonSizeEnum = None,
                 data_toggle: DataToggleEnum = None,
                 data_target: str = None, aria_expanded: bool = None, aria_controls: str = None,
                 additional_classes: [str] = None, *args, **kwargs):
        super().__init__(template_name='button.html', *args, **kwargs)
        self.value = value
        self.color = color
        self.size = size
        self.data_toggle = data_toggle
        self.data_target = data_target
        if aria_expanded == True:
            self.aria_expanded = 'true'
        elif aria_expanded == False:
            self.aria_expanded = 'false'
        self.aria_controls = aria_controls
        self.additional_classes = additional_classes


class Modal(BootstrapComponent):
    def __init__(self, title: str, body: str, btn_value: str, btn_color: ButtonColorEnum,
                 btn_size: ButtonSizeEnum = None, footer: str = None, fade: bool = True,
                 size: ModalSizeEnum = None, fetch_url: str = None):
        super().__init__(template_name="modal.html")
        self.title = title
        self.body = body
        self.footer = footer
        self.fade = fade
        self.size = size
        self.modal_id = 'id_' + str(uuid.uuid4())
        self.fetch_url = fetch_url
        self.button = Button(value=btn_value, color=btn_color, size=btn_size, data_toggle=DataToggleEnum.MODAL,
                             data_target=f'{self.modal_id}')


class Cell(BootstrapComponent):
    def __init__(self):
        super(Cell, self).__init__(template_name='cell.html')


class Row(BootstrapComponent):
    def __init__(self, cells: [Cell]):
        super(Row, self).__init__(template_name='row.html')
        self.cells = cells


class CardHeader(BootstrapComponent):
    def __init__(self, content: str, header_id: uuid = None, bg_color: BackgroundColorEnum = None,
                 text_color: TextColorEnum = None, border: BorderColorEnum = None, *args, **kwargs):
        super(CardHeader, self).__init__(template_name='card_header.html', *args, **kwargs)
        self.content = content
        self.header_id = 'id_' + str(header_id) if header_id else 'id_' + str(uuid.uuid4())
        self.bg_color = bg_color
        self.border = border
        self.text_color = text_color


class CardBody(BootstrapComponent):
    def __init__(self, content: str = None, body_id: uuid = None, bg_color: BackgroundColorEnum = None,
                 text_color: TextColorEnum = None, border: BorderColorEnum = None, fetch_url: str = None,
                 data_parent: str = None, aria_labelledby: str = None, additional_classes: [str] = None,
                 *args, **kwargs):
        super(CardBody, self).__init__(template_name='card_body.html', *args, **kwargs)
        self.content = content
        self.body_id = 'id_' + str(body_id) if body_id else 'id_' + str(uuid.uuid4())
        self.bg_color = bg_color
        self.text_color = text_color
        self.border = border
        self.fetch_url = fetch_url
        self.data_parent = data_parent
        self.aria_labelledby = aria_labelledby
        self.additional_classes = additional_classes


class CardFooter(BootstrapComponent):
    def __init__(self, content: str, bg_color: BackgroundColorEnum = None, text_color: TextColorEnum = None,
                 border: BorderColorEnum = None,  *args, **kwargs):
        super(CardFooter, self).__init__(template_name='card_footer.html', *args, **kwargs)
        self.content = content
        self.bg_color = bg_color
        self.border = border
        self.text_color = text_color


class Card(BootstrapComponent):
    def __init__(self, body: CardBody, header: CardHeader = None, footer: CardFooter = None,
                 bg_color: BackgroundColorEnum = None, text_color: TextColorEnum = None,
                 border: BorderColorEnum = None, *args, **kwargs):
        super(Card, self).__init__(template_name='card.html', *args, **kwargs)
        self.body = body
        self.header = header
        self.footer = footer
        self.bg_color = bg_color
        self.border = border
        self.text_color = text_color


class Accordion(BootstrapComponent):
    def __init__(self, btn_value: str, content: str = None, fetch_url: str = None,
                 header_bg_color: BackgroundColorEnum = None, body_bg_color: BackgroundColorEnum = None,
                 header_text_color: TextColorEnum = None, body_text_color: TextColorEnum = None,
                 header_border: BorderColorEnum = None, body_border: BorderColorEnum = None,):
        super().__init__(template_name='accordion.html')
        self.accordion_id = 'id_' + str(uuid.uuid4())
        self.card_body = CardBody(content=content,
                                  fetch_url=fetch_url,
                                  bg_color=body_bg_color,
                                  data_parent=self.accordion_id,
                                  additional_classes=['collapse'],
                                  text_color=body_text_color,
                                  border=body_border)
        accordion_btn = Button(value=f'<i class="fa" aria-hidden="true"></i> {btn_value}',
                               data_toggle=DataToggleEnum.COLLAPSE,
                               data_target=self.card_body.body_id,
                               additional_classes=['collapsed', 'accordion', 'text-left'],
                               aria_expanded=False,
                               aria_controls=self.card_body.body_id)
        self.card_header = CardHeader(content=f'{accordion_btn}',
                                      bg_color=header_bg_color,
                                      text_color=header_text_color,
                                      border=header_border)
        self.card_body.aria_labelledby = self.card_header.header_id
        self.content = Card(header=self.card_header, body=self.card_body)


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
