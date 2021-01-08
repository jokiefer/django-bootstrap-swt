import uuid
from unittest import TestCase
from django.template.loader import render_to_string
from django.utils.safestring import SafeString
from django_bootstrap_swt.components import BootstrapComponent, ProgressBar, Badge, Tooltip, \
    TooltipSurroundedComponent, Modal, Accordion, LinkButton, Link, Button, ButtonGroup, Dropdown, ListGroupItem, \
    ListGroup, CardHeader, CardFooter, CardBody, Card, Tag, ModalFooter, ModalHeader, ModalBody
from django_bootstrap_swt.enums import ProgressColorEnum, BadgeColorEnum, ButtonColorEnum, \
    ButtonSizeEnum, ModalSizeEnum, TextColorEnum, DataToggleEnum, BackgroundColorEnum, BorderColorEnum, \
    TooltipPlacementEnum

MSG_TYPE_AFTER_CONCATENATING_WRONG = 'The type after concatenating is not str.'
MSG_STRING_CONTENT_WRONG_AFTER_CONCATENATING = 'The content of the string is wrong after concatenating.'
MSG_SUBCLASS_DOES_NOT_INHERIT_FROM_BOOTSTRAP_COMPONENT = 'The class "{}" does not inherit from "BootstrapComponent"'
MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT = 'The rendered string is not correct.'

BOOTSTRAP_COMPONENT_LIST = [Tooltip,
                            TooltipSurroundedComponent,
                            ProgressBar,
                            Badge,
                            Link,
                            Modal,
                            Accordion,
                            LinkButton,
                            Button,
                            ButtonGroup,
                            Dropdown,
                            ListGroupItem,
                            ListGroup,
                            Card,
                            CardBody,
                            CardFooter,
                            CardHeader,
                            Tooltip,
                            Tag]


