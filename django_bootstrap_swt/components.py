import uuid
from abc import ABC
from django.template.loader import render_to_string
from django_bootstrap_swt.enums import ButtonColorEnum, TooltipPlacementEnum, ProgressColorEnum, BadgeColorEnum, \
    ButtonSizeEnum, ModalSizeEnum, TextColorEnum, BackgroundColorEnum, BorderColorEnum, DataToggleEnum, HeadingsEnum, \
    AlertEnum
from django.utils.translation import gettext as _

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


class Tag(BootstrapComponent):
    """
    This is a helper class for generic div rendering
    """
    def __init__(self, tag: str = None, content: str = None, attrs: {} = None, template_name: str = 'tag.html',
                 *args, **kwargs):
        """
        :param tag: the tag name
        :param content: the content of this div
        :param attrs: Optional: a dict with with key value pairs which describes the attribute and his values
        :param args:
        :param kwargs:
        """
        super(Tag, self).__init__(template_name=template_name, *args, **kwargs)
        self.tag = tag
        self.content = content
        self.attrs = attrs if attrs else {}

    def update_attribute(self, attribute: str, values: list):
        """
        Updates the self.attrs[attribute] key with new values
        :param attribute: the lookup key for self.attrs
        :param values: the list of new values
        :return:
        """
        if attribute in self.attrs:
            self.attrs[attribute].extend(value for value in values if value not in self.attrs[attribute])
        else:
            self.attrs.update({attribute: values})

    def update_attributes(self, update_attrs: dict):
        """
        Updates the self.attrs attribute with the update_attrs dict
        :param update_attrs: the dict with the update key value pairs. Value shall be a list
        :return: None
        """
        if update_attrs:
            for attribute, values in update_attrs.items():
                self.update_attribute(attribute, values)


class Tooltip(Tag):
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
        attrs = {"class": ["d-inline-block"],
                 "tabindex": [0],
                 "data-html": ["true"],
                 "data-toggle": [DataToggleEnum.TOOLTIP.value],
                 "title": [title]}
        if placement:
            attrs.update({"data-placement": [placement.value]})
        super(Tooltip, self).__init__(tag="span", attrs=attrs, content=surrounded_component, *args, **kwargs)


class TooltipSurroundedComponent(Tag, ABC):
    """
    This is the helper class to surround a BootstrapComponent with a Tooltip.
    """
    def __init__(self, tooltip: str = None, tooltip_placement: TooltipPlacementEnum = None,
                 *args, **kwargs):
        """
        :param tooltip: Optional the title of the tooltip which is also the content of the tooltip
        :param tooltip_placement: Optional: placement of the tooltip relative to the surrounded_component
        :param template_name: Optional: the template to use for rendering
        :param args:
        :param kwargs:
        """
        self.tooltip = tooltip
        self.tooltip_placement = tooltip_placement
        super(TooltipSurroundedComponent, self).__init__(*args, **kwargs)

    def render(self, safe: bool = False) -> str:
        self_rendered = super(TooltipSurroundedComponent, self).render(safe=safe)
        if self.tooltip:
            return Tooltip(title=self.tooltip, surrounded_component=self_rendered,
                           placement=self.tooltip_placement).render(safe=safe)
        return self_rendered


class Alert(Tag):
    """
    This class renders the Bootstrap Alert component.
    https://getbootstrap.com/docs/4.0/components/alerts/
    """
    def __init__(self, msg: str, alert_type: AlertEnum, dismiss: bool = True, *args, **kwargs):
        self.attrs = {"class": ["alert", alert_type.value, "fade", "show"],
                      "role": ["alert"]}

        if dismiss:
            self.update_attribute(attribute="class", values=["alert-dismissible"])
            times = Tag(tag="span", attrs={"aria-hidden": ["true"]}, content="&times;").render()
            dismiss_btn = Tag(tag="button", attrs={"type": ["button"],
                                                   "class": ["close"],
                                                   "data-dismiss": ["alert"],
                                                   "aria-label": [_("Close")]}, content=times)
            msg += dismiss_btn

        super(Alert, self).__init__(tag="div", attrs=self.attrs, content=msg, *args, **kwargs)


