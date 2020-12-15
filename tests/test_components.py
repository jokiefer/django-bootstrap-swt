from unittest import TestCase
from django.template.loader import render_to_string
from django.utils.safestring import SafeString
from django_bootstrap_swt.components import BootstrapComponent, ProgressBar, Badge, Tooltip, TooltipSouroundedComponent, \
    Modal, Accordion, LinkButton, Link, Button, ButtonGroup, Dropdown, LeafletClient, ListGroupItem, \
    ListGroup
from django_bootstrap_swt.enums import ProgressColorEnum, BadgeColorEnum, ButtonColorEnum, \
    ButtonSizeEnum, ModalSizeEnum, TextColorEnum, DataToggleEnum

MSG_TYPE_AFTER_CONCATENATING_WRONG = 'The type after concatenating is not str.'
MSG_STRING_CONTENT_WRONG_AFTER_CONCATENATING = 'The content of the string is wrong after concatenating.'
MSG_SUBCLASS_DOES_NOT_INHERIT_FROM_BOOTSTRAP_COMPONENT = 'The class "{}" does not inherit from "BootstrapComponent"'
MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT = 'The rendered string is not correct.'


BOOTSTRAP_COMPONENT_LIST = [Tooltip,
                            TooltipSouroundedComponent,
                            ProgressBar,
                            Badge,
                            Link,
                            Modal,
                            Accordion,
                            LinkButton,
                            Button,
                            ButtonGroup,
                            Dropdown,
                            LeafletClient,
                            ListGroupItem,
                            ListGroup]


class StringDiffTestCase(TestCase):
    def setUp(self) -> None:
        self.maxDiff = 1000


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
        self.assertEqual(first=self.dummy_content+self.test_string, second=new_string,
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
        badge = Badge(value='1234', color=BadgeColorEnum.PRIMARY).render(safe=True)
        expr = render_to_string(template_name='components/badge/test_badge_color_primary.html', context={})
        self.assertMultiLineEqual(first=badge, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_pill_argument(self):
        badge = Badge(value='1234', pill=True).render(safe=True)
        expr = render_to_string(template_name='components/badge/test_badge_pill_true.html', context={})
        self.assertMultiLineEqual(first=badge, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)


class TestLink(StringDiffTestCase):
    """ This class contains all needed tests for testing Link class
    """

    def test_rendering_with_color_argument(self):
        first = Link(url='http://example.com', value='http://example.com', color=TextColorEnum.SUCCESS, ).render(safe=True)
        expr = render_to_string(template_name='components/link/test_link_color_success.html', context={})
        self.assertMultiLineEqual(first=first, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_dropdown_item_argument(self):
        first = Link(url='http://example.com', value='http://example.com', dropdown_item=True, ).render(
            safe=True)
        expr = render_to_string(template_name='components/link/test_link_dropdown_item_true.html', context={})
        self.assertMultiLineEqual(first=first, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_open_in_new_tab_argument(self):
        first = Link(url='http://example.com', value='http://example.com', open_in_new_tab=True, ).render(
            safe=True)
        expr = render_to_string(template_name='components/link/test_link_open_in_new_tab_true.html', context={})
        self.assertMultiLineEqual(first=first, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)


class TestLinkButton(StringDiffTestCase):
    """ This class contains all needed tests for testing LinkButton class
    """

    def test_rendering_with_color_argument(self):
        first = LinkButton(url='http://example.com', value='http://example.com', color=ButtonColorEnum.SUCCESS,
                           size=ButtonSizeEnum.SMALL).render(safe=True)
        expr = render_to_string(template_name='components/linkbutton/test_linkbutton_size_small.html', context={})
        self.assertMultiLineEqual(first=first, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)


class TestButton(StringDiffTestCase):
    """ This class contains all needed tests for testing Button class
    """

    def test_rendering_with_color_argument(self):
        first = Button(value='nice button', color=ButtonColorEnum.SUCCESS, size=ButtonSizeEnum.SMALL).render(safe=True)
        expr = render_to_string(template_name='components/button/test_button_size_small.html', context={})
        self.assertMultiLineEqual(first=first, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_data_toggle_argument(self):
        first = Button(value='nice button', color=ButtonColorEnum.SUCCESS, data_toggle=DataToggleEnum.MODAL).render(safe=True)
        expr = render_to_string(template_name='components/button/test_button_data_toggle_modal.html', context={})
        self.assertMultiLineEqual(first=first, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_data_target_argument(self):
        first = Button(value='nice button', color=ButtonColorEnum.SUCCESS, data_target='modal').render(safe=True)
        expr = render_to_string(template_name='components/button/test_button_data_target_modal.html', context={})
        self.assertMultiLineEqual(first=first, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_area_expand_argument(self):
        first = Button(value='nice button', color=ButtonColorEnum.SUCCESS, aria_expanded=True).render(safe=True)
        expr = render_to_string(template_name='components/button/test_button_aria_expanded_true.html', context={})
        self.assertMultiLineEqual(first=first, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_area_controls_argument(self):
        first = Button(value='nice button', color=ButtonColorEnum.SUCCESS, aria_controls='modal').render(safe=True)
        expr = render_to_string(template_name='components/button/test_button_aria_controls_modal.html', context={})
        self.assertMultiLineEqual(first=first, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)


class TestModal(StringDiffTestCase):
    """ This class contains all needed tests for testing Modal class
    """

    def test_rendering_with_modal_footer_argument(self):
        first = Modal(title='nice modal', body='something', btn_value='nice button',
                      btn_color=ButtonColorEnum.SUCCESS, footer='nice footer')
        expr = render_to_string(template_name='components/modal/test_modal_footer.html',
                                context={"modal_id": first.modal_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_fade_argument(self):
        first = Modal(title='nice modal', body='something', btn_value='nice button',
                      btn_color=ButtonColorEnum.SUCCESS, fade=False)
        expr = render_to_string(template_name='components/modal/test_modal_fade_false.html',
                                context={"modal_id": first.modal_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_size_argument(self):
        first = Modal(title='nice modal', body='something', btn_value='nice button',
                      btn_color=ButtonColorEnum.SUCCESS, size=ModalSizeEnum.LARGE)
        expr = render_to_string(template_name='components/modal/test_modal_size_large.html',
                                context={"modal_id": first.modal_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_fetch_url_argument(self):
        first = Modal(title='nice modal', body='something', btn_value='nice button',
                      btn_color=ButtonColorEnum.SUCCESS, fetch_url='http://example.com')
        expr = render_to_string(template_name='components/modal/test_modal_fetch_url.html',
                                context={"modal_id": first.modal_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)


class TestCard(StringDiffTestCase):
    # todo
    pass


class TestAccordion(StringDiffTestCase):
    """ This class contains all needed tests for testing Accordion class
    """

    def test_rendering_with_accordion_title_center_argument(self):
        return
        # todo:
        first = Accordion(accordion_title='nice accordion', accordion_title_center='nice center')
        expr = render_to_string(template_name='components/modal/test_accordion_center.html',
                                context={"accordion_id": first.accordion_id})
        self.assertMultiLineEqual(first=first.render(safe=True), second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)