class StringDiffTestCase(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None


class TestBoostrapComponent(TestCase):
    """ This class contains all needed tests for testing BoostrapComponent class
    """

    def setUp(self) -> None:
        self.bootstrap_component = BootstrapComponent(path_to_templates='', template_name='dummy.html')
        self.test_string = 'some string'
        self.dummy_content = 'dummy template contents'  # this is the content of the templates/dummy.html file

    def test_magic_repr(self):
        self.assertEqual(first=self.dummy_content, second=self.bootstrap_component.__repr__())

    def test_magic_add(self):
        new_string = self.bootstrap_component + self.test_string
        self.assertIsInstance(obj=new_string, cls=str,
                              msg=MSG_TYPE_AFTER_CONCATENATING_WRONG)
        self.assertEqual(first=self.dummy_content + self.test_string, second=new_string,
                         msg=MSG_STRING_CONTENT_WRONG_AFTER_CONCATENATING)

    def test_magic_radd(self):
        new_string = self.test_string + self.bootstrap_component
        self.assertIsInstance(obj=new_string, cls=str,
                              msg=MSG_TYPE_AFTER_CONCATENATING_WRONG)
        self.assertEqual(first=self.test_string + self.dummy_content, second=new_string,
                         msg=MSG_STRING_CONTENT_WRONG_AFTER_CONCATENATING)

    def test_magic_iadd(self):
        new_string = self.test_string
        new_string += self.bootstrap_component
        self.assertIsInstance(obj=new_string, cls=str,
                              msg=MSG_TYPE_AFTER_CONCATENATING_WRONG)

        first = self.test_string
        first += self.dummy_content
        self.assertEqual(first=first, second=new_string,
                         msg=MSG_STRING_CONTENT_WRONG_AFTER_CONCATENATING)

    def test_render(self):
        rendered_string = self.bootstrap_component.render()
        self.assertIsInstance(obj=rendered_string, cls=str)
        self.assertEqual(first=self.dummy_content, second=rendered_string)

        rendered_string = self.bootstrap_component.render(safe=False)
        self.assertIsInstance(obj=rendered_string, cls=str)
        self.assertEqual(first=self.dummy_content, second=rendered_string)

        rendered_safe_string = self.bootstrap_component.render(safe=True)
        self.assertIsInstance(obj=rendered_safe_string, cls=SafeString)
        self.assertEqual(first=self.dummy_content, second=rendered_safe_string)


class TestInheritance(TestCase):
    """ This class contains all needed tests for testing inheritance of super classes.
    """

    def test_inheritance_of_bootstrap_components(self):
        for Component in BOOTSTRAP_COMPONENT_LIST:
            self.assertTrue(expr=issubclass(Component, BootstrapComponent),
                            msg=MSG_SUBCLASS_DOES_NOT_INHERIT_FROM_BOOTSTRAP_COMPONENT.format(Component.__name__))


class TestProgressBar(StringDiffTestCase):
    """ This class contains all needed tests for testing ProgressBar class
    """

    def test_rendering_with_progress_argument(self):
        progress_bar = ProgressBar(progress=20).render(safe=True)
        expr = render_to_string(template_name='components/progressbar/test_progress_20.html', context={})
        self.assertMultiLineEqual(first=progress_bar, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_color_argument(self):
        progress_bar = ProgressBar(color=ProgressColorEnum.DANGER).render(safe=True)
        expr = render_to_string(template_name='components/progressbar/test_color_danger.html', context={})
        self.assertMultiLineEqual(first=progress_bar, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_animated_argument(self):
        progress_bar = ProgressBar(animated=False).render(safe=True)
        expr = render_to_string(template_name='components/progressbar/test_animated_false.html', context={})
        self.assertMultiLineEqual(first=progress_bar, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_striped_argument(self):
        progress_bar = ProgressBar(striped=False).render(safe=True)
        expr = render_to_string(template_name='components/progressbar/test_striped_false.html', context={})
        self.assertMultiLineEqual(first=progress_bar, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)


class TestBadge(StringDiffTestCase):
    """ This class contains all needed tests for testing Badge class
    """

    def test_rendering_with_color_argument(self):
        badge = Badge(content='1234', color=BadgeColorEnum.PRIMARY).render(safe=True)
        expr = render_to_string(template_name='components/badge/test_badge_color_primary.html', context={})
        self.assertMultiLineEqual(first=badge, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_pill_argument(self):
        badge = Badge(content='1234', pill=True).render(safe=True)
        expr = render_to_string(template_name='components/badge/test_badge_pill_true.html', context={})
        self.assertMultiLineEqual(first=badge, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)


class TestLink(StringDiffTestCase):
    """ This class contains all needed tests for testing Link class
    """

    def test_rendering_with_color_argument(self):
        first = Link(url='http://example.com', content='http://example.com', color=TextColorEnum.SUCCESS, ).render(
            safe=True)
        expr = render_to_string(template_name='components/link/test_link_color_success.html', context={})
        self.assertMultiLineEqual(first=first, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_dropdown_item_argument(self):
        first = Link(url='http://example.com', content='http://example.com', dropdown_item=True, ).render(
            safe=True)
        expr = render_to_string(template_name='components/link/test_link_dropdown_item_true.html', context={})
        self.assertMultiLineEqual(first=first, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_open_in_new_tab_argument(self):
        first = Link(url='http://example.com', content='http://example.com', open_in_new_tab=True, ).render(
            safe=True)
        expr = render_to_string(template_name='components/link/test_link_open_in_new_tab_true.html', context={})
        self.assertMultiLineEqual(first=first, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)


class TestLinkButton(StringDiffTestCase):
    """ This class contains all needed tests for testing LinkButton class
    """

    def test_rendering_with_color_argument(self):
        first = LinkButton(url='http://example.com', content='http://example.com', color=ButtonColorEnum.SUCCESS,
                           size=ButtonSizeEnum.SMALL).render(safe=True)
        expr = render_to_string(template_name='components/linkbutton/test_linkbutton_size_small.html', context={})
        self.assertMultiLineEqual(first=first, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)


class TestButton(StringDiffTestCase):
    """ This class contains all needed tests for testing Button class
    """

    def test_rendering_with_color_argument(self):
        first = Button(content='nice button', color=ButtonColorEnum.SUCCESS, size=ButtonSizeEnum.SMALL)
        expr = render_to_string(template_name='components/button/test_button_size_small.html',
                                context={"button_id": first.button_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_data_toggle_argument(self):
        first = Button(content='nice button', color=ButtonColorEnum.SUCCESS, data_toggle=DataToggleEnum.MODAL)
        expr = render_to_string(template_name='components/button/test_button_data_toggle_modal.html',
                                context={"button_id": first.button_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_data_target_argument(self):
        first = Button(content='nice button', color=ButtonColorEnum.SUCCESS, data_target='modal')
        expr = render_to_string(template_name='components/button/test_button_data_target_modal.html',
                                context={"button_id": first.button_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_area_expand_argument(self):
        first = Button(content='nice button', color=ButtonColorEnum.SUCCESS, aria_expanded=True)
        expr = render_to_string(template_name='components/button/test_button_aria_expanded_true.html',
                                context={"button_id": first.button_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_area_controls_argument(self):
        first = Button(content='nice button', color=ButtonColorEnum.SUCCESS, aria_controls='modal')
        expr = render_to_string(template_name='components/button/test_button_aria_controls_modal.html',
                                context={"button_id": first.button_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)


class TestModalHeader(StringDiffTestCase):
    """ This class contains all needed tests for testing ModalHeader class
    """
    def test_rendering_with_closeable_argument(self):
        first = ModalHeader(content="nice header", closeable=False)
        expr = render_to_string(template_name='components/modal_header/test_modal_header_closeable_false.html')
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)


class TestModal(StringDiffTestCase):
    """ This class contains all needed tests for testing Modal class
    """

    def test_rendering_with_modal_header_str_argument(self):
        first = Modal(title='nice modal', btn_content='nice button',
                      btn_attrs={"class": [ButtonColorEnum.SUCCESS.value]}, header='nice header')
        expr = render_to_string(template_name='components/modal/test_modal_header_str.html',
                                context={"modal_id": first.modal_id,
                                         "button": first.button})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_modal_header_ModalHeader_argument(self):
        header = ModalHeader(content="nice header")
        first = Modal(title='nice modal', btn_content='nice button',
                      btn_attrs={"class": [ButtonColorEnum.SUCCESS.value]}, header=header)
        expr = render_to_string(template_name='components/modal/test_modal_header_ModalHeader.html',
                                context={"modal_id": first.modal_id,
                                         "button": first.button})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_modal_body_str_argument(self):
        first = Modal(title='nice modal', btn_content='nice button',
                      btn_attrs={"class": [ButtonColorEnum.SUCCESS.value]}, body='nice body')
        expr = render_to_string(template_name='components/modal/test_modal_body_str.html',
                                context={"modal_id": first.modal_id,
                                         "button": first.button})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_modal_body_ModalBody_argument(self):
        body = ModalBody(content="nice body")
        first = Modal(title='nice modal', btn_content='nice button',
                      btn_attrs={"class": [ButtonColorEnum.SUCCESS.value]}, body=body)
        expr = render_to_string(template_name='components/modal/test_modal_body_ModalBody.html',
                                context={"modal_id": first.modal_id,
                                         "button": first.button})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_modal_footer_str_argument(self):
        first = Modal(title='nice modal', btn_content='nice button',
                      btn_attrs={"class": [ButtonColorEnum.SUCCESS.value]}, footer='nice footer')
        expr = render_to_string(template_name='components/modal/test_modal_footer_str.html',
                                context={"modal_id": first.modal_id,
                                         "button": first.button})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_modal_footer_ModelFooter_argument(self):
        footer = ModalFooter(content="nice footer")
        first = Modal(title='nice modal', btn_content='nice button',
                      btn_attrs={"class": [ButtonColorEnum.SUCCESS.value]}, footer=footer)
        expr = render_to_string(template_name='components/modal/test_modal_footer_ModalFooter.html',
                                context={"modal_id": first.modal_id,
                                         "button": first.button})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_fade_argument(self):
        first = Modal(title='nice modal', btn_content='nice button',
                      btn_attrs={"class": [ButtonColorEnum.SUCCESS.value]}, fade=False)
        expr = render_to_string(template_name='components/modal/test_modal_fade_false.html',
                                context={"modal_id": first.modal_id,
                                         "button": first.button})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_backdrop_argument(self):
        first = Modal(title='nice modal', btn_content='nice button',
                      btn_attrs={"class": [ButtonColorEnum.SUCCESS.value]}, backdrop=False)
        expr = render_to_string(template_name='components/modal/test_modal_backdrop_false.html',
                                context={"modal_id": first.modal_id,
                                         "button": first.button})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_close_on_esc_argument(self):
        first = Modal(title='nice modal', btn_content='nice button',
                      btn_attrs={"class": [ButtonColorEnum.SUCCESS.value]}, clos_on_esc=False)
        expr = render_to_string(template_name='components/modal/test_modal_close_on_esc_false.html',
                                context={"modal_id": first.modal_id,
                                         "button": first.button})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_size_argument(self):
        first = Modal(title='nice modal', body='something', btn_content='nice button',
                      btn_attrs={"class": [ButtonColorEnum.SUCCESS.value, ]},
                      size=ModalSizeEnum.LARGE)
        expr = render_to_string(template_name='components/modal/test_modal_size_large.html',
                                context={"modal_id": first.modal_id,
                                         "button": first.button})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_fetch_url_argument(self):
        first = Modal(title='nice modal', btn_content='nice button',
                      btn_attrs={"class": [ButtonColorEnum.SUCCESS.value]}, fetch_url='http://example.com')
        expr = render_to_string(template_name='components/modal/test_modal_fetch_url.html',
                                context={"modal_id": first.modal_id,
                                         "button": first.button})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_btn_tooltip_argument(self):
        first = Modal(title='nice modal', btn_content='nice button', btn_tooltip='nice tooltip')
        expr = render_to_string(template_name='components/modal/test_modal_btn_tooltip.html',
                                context={"modal_id": first.modal_id,
                                         "button": first.button})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)


class TestCardHeader(StringDiffTestCase):
    """ This class contains all needed tests for testing CardHeader class
    """

    def test_rendering_with_header_id(self):
        header_id = uuid.uuid4()
        first = CardHeader(content='nice header', header_id=header_id)
        expr = render_to_string(template_name='components/card/header/test_card_header_header_id.html',
                                context={"header_id": 'id_' + str(header_id)})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_bg_color(self):
        first = CardHeader(content='nice header', bg_color=BackgroundColorEnum.SUCCESS)
        expr = render_to_string(template_name='components/card/header/test_card_header_bg_color_success.html',
                                context={"header_id": first.header_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_text_color(self):
        first = CardHeader(content='nice header', text_color=TextColorEnum.SUCCESS)
        expr = render_to_string(template_name='components/card/header/test_card_header_text_color_success.html',
                                context={"header_id": first.header_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_border_color(self):
        first = CardHeader(content='nice header', border=BorderColorEnum.SUCCESS)
        expr = render_to_string(template_name='components/card/header/test_card_header_border_color_success.html',
                                context={"header_id": first.header_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)


class TestCardFooter(StringDiffTestCase):
    """ This class contains all needed tests for testing CardFooter class
    """

    def test_rendering_with_bg_color(self):
        first = CardFooter(content='nice footer', bg_color=BackgroundColorEnum.SUCCESS)
        expr = render_to_string(template_name='components/card/footer/test_card_footer_bg_color_success.html',
                                context={})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_text_color(self):
        first = CardFooter(content='nice footer', text_color=TextColorEnum.SUCCESS)
        expr = render_to_string(template_name='components/card/footer/test_card_footer_text_color_success.html',
                                context={})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_border_color(self):
        first = CardFooter(content='nice footer', border=BorderColorEnum.SUCCESS)
        expr = render_to_string(template_name='components/card/footer/test_card_footer_border_color_success.html',
                                context={})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)


class TestCardBody(StringDiffTestCase):
    """ This class contains all needed tests for testing CardBody class
    """

    def test_rendering_with_body_id(self):
        body_id = uuid.uuid4()
        first = CardBody(content='nice body', body_id=body_id)
        expr = render_to_string(template_name='components/card/body/test_card_body_body_id.html',
                                context={"body_id": 'id_' + str(body_id)})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_bg_color(self):
        first = CardBody(content='nice body', bg_color=BackgroundColorEnum.SUCCESS)
        expr = render_to_string(template_name='components/card/body/test_card_body_bg_color_success.html',
                                context={"body_id": first.body_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_text_color(self):
        first = CardBody(content='nice body', text_color=TextColorEnum.SUCCESS)
        expr = render_to_string(template_name='components/card/body/test_card_body_text_color_success.html',
                                context={"body_id": first.body_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_border_color(self):
        first = CardBody(content='nice body', border=BorderColorEnum.SUCCESS)
        expr = render_to_string(template_name='components/card/body/test_card_body_border_color_success.html',
                                context={"body_id": first.body_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_fetch_url(self):
        first = CardBody(content='nice body', fetch_url='http://example.com')
        expr = render_to_string(template_name='components/card/body/test_card_body_fetch_url.html',
                                context={"body_id": first.body_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_data_parent(self):
        first = CardBody(content='nice body', data_parent='id_1234')
        expr = render_to_string(template_name='components/card/body/test_card_body_data_parent.html',
                                context={"body_id": first.body_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_aria_labelledby(self):
        first = CardBody(content='nice body', aria_labelledby='id_1234')
        expr = render_to_string(template_name='components/card/body/test_card_body_aria_labelledby.html',
                                context={"body_id": first.body_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)


class TestCard(StringDiffTestCase):
    """ This class contains all needed tests for testing Card class
    """

    def setUp(self) -> None:
        super(TestCard, self).setUp()
        self.header = CardHeader(content='nice header')
        self.body = CardBody(content='nice body')
        self.footer = CardFooter(content='nice footer')

    def test_rendering_with_header_argument(self):
        first = Card(body=self.body, header=self.header)
        expr = render_to_string(template_name='components/card/card/test_card_with_header.html',
                                context={"header_id": self.header.header_id,
                                         "body_id": self.body.body_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_footer_argument(self):
        first = Card(body=self.body, footer=self.footer)
        expr = render_to_string(template_name='components/card/card/test_card_with_footer.html',
                                context={"body_id": self.body.body_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_bg_color_argument(self):
        first = Card(body=self.body, bg_color=BackgroundColorEnum.SUCCESS)
        expr = render_to_string(template_name='components/card/card/test_card_bg_color_success.html',
                                context={"body_id": self.body.body_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_text_color_argument(self):
        first = Card(body=self.body, text_color=TextColorEnum.SUCCESS)
        expr = render_to_string(template_name='components/card/card/test_card_text_color_success.html',
                                context={"body_id": self.body.body_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_border_color_argument(self):
        first = Card(body=self.body, border=BorderColorEnum.SUCCESS)
        expr = render_to_string(template_name='components/card/card/test_card_border_color_success.html',
                                context={"body_id": self.body.body_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)


class TestAccordion(StringDiffTestCase):
    """ This class contains all needed tests for testing Accordion class
    """

    def setUp(self) -> None:
        super(TestAccordion, self).setUp()
        self.header = CardHeader(content='nice header')
        self.body = CardBody(content='nice body')
        self.footer = CardFooter(content='nice footer')

    def test_rendering_with_content_argument(self):
        first = Accordion(btn_value='nice button', content='nice body')
        expr = render_to_string(template_name='components/accordion/test_accordion_with_content.html',
                                context={"accordion_id": first.accordion_id,
                                         "card_header_id": first.card_header.header_id,
                                         "card_body_id": first.card_body.body_id,
                                         "button_id": first.accordion_btn.button_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_fetch_url_argument(self):
        first = Accordion(btn_value='nice button', fetch_url='http://example.com')
        expr = render_to_string(template_name='components/accordion/test_accordion_fetch_url.html',
                                context={"accordion_id": first.accordion_id,
                                         "card_header_id": first.card_header.header_id,
                                         "card_body_id": first.card_body.body_id,
                                         "button_id": first.accordion_btn.button_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_card_header_attrs_argument(self):
        first = Accordion(btn_value='nice button', card_header_attrs={"class": [TextColorEnum.SUCCESS.value]})
        expr = render_to_string(template_name='components/accordion/test_accordion_card_header_attrs.html',
                                context={"accordion_id": first.accordion_id,
                                         "card_header_id": first.card_header.header_id,
                                         "card_body_id": first.card_body.body_id,
                                         "button_id": first.accordion_btn.button_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_card_body_attrs_argument(self):
        first = Accordion(btn_value='nice button', card_body_attrs={"class": [TextColorEnum.SUCCESS.value]})
        expr = render_to_string(template_name='components/accordion/test_accordion_card_body_attrs.html',
                                context={"accordion_id": first.accordion_id,
                                         "card_header_id": first.card_header.header_id,
                                         "card_body_id": first.card_body.body_id,
                                         "button_id": first.accordion_btn.button_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_card_attrs_argument(self):
        first = Accordion(btn_value='nice button', card_attrs={"class": [TextColorEnum.SUCCESS.value]})
        expr = render_to_string(template_name='components/accordion/test_accordion_card_attrs.html',
                                context={"accordion_id": first.accordion_id,
                                         "card_header_id": first.card_header.header_id,
                                         "card_body_id": first.card_body.body_id,
                                         "button_id": first.accordion_btn.button_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)


class TestButtonGroup(StringDiffTestCase):
    """ This class contains all needed tests for testing ButtonGroup class
    """
    def test_rendering(self):
        button = Button(content='nice button')
        link_button = LinkButton(url='http://example.com', content='nice linkbutton', color=ButtonColorEnum.SUCCESS)
        first = ButtonGroup(aria_label='nice_buttons', buttons=[button, link_button])
        expr = render_to_string(template_name='components/buttongroup/test_button_group.html',
                                context={"button_id": button.button_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)


class TestDropdown(StringDiffTestCase):
    """ This class contains all needed tests for testing Dropdown class
    """
    def test_rendering_with_color_argument(self):
        link = Link(url='http://example.com', content='nice link')
        first = Dropdown(btn_value='nice dropdown', items=[link, ], color=ButtonColorEnum.SUCCESS)
        expr = render_to_string(template_name='components/dropdown/test_dropdown_color_success.html',
                                context={"dropdown_id": first.dropdown_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_header_argument(self):
        link = Link(url='http://example.com', content='nice link')
        first = Dropdown(btn_value='nice dropdown', items=[link, ], header='nice header')
        expr = render_to_string(template_name='components/dropdown/test_dropdown_header.html',
                                context={"dropdown_id": first.dropdown_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)


class TestListGroupItem(StringDiffTestCase):
    """ This class contains all needed tests for testing ListGroupItem class
    """
    def test_rendering(self):
        first = ListGroupItem(content='nice item')
        expr = render_to_string(template_name='components/listgroup/test_listgroupitem.html')
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)


class TestListGroup(StringDiffTestCase):
    """ This class contains all needed tests for testing ListGroup class
    """
    def test_rendering(self):
        item = ListGroupItem(content='nice item')
        first = ListGroup(items=[item, ])
        expr = render_to_string(template_name='components/listgroup/test_listgroup.html')
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)


class TestTooltip(StringDiffTestCase):
    """ This class contains all needed tests for testing Tooltip class
    """
    def test_rendering(self):
        first = Tooltip(title='nice tooltip', surrounded_component='nice component', placement=TooltipPlacementEnum.TOP)
        expr = render_to_string(template_name='components/tooltip/test_tooltip.html')
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)


class TestTag(StringDiffTestCase):
    """ This class contains all needed tests for testing Tooltip class
    """
    def test_update_attribute_extend_without_duplicates(self):
        tag = Tag(tag='div', attrs={'class': ['class-1', 'class-2']})
        tag.update_attribute('class', ['class-3'])
        self.assertEqual(tag.attrs['class'], ['class-1', 'class-2', 'class-3'])

    def test_update_attribute_extend_with_duplicates(self):
        tag = Tag(tag='div', attrs={'class': ['class-1', 'class-2']})
        tag.update_attribute('class', ['class-3', 'class-2'])
        self.assertEqual(tag.attrs['class'], ['class-1', 'class-2', 'class-3'])

    def test_update_attribute_extend_with_new_attribute(self):
        tag = Tag(tag='div', attrs={'class': ['class-1', 'class-2']})
        tag.update_attribute('new_attr', ['value-1'])
        self.assertEqual(tag.attrs['new_attr'], ['value-1'])

    def test_update_attributes(self):
        tag = Tag(tag='div', attrs={'class': ['class-1', 'class-2']})
        tag.update_attributes({'new_attr': ['value-1']})
        self.assertEqual(tag.attrs, {'class': ['class-1', 'class-2'],
                                     'new_attr': ['value-1']})

    def test_rendering_of_icon(self):
        first = Tag(tag='i', attrs={'class': ['fab', 'fa-accessible-icon']})
        expr = render_to_string(template_name='components/tag/test_tag_icon.html')
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_of_disabled_icon(self):
        first = Tag(tag='i', attrs={'class': ['fab', 'fa-accessible-icon'], 'disabled': {}})
        expr = render_to_string(template_name='components/tag/test_tag_icon_disabled.html')
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)