class ProgressBar(Tag):
    """
    This class renders the Bootstrap Progress component.
    https://getbootstrap.com/docs/4.0/components/progress
    """
    def __init__(self, progress: int = 0, color: ProgressColorEnum = None, striped: bool = True, animated: bool = True,
                 *args, **kwargs):
        """
        :param progress: the progress value from 0 - 100 percentage
        :param color: Optional: the color of the Progressbar. Default color is primary blue.
        :param striped: Optional: toggles the striped flag for striped css
        :param animated: Optional: toggles the animation flag of the progressbar
        :param args:
        :param kwargs:
        """
        tag = "div"
        attrs = {"class": ["progress"]}

        self.attrs = {"class": ["progress-bar", ],
                      "role": ["progressbar"],
                      "aria-valuenow": [progress],
                      "aria-valuemin": [0],
                      "aria-valuemax": [100],
                      "style": [f"width: { progress }%"]}
        if color:
            self.update_attribute("class", [color.value])
        if striped:
            self.update_attribute("class", ["progress-bar-striped"])
        if animated:
            self.update_attribute("class", ["progress-bar-animated"])

        bar = Tag(tag=tag, attrs=self.attrs, content=f"{progress}%").render()
        super(ProgressBar, self).__init__(tag=tag, attrs=attrs, content=bar, *args, **kwargs)


class Badge(TooltipSurroundedComponent):
    """
    This class renders the Bootstrap Badge component.
    https://getbootstrap.com/docs/4.0/components/badge/
    """
    def __init__(self, content: str, pill: bool = False, color: BadgeColorEnum = BadgeColorEnum.INFO, *args, **kwargs):
        """
        :param content: the content of the badge
        :param pill: toggles the pill flag
        :param color: the color of the badge. Default is bootstrap info color.
        :param args:
        :param kwargs:
        """
        self.attrs = {"class": ["badge", ]}
        if pill:
            self.update_attribute("class", ["pill"])
        if color:
            self.update_attribute("class", [color.value])
        self.content = content
        super(Badge, self).__init__(tag="span", attrs=self.attrs, content=self.content, *args, **kwargs)


class Link(TooltipSurroundedComponent):
    """
    This class renders the a HTML Link with bootstrap depending css if needed.
    """
    def __init__(self, url: str, content: str, color: TextColorEnum = None, open_in_new_tab: bool = False,
                 dropdown_item: bool = False, *args, **kwargs):
        """
        :param url: the href of the link
        :param content: the content of the link
        :param color: the color of the link
        :param open_in_new_tab: toggles the open link in new tab flag
        :param dropdown_item: toggles the is dropdown item flag
        :param args:
        :param kwargs:
        """
        self.attrs = {"href": [url]}
        if color:
            self.update_attribute("class", [color.value])
        if open_in_new_tab:
            self.update_attribute("target", ["_blank"])
        if dropdown_item:
            self.update_attribute("class", ["dropdown-item"])
        self.content = content
        super(Link, self).__init__(tag='a', attrs=self.attrs, content=self.content, *args, **kwargs)


class LinkButton(TooltipSurroundedComponent, AbstractButton):
    """
    This class renders the a HTML Link as a Bootstrap Button.
    https://getbootstrap.com/docs/4.0/components/buttons/#button-tags
    """
    def __init__(self, url: str, content: str, color: ButtonColorEnum, size: ButtonSizeEnum = None,
                 open_in_new_tab: bool = False, *args, **kwargs):
        """
        :param url: the href of the link
        :param content: the content of the link
        :param color: the color of the link
        :param open_in_new_tab: toggles the open link in new tab flag
        :param size: the size of the button
        :param args:
        :param kwargs:
        """
        self.attrs = {"href": [url],
                      "class": ["btn"]}
        if color:
            self.update_attribute("class", [color.value])
        if size:
            self.update_attribute("class", [size.value])
        if open_in_new_tab:
            self.update_attribute("target", ["_blank"])
        self.content = content
        super(LinkButton, self).__init__(tag='a', attrs=self.attrs, content=self.content, *args, **kwargs)


