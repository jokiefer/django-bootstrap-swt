import uuid
from abc import ABC
from collections import OrderedDict

from django.template.loader import render_to_string
from django_bootstrap_swt.enums import ButtonColorEnum, TooltipPlacementEnum, ProgressColorEnum, BadgeColorEnum, \
    ButtonSizeEnum, ModalSizeEnum, TextColorEnum, BackgroundColorEnum, BorderColorEnum, DataToggleEnum

PATH_TO_TEMPLATES = "django_bootstrap_swt/components/"


class AbstractButton(ABC):
    """
    This class is used to group other Button representing components
    """
    pass


class BootstrapComponent:
    """
    This is the base class for all components. It customizes some magic functions to get it running for concatenating
    without calling any function.
    """
    def __init__(self, path_to_templates: str = PATH_TO_TEMPLATES, template_name: str = None, needs_perm: str = None,
                 *args, **kwargs):
        """
        :param path_to_templates: the relative path to the templates
        :param template_name: the name of the template which should be used for rendering
        :param needs_perm: Only used in RenderHelper: the permission which is needed to see the component.
        :param args:
        :param kwargs:
        """
        self.path_to_templates = path_to_templates
        self.template_name = template_name
        self.needs_perm = needs_perm

    def __str__(self) -> str:
        """:returns rendered component as string"""
        return self.render()

    def __add__(self, other) -> str:
        """:returns rendered component concatenated with the :param other"""
        return self.render() + other

    def __radd__(self, other) -> str:
        """:returns :param other concatenated with the rendered component """
        return other + self.render()

    def __iadd__(self, other) -> str:
        """:returns :param other concatenated with the rendered component """
        return other + self.render()

    def __repr__(self) -> str:
        """:returns rendered component as string"""
        return self.render()

    def render(self, safe: bool = False) -> str:
        """Renders a template with self.__dict__ as context

        :param safe: switches if the rendered component is returned as SafeString or str
        :return: rendered template as string | SafeString
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
    """
    This class renders the Bootstrap Tooltip component.
    https://getbootstrap.com/docs/4.0/components/tooltips/
    """
    def __init__(self, title: str, surrounded_component: str, placement: TooltipPlacementEnum = None, *args, **kwargs):
        """
        :param title: the title of the tooltip which is also the content of the tooltip to show
        :param surrounded_component: the content to surround with this tooltip
        :param placement: Optional: placement of the tooltip relative to the surrounded_component
        :param args:
        :param kwargs:
        """
        super(Tooltip, self).__init__(template_name="tooltip.html", *args, **kwargs)
        self.title = title
        self.surrounded_component = surrounded_component
        self.placement = placement


class TooltipSurroundedComponent(BootstrapComponent, ABC):
    """
    This is the helper class to surround a BootstrapComponent with a Tooltip.
    """
    def __init__(self, tooltip: str = None, tooltip_placement: TooltipPlacementEnum = None, template_name: str = None,
                 *args, **kwargs):
        """
        :param tooltip: Optional the title of the tooltip which is also the content of the tooltip
        :param tooltip_placement: Optional: placement of the tooltip relative to the surrounded_component
        :param template_name: Optional: the template to use for rendering
        :param args:
        :param kwargs:
        """
        super(TooltipSurroundedComponent, self).__init__(template_name=template_name,
                                                         path_to_templates=PATH_TO_TEMPLATES,
                                                         *args, **kwargs)
        self.tooltip = tooltip
        self.tooltip_placement = tooltip_placement

    def render(self, safe: bool = False) -> str:
        self_rendered = super(TooltipSurroundedComponent, self).render(safe=safe)
        if self.tooltip:
            return Tooltip(title=self.tooltip, surrounded_component=self_rendered,
                           placement=self.tooltip_placement).render(safe=safe)
        return self_rendered


class ProgressBar(BootstrapComponent):
    """
    This class renders the Bootstrap Progress component.
    https://getbootstrap.com/docs/4.0/components/progress
    """
    def __init__(self, progress: int = 0, color: ProgressColorEnum = None, animated: bool = True,
                 striped: bool = True, *args, **kwargs):
        """
        :param progress: the progress value from 0 - 100 percentage
        :param color: Optional: the color of the Progressbar. Default color is primary blue.
        :param animated: Optional: toggles the animation flag of the progressbar
        :param striped: Optional: toggles the striped flag for striped css
        :param args:
        :param kwargs:
        """
        super(ProgressBar, self).__init__(template_name="progressbar.html", *args, **kwargs)
        self.progress = progress
        self.color = color
        self.animated = animated
        self.striped = striped


class Badge(TooltipSurroundedComponent):
    """
    This class renders the Bootstrap Badge component.
    https://getbootstrap.com/docs/4.0/components/badge/
    """
    def __init__(self, value: str, color: BadgeColorEnum = BadgeColorEnum.INFO, pill: bool = False, *args, **kwargs):
        """
        :param value: the value of the badge
        :param color: the color of the badge. Default is bootstrap info color.
        :param pill: toggles the pill flag
        :param args:
        :param kwargs:
        """
        super(Badge, self).__init__(template_name='badge.html', *args, **kwargs)
        self.value = value
        self.color = color
        self.pill = pill


class Link(TooltipSurroundedComponent):
    """
    This class renders the a HTML Link with bootstrap depending css if needed.
    """
    def __init__(self, url: str, value: str, color: TextColorEnum = None, open_in_new_tab: bool = False,
                 dropdown_item: bool = False, *args, **kwargs):
        """
        :param url: the href of the link
        :param value: the value of the link
        :param color: the color of the link
        :param open_in_new_tab: toggles the open link in new tab flag
        :param dropdown_item: toggles the is dropdown item flag
        :param args:
        :param kwargs:
        """
        super(Link, self).__init__(*args, **kwargs)
        self.template_name = "link.html"
        self.url = url
        self.value = value
        self.color = color
        self.open_in_new_tab = open_in_new_tab
        self.dropdown_item = dropdown_item


class LinkButton(AbstractButton, TooltipSurroundedComponent):
    """
    This class renders the a HTML Link as a Bootstrap Button.
    https://getbootstrap.com/docs/4.0/components/buttons/#button-tags
    """
    def __init__(self, url: str, value: str, color: ButtonColorEnum, size: ButtonSizeEnum = None,
                 open_in_new_tab: bool = False, *args, **kwargs):
        """
        :param url: the href of the link
        :param value: the value of the link
        :param color: the color of the link
        :param open_in_new_tab: toggles the open link in new tab flag
        :param size: the size of the button
        :param args:
        :param kwargs:
        """
        super(LinkButton, self).__init__(template_name="link.html", *args, **kwargs)
        self.url = url
        self.value = value
        self.is_btn = True
        self.color = color
        self.size = size.value if size else None
        self.open_in_new_tab = open_in_new_tab


class Button(AbstractButton, TooltipSurroundedComponent):
    """
    This class renders the Bootstrap Button component.
    https://getbootstrap.com/docs/4.0/components/buttons/
    """
    def __init__(self, value: str, color: ButtonColorEnum = None, size: ButtonSizeEnum = None,
                 data_toggle: DataToggleEnum = None,
                 data_target: str = None, aria_expanded: bool = None, aria_controls: str = None,
                 aria_haspopup: bool = None, additional_classes: [str] = None, *args, **kwargs):
        """
        :param value: the value of the button
        :param color: the color of the button
        :param size: the size of the button
        :param data_toggle: Optional: sets the data_toggle attribute
        :param data_target: Optional: sets the data_target attribute
        :param aria_expanded: Optional: sets the aria_expanded attribute
        :param aria_controls: Optional: sets the aria_controls attribute
        :param aria_haspopup: Optional: sets the aria_haspopup attribute
        :param additional_classes: Optional: appends strings to the class html tag
        :param args:
        :param kwargs:
        """
        super(Button, self).__init__(template_name='button.html', *args, **kwargs)
        self.value = value
        self.color = color
        self.size = size
        self.data_toggle = data_toggle
        self.data_target = data_target
        if aria_expanded is True:
            self.aria_expanded = 'true'
        elif aria_expanded is False:
            self.aria_expanded = 'false'
        if aria_haspopup is True:
            self.aria_haspopup = 'true'
        elif aria_haspopup is False:
            self.aria_haspopup = 'false'
        self.aria_controls = aria_controls
        self.button_id = 'id_' + str(uuid.uuid4())
        self.additional_classes = additional_classes


class Modal(BootstrapComponent):
    """
    This class renders the Bootstrap Modal component.
    https://getbootstrap.com/docs/4.0/components/modal/
    """
    def __init__(self, title: str, body: str, btn_value: str, btn_color: ButtonColorEnum,
                 btn_size: ButtonSizeEnum = None, footer: str = None, fade: bool = True,
                 size: ModalSizeEnum = None, fetch_url: str = None, *args, **kwargs):
        """
        :param title: the title of the modal
        :param body: the body content of the modal
        :param btn_value: the value of the button which opens the modal
        :param btn_color: the color of the button which opens the modal
        :param btn_size: Optional: the size of the button which opens the modal
        :param footer: Optional: the footer content of the modal
        :param fade: Optional: toggles the fade flag
        :param size: Optional: the size of the modal
        :param fetch_url: Optional: the url where the content will be fetched from on modal shown event
        :param args:
        :param kwargs:
        """
        super(Modal, self).__init__(template_name="modal.html", *args, **kwargs)
        self.title = title
        self.body = body
        self.footer = footer
        self.fade = fade
        self.size = size
        self.modal_id = 'id_' + str(uuid.uuid4())
        self.fetch_url = fetch_url
        self.button = Button(value=btn_value, color=btn_color, size=btn_size, data_toggle=DataToggleEnum.MODAL,
                             data_target=f'{self.modal_id}')


class CardHeader(BootstrapComponent):
    """
    This class renders the Bootstrap Card Header component.
    https://getbootstrap.com/docs/4.0/components/card/#header-and-footer
    """
    def __init__(self, content: str, header_id: uuid = None, bg_color: BackgroundColorEnum = None,
                 text_color: TextColorEnum = None, border: BorderColorEnum = None, *args, **kwargs):
        """
        :param content: the conent of the header
        :param header_id: Optional: the id of the header div
        :param bg_color: Optional: the background color of the header
        :param text_color: Optional: the text color of all content in the header
        :param border: Optional: the border color of the header
        :param args:
        :param kwargs:
        """
        super(CardHeader, self).__init__(template_name='card_header.html', *args, **kwargs)
        self.content = content
        self.header_id = 'id_' + str(header_id) if header_id else 'id_' + str(uuid.uuid4())
        self.bg_color = bg_color
        self.border = border
        self.text_color = text_color


class CardBody(BootstrapComponent):
    """
    This class renders the Bootstrap Card Body component.
    https://getbootstrap.com/docs/4.0/components/card/#content-types
    """
    def __init__(self, content: str = None, body_id: uuid = None, bg_color: BackgroundColorEnum = None,
                 text_color: TextColorEnum = None, border: BorderColorEnum = None, fetch_url: str = None,
                 data_parent: str = None, aria_labelledby: str = None, additional_classes: [str] = None,
                 *args, **kwargs):
        """
        :param content: Optional: the content of the card body
        :param body_id: Optional: the id of the body div
        :param bg_color: Optional: the background color of the card body
        :param text_color: Optional: the text color for all content in card body
        :param border: Optional: the border color of the card body
        :param fetch_url: Optional: is used from Modal class to set the fetch_url for this div
        :param data_parent: Optional: sets the data_parent attribute
        :param aria_labelledby: Optional: sets the aria_labelledby attribute
        :param additional_classes: Optional: appends strings to the class html tag
        :param args:
        :param kwargs:
        """
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
    """
    This class renders the Bootstrap Card Footer component.
    https://getbootstrap.com/docs/4.0/components/card/#header-and-footer
    """
    def __init__(self, content: str, bg_color: BackgroundColorEnum = None, text_color: TextColorEnum = None,
                 border: BorderColorEnum = None,  *args, **kwargs):
        """
        :param content: Optional: the content of the card footer
        :param bg_color: Optional: the background color of the card footer
        :param text_color: Optional: the text color of the all content in card footer
        :param border: Optional: the border color of the card footer
        :param args:
        :param kwargs:
        """
        super(CardFooter, self).__init__(template_name='card_footer.html', *args, **kwargs)
        self.content = content
        self.bg_color = bg_color
        self.border = border
        self.text_color = text_color


class Card(BootstrapComponent):
    """
    This class renders the Bootstrap Card component.
    https://getbootstrap.com/docs/4.0/components/card/
    """
    def __init__(self, body: CardBody, header: CardHeader = None, footer: CardFooter = None,
                 bg_color: BackgroundColorEnum = None, text_color: TextColorEnum = None,
                 border: BorderColorEnum = None, *args, **kwargs):
        """
        :param body: the CardBody component
        :param header: the CardHeader component
        :param footer: the CardFooter component
        :param bg_color: the background color of the card
        :param text_color: the text color of the card
        :param border: the border color of the card
        :param args:
        :param kwargs:
        """
        super(Card, self).__init__(template_name='card.html', *args, **kwargs)
        self.body = body
        self.header = header
        self.footer = footer
        self.bg_color = bg_color
        self.border = border
        self.text_color = text_color


class Accordion(BootstrapComponent):
    """
    This class renders the Bootstrap Accordion component.
    https://getbootstrap.com/docs/4.0/components/collapse/#accordion-example
    """
    def __init__(self, btn_value: str, content: str = None, fetch_url: str = None,
                 header_bg_color: BackgroundColorEnum = None, body_bg_color: BackgroundColorEnum = None,
                 header_text_color: TextColorEnum = None, body_text_color: TextColorEnum = None,
                 header_border: BorderColorEnum = None, body_border: BorderColorEnum = None,
                 header_center_content: str = None, header_right_content: str = None, *args, **kwargs):
        """
        :param btn_value: the value of the button to toggle the accordion
        :param content: the content of the accordion
        :param fetch_url: Optional: the url where the content will be fetched from on accordion shown event
        :param header_bg_color: the background color of the accordion header
        :param body_bg_color: the background color of the accordion body
        :param header_text_color: the text color of the accordion header
        :param body_text_color: the text color of the accordion body
        :param header_border: the border color of the accordion header
        :param body_border: the border color of the accordion body
        :param header_center_content: the content of the header center placed
        :param header_right_content: the content of the header right placed
        :param args:
        :param kwargs:
        """
        super(Accordion, self).__init__(template_name='accordion.html', *args, **kwargs)
        self.accordion_id = 'id_' + str(uuid.uuid4())
        self.card_body = CardBody(content=content,
                                  fetch_url=fetch_url,
                                  bg_color=body_bg_color,
                                  data_parent=self.accordion_id,
                                  additional_classes=['collapse'],
                                  text_color=body_text_color,
                                  border=body_border)

        self.accordion_btn = Button(value=f'<i class="fa" aria-hidden="true"></i> {btn_value}',
                                    data_toggle=DataToggleEnum.COLLAPSE,
                                    data_target=self.card_body.body_id,
                                    additional_classes=['collapsed', 'accordion', 'text-left'],
                                    aria_expanded=False,
                                    aria_controls=self.card_body.body_id)
        default_header_row = DefaultHeaderRow(content_left=self.accordion_btn.render(),
                                              content_center=header_center_content,
                                              content_right=header_right_content).render()

        self.card_header = CardHeader(content=default_header_row,
                                      bg_color=header_bg_color,
                                      text_color=header_text_color,
                                      border=header_border)
        self.card_body.aria_labelledby = self.card_header.header_id
        self.content = Card(header=self.card_header, body=self.card_body)


class ButtonGroup(BootstrapComponent):
    """
    This class renders the Bootstrap Button Group component.
    https://getbootstrap.com/docs/4.0/components/button-group/
    """
    def __init__(self, aria_label: str, buttons: [AbstractButton], *args, **kwargs):
        """
        :param aria_label: sets the aria_label attribute
        :param buttons: list of buttons to include them in this ButtonGroup
        :param args:
        :param kwargs:
        """
        super(ButtonGroup, self).__init__(template_name='button_group.html', *args, **kwargs)
        self.aria_label = aria_label
        self.buttons = [button.render() for button in buttons]


class Dropdown(TooltipSurroundedComponent):
    """
    This class renders the Bootstrap Dropdown component.
    https://getbootstrap.com/docs/4.0/components/dropdowns/
    """
    def __init__(self, value: str, items: [Link], color: ButtonColorEnum = ButtonColorEnum.INFO, header: str = None,
                 *args, **kwargs):
        """
        :param value: the value of the dropdown collapse button
        :param items: the items which should be placed in this dropdown
        :param color: the color of the dropdown collapse button
        :param header: sets one header on top of the dropdown
        :param args:
        :param kwargs:
        """
        super(Dropdown, self).__init__(template_name='dropdown.html', *args, **kwargs)
        self.value = value
        self.color = color
        self.button = Button(value=value, color=color, additional_classes=['dropdown-toggle'],
                             data_toggle=DataToggleEnum.DROPDOWN, aria_haspopup=True, aria_expanded=False)
        self.button.data_target = self.button.button_id
        self.dropdown_id = self.button.button_id
        self.items = []
        for item in items:
            item.dropdown_item = 'dropdown-item'
            self.items.append(item.render())
        self.header = header


class ListGroupItem(BootstrapComponent):
    """
    This class renders the Bootstrap List Group Item component.
    https://getbootstrap.com/docs/4.0/components/list-group/
    """
    def __init__(self, content: str, *args, **kwargs):
        """
        :param content: content of the item
        :param args:
        :param kwargs:
        """
        super(ListGroupItem, self).__init__(template_name='list_group_item.html', *args, **kwargs)
        self.content = content


class ListGroup(BootstrapComponent):
    """
    This class renders the Bootstrap List Group component.
    https://getbootstrap.com/docs/4.0/components/list-group/
    """
    def __init__(self, items: [ListGroupItem], *args, **kwargs):
        """
        :param items: a list of items which shall be part of this ListGroup
        :param args:
        :param kwargs:
        """
        super(ListGroup, self).__init__(template_name='list_group.html', *args, **kwargs)
        self.items = [item.render() for item in items]


class Tag(TooltipSurroundedComponent):
    """
    This is a helper class for generic div rendering
    """
    def __init__(self, tag: str, content: str = None, attrs: {} = None, *args, **kwargs):
        """
        :param tag: the tag name
        :param content: the content of this div
        :param attrs: Optional: a dict with with key value pairs which describes the attribute and his values
        :param args:
        :param kwargs:
        """
        super(Tag, self).__init__(template_name='tag.html', *args, **kwargs)
        self.tag = tag
        self.content = content
        self.attrs = attrs if attrs else {}


class DefaultHeaderRow(BootstrapComponent):
    """
    This is a helper class for standardized headers with three columns
    """
    def __init__(self, content_left: str, content_right: str, content_center: str = None, *args, **kwargs):
        """
        :param content_left: the left content in this row
        :param content_right:  the right content in this row
        :param content_center: Optional: the centered content in this row
        :param args:
        :param kwargs:
        """
        super(DefaultHeaderRow, self).__init__(*args, **kwargs)
        self.content_left = content_left
        self.content_center = content_center
        self.content_right = content_right

    def render(self, safe: bool = False) -> str:
        col_left = Tag(tag='div',
                       content=self.content_left,
                       attrs={"class": ['col-sm', 'text-left']})
        if self.content_center:
            col_center = Tag(tag='div',
                             content=self.content_center,
                             attrs={"class": ['col-sm', 'text-center']})
        else:
            col_center = ''
        if self.content_right:
            col_right = Tag(tag='div',
                            content=self.content_right,
                            attrs={"class": ['col-sm', 'text-right']})
        else:
            col_right = ''
        content = col_left + col_center + col_right
        return Tag(tag='div',
                   content=content,
                   attrs={"class": ['row']}).render(safe=safe)