class Button(TooltipSurroundedComponent, AbstractButton):
    """
    This class renders the Bootstrap Button component.
    https://getbootstrap.com/docs/4.0/components/buttons/
    """
    def __init__(self, content: str, color: ButtonColorEnum = None, size: ButtonSizeEnum = None,
                 data_toggle: DataToggleEnum = None,
                 data_target: str = None, aria_expanded: bool = None, aria_controls: str = None,
                 aria_haspopup: bool = None, *args, **kwargs):
        """
        :param content: the content of the button
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
        self.button_id = 'id_' + str(uuid.uuid4())
        self.attrs = {"id": [self.button_id],
                      "type": ["button"],
                      "class": ["btn"]}
        if color:
            self.update_attribute("class", [color.value])
        if size:
            self.update_attribute("class", [size.value])
        if data_toggle:
            self.update_attribute("data-toggle", [data_toggle.value])
        if data_target:
            self.update_attribute("data-target", [f"#{data_target}"])
        if aria_expanded is True:
            self.update_attribute("aria-expanded", ['true'])
        elif aria_expanded is False:
            self.update_attribute("aria-expanded", ['false'])
        if aria_haspopup is True:
            self.update_attribute("aria-haspopup", ['true'])
        elif aria_haspopup is False:
            self.update_attribute("aria-haspopup", ['false'])
        if aria_controls:
            self.update_attribute("aria-controls", [aria_controls])
        self.content = content
        super(Button, self).__init__(tag='button', attrs=self.attrs, content=self.content, *args, **kwargs)


class ModalHeader(Tag):
    """
    This class renders the Bootstrap ModalHeader component.
    https://getbootstrap.com/docs/4.0/components/modal/
    """
    def __init__(self, content: str, heading_size: HeadingsEnum = HeadingsEnum.H5, closeable: bool = True, *args,
                 **kwargs):
        """
        :param content: the content of the header
        :param heading_size: the size of the content
        :param closeable: toggle to show or show not close button on header
        """
        self.attrs = {"class": ["modal-header"]}

        self.content = Tag(tag=heading_size.value, attrs={"class": ["modal-title"]}, content=content).render()
        if closeable:
            close_sym = Tag(tag='span', attrs={"aria-hidden": ["true"]}, content="&times;").render()
            self.content += Tag(tag='button',
                                attrs={"class": ["close"],
                                       "type": ["button"],
                                       "data-dismiss": ["modal"],
                                       "aria-label": ["Close"]},
                                content=close_sym, )

        super(ModalHeader, self).__init__(tag="div", attrs=self.attrs, content=self.content, *args, **kwargs)


class ModalBody(Tag):
    """
    This class renders the Bootstrap ModalBody component.
    https://getbootstrap.com/docs/4.0/components/modal/
    """
    def __init__(self, content: str, *args, **kwargs):
        """
        :param content: the content of the header
        :param heading_size: the size of the content
        :param closeable: toggle to show or show not close button on header
        """
        self.attrs = {"class": ["modal-body"]}
        self.content = content
        super(ModalBody, self).__init__(tag="div", attrs=self.attrs, content=self.content, *args, **kwargs)


class ModalFooter(Tag):
    """
    This class renders the Bootstrap ModalBody component.
    https://getbootstrap.com/docs/4.0/components/modal/
    """
    def __init__(self, content: str, *args, **kwargs):
        """
        :param content: the content of the header
        :param heading_size: the size of the content
        :param closeable: toggle to show or show not close button on header
        """
        self.attrs = {"class": ["modal-footer"]}
        self.content = content
        super(ModalFooter, self).__init__(tag="div", attrs=self.attrs, content=self.content, *args, **kwargs)


class Modal(BootstrapComponent):
    """
    This class renders the Bootstrap Modal component.
    https://getbootstrap.com/docs/4.0/components/modal/
    """
    def __init__(self, btn_content: str, header=None, body=None, btn_attrs: dict = None,
                 footer=None, fade: bool = True, size: ModalSizeEnum = None, fetch_url: str = None,
                 btn_tooltip: str = None, backdrop: bool = True, clos_on_esc: bool = True,
                 *args, **kwargs):
        """
        :param btn_content: the value of the button which opens the modal
        :param header: Optional: the title of the modal
        :param body: Optional: the body content of the modal
        :param btn_attrs: Optional: the dict which contains all attributes to update the button attributes
        :param btn_size: Optional: the size of the button which opens the modal
        :param footer: Optional: the footer content of the modal
        :param fade: Optional: toggles the fade flag
        :param size: Optional: the size of the modal
        :param fetch_url: Optional: the url where the content will be fetched from on modal shown event
        :param btn_tooltip: Optional: the tooltip of the modal toggle button
        :param args:
        :param kwargs:
        """
        super(Modal, self).__init__(template_name="modal.html", *args, **kwargs)
        self.modal_id = 'id_' + str(uuid.uuid4())
        if header and isinstance(header, str):
            self.header = ModalHeader(content=header)
            self.header.update_attribute(attribute="id", values=[f"{self.modal_id}_header"])
        elif header and isinstance(header, ModalHeader):
            self.header = header
        if body and isinstance(body, str):
            self.body = ModalBody(content=body)
            self.body.update_attribute(attribute="id", values=[f"{self.modal_id}_body"])
        elif body and isinstance(body, ModalBody):
            self.body = body
        if footer and isinstance(footer, str):
            self.footer = ModalFooter(content=footer)
            self.footer.update_attribute(attribute="id", values=[f"{self.modal_id}_footer"])
        elif footer and isinstance(footer, ModalFooter):
            self.footer = footer
        self.fade = fade
        self.size = size
        self.fetch_url = fetch_url
        self.backdrop = backdrop
        self.clos_on_esc = clos_on_esc
        self.button = Button(content=btn_content, data_toggle=DataToggleEnum.MODAL,
                             data_target=f'{self.modal_id}', tooltip=btn_tooltip)
        self.button.update_attributes(update_attrs=btn_attrs)
        self.rendered_button = None

    def render(self, safe: bool = False) -> str:
        """Renders a template with self.__dict__ as context

        :param safe: switches if the rendered component is returned as SafeString or str
        :return: rendered template as string | SafeString
        """
        self.rendered_button = self.button.render()
        return super().render(safe=safe)


class CardHeader(Tag):
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
        self.header_id = 'id_' + str(header_id) if header_id else 'id_' + str(uuid.uuid4())
        self.attrs = {"id": [self.header_id],
                      "class": ["card-header"]}
        if bg_color:
            self.update_attribute("class", [bg_color.value])
        if border:
            self.update_attribute("class", [border.value])
        if text_color:
            self.update_attribute("class", [text_color.value])
        self.content = content
        super(CardHeader, self).__init__(tag="div", attrs=self.attrs, content=self.content, *args, **kwargs)


class CardBody(Tag):
    """
    This class renders the Bootstrap Card Body component.
    https://getbootstrap.com/docs/4.0/components/card/#content-types
    """
    def __init__(self, content: str = None, body_id: uuid = None, bg_color: BackgroundColorEnum = None,
                 text_color: TextColorEnum = None, border: BorderColorEnum = None, fetch_url: str = None,
                 data_parent: str = None, aria_labelledby: str = None, *args, **kwargs):
        """
        :param content: Optional: the content of the card body
        :param body_id: Optional: the id of the body div
        :param bg_color: Optional: the background color of the card body
        :param text_color: Optional: the text color for all content in card body
        :param border: Optional: the border color of the card body
        :param fetch_url: Optional: is used from Modal class to set the fetch_url for this div
        :param data_parent: Optional: sets the data_parent attribute
        :param aria_labelledby: Optional: sets the aria_labelledby attribute
        :param args:
        :param kwargs:
        """
        self.body_id = 'id_' + str(body_id) if body_id else 'id_' + str(uuid.uuid4())
        self.attrs = {"id": [self.body_id],
                      "class": ["card-body"]}
        if bg_color:
            self.update_attribute("class", [bg_color.value])
        if border:
            self.update_attribute("class", [border.value])
        if text_color:
            self.update_attribute("class", [text_color.value])
        if fetch_url:
            self.update_attribute("data-url", [fetch_url])
        if data_parent:
            self.update_attribute("data-parent", [f"#{data_parent}"])
        if aria_labelledby:
            self.update_attribute("aria-labelledby", [aria_labelledby])
        self.content = content
        super(CardBody, self).__init__(tag="div", attrs=self.attrs, content=self.content, *args, **kwargs)


class CardFooter(Tag):
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
        self.attrs = {"class": ["card-footer"]}
        if bg_color:
            self.update_attribute("class", [bg_color.value])
        if border:
            self.update_attribute("class", [border.value])
        if text_color:
            self.update_attribute("class", [text_color.value])
        self.content = content
        super(CardFooter, self).__init__(tag="div", attrs=self.attrs, content=self.content, *args, **kwargs)


class Card(Tag):
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
        self.attrs = {"class": ["card"]}
        if bg_color:
            self.update_attribute("class", [bg_color.value])
        if border:
            self.update_attribute("class", [border.value])
        if text_color:
            self.update_attribute("class", [text_color.value])
        self.content = ''
        if header:
            self.content += header
        if body:
            self.content += body
        if footer:
            self.content += footer
        super(Card, self).__init__(tag="div", attrs=self.attrs, content=self.content, *args, **kwargs)


class Accordion(Tag):
    """
    This class renders the Bootstrap Accordion component.
    https://getbootstrap.com/docs/4.0/components/collapse/#accordion-example
    """
    def __init__(self, btn_value: str, content: str = None, fetch_url: str = None, header_center_content: str = None,
                 header_right_content: str = None, card_header_attrs: dict = None, card_body_attrs: dict = None,
                 card_attrs: dict = None, button_attrs: dict = None, *args, **kwargs):
        """
        :param btn_value: the value of the button to toggle the accordion
        :param content: the content of the accordion
        :param fetch_url: Optional: the url where the content will be fetched from on accordion shown event
        :param header_center_content: the content of the header center placed
        :param header_right_content: the content of the header right placed
        :param args:
        :param kwargs:
        """
        self.accordion_id = 'id_' + str(uuid.uuid4())
        if fetch_url:
            content = render_to_string("django_bootstrap_swt/includes/ajax_loading_spinner.html")
            content += render_to_string("django_bootstrap_swt/includes/ajax_error.html")
        self.card_body = CardBody(content=content,
                                  fetch_url=fetch_url,
                                  data_parent=self.accordion_id)
        self.card_body.update_attribute("class", ["collapse"])
        self.card_body.update_attributes(update_attrs=card_body_attrs)

        self.accordion_btn = Button(content=f'<i class="fa" aria-hidden="true"></i> {btn_value}',
                                    data_toggle=DataToggleEnum.COLLAPSE,
                                    data_target=self.card_body.body_id,
                                    aria_expanded=False,
                                    aria_controls=self.card_body.body_id)
        self.accordion_btn.update_attribute("class", ['collapsed', 'accordion', 'text-left'])
        self.accordion_btn.update_attributes(update_attrs=button_attrs)

        default_header_row = DefaultHeaderRow(content_left=self.accordion_btn.render(),
                                              content_center=header_center_content,
                                              content_right=header_right_content).render()

        self.card_header = CardHeader(content=default_header_row)
        self.card_header.update_attributes(update_attrs=card_header_attrs)

        self.card_body.update_attribute("aria-labelledby", [self.card_header.header_id])
        self.card = Card(header=self.card_header, body=self.card_body)
        self.card.update_attributes(update_attrs=card_attrs)

        self.attrs = {"id": [self.accordion_id],
                      "class": ["accordion"]}
        super(Accordion, self).__init__(tag="div", attrs=self.attrs, content=self.card.render(), *args, **kwargs)


class ButtonGroup(Tag):
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
        self.attrs = {"class": ["btn-group"],
                      "role": ["group"],
                      "aria-label": [aria_label], }
        content = ''
        for button in buttons:
            content += button
        super(ButtonGroup, self).__init__(tag="div", attrs=self.attrs, content=content, *args, **kwargs)


class Dropdown(TooltipSurroundedComponent):
    """
    This class renders the Bootstrap Dropdown component.
    https://getbootstrap.com/docs/4.0/components/dropdowns/
    """
    def __init__(self, btn_value: str, items: [Link], color: ButtonColorEnum = ButtonColorEnum.INFO, header: str = None,
                 btn_attrs: dict = None, *args, **kwargs):
        """
        :param btn_value: the value of the dropdown collapse button
        :param items: the items which should be placed in this dropdown
        :param color: the color of the dropdown collapse button
        :param header: sets one header on top of the dropdown
        :param args:
        :param kwargs:
        """
        super(Dropdown, self).__init__(tag="", template_name='dropdown.html', *args, **kwargs)
        self.value = btn_value
        self.color = color
        self.button = Button(content=btn_value, color=color,
                             data_toggle=DataToggleEnum.DROPDOWN, aria_haspopup=True, aria_expanded=False)
        self.button.update_attributes(update_attrs=btn_attrs)
        self.button.update_attribute("class", ['dropdown-toggle'])
        self.dropdown_id = self.button.button_id
        self.items = []
        for item in items:
            item.update_attribute("class", ["dropdown-item"])
            self.items.append(item.render())
        self.header = header


class ListGroupItem(Tag):
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
        self.attrs = {"class": ["list-group-item"], }
        self.content = content
        super(ListGroupItem, self).__init__(tag="li", attrs=self.attrs, content=self.content, *args, **kwargs)


class ListGroup(Tag):
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
        self.attrs = {"class": ["list-group"], }
        self.content = ''
        for item in items:
            self.content += item
        super(ListGroup, self).__init__(tag="ul", attrs=self.attrs, content=self.content, *args, **kwargs)


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
