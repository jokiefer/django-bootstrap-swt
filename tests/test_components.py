from unittest import TestCase
from django.template.loader import render_to_string
from django.utils.safestring import SafeString
from django_bootstrap_swt.components import BootstrapComponent, ProgressBar, Badge
from django_bootstrap_swt.enums import ProgressColorEnum, BadgeColorEnum

MSG_TYPE_AFTER_CONCATENATING_WRONG = 'The type after concatenating is not str.'
MSG_STRING_CONTENT_WRONG_AFTER_CONCATENATING = 'The content of the string is wrong after concatenating.'
MSG_SUBCLASS_DOES_NOT_INHERIT_FROM_BOOTSTRAP_COMPONENT = 'The class "{}" does not inherit from "BootstrapComponent"'
MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT = 'The rendered string is not correct.'


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


class TestProgressBar(TestCase):
    """ This class contains all needed tests for testing ProgressBar class
    """

    def test_inheritance_of_bootstrap_components(self):
        self.assertTrue(expr=issubclass(ProgressBar, BootstrapComponent),
                        msg=MSG_SUBCLASS_DOES_NOT_INHERIT_FROM_BOOTSTRAP_COMPONENT.format('ProgressBar'))

    def test_rendering_with_progress_argument(self):
        progress_bar = ProgressBar(progress=20).render(safe=True)
        expr = render_to_string(template_name='components/progressbar/test_progress_20.html', context={})
        self.assertEqual(first=progress_bar, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_color_argument(self):
        progress_bar = ProgressBar(color=ProgressColorEnum.DANGER).render(safe=True)
        expr = render_to_string(template_name='components/progressbar/test_color_danger.html', context={})
        self.assertEqual(first=progress_bar, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_animated_argument(self):
        progress_bar = ProgressBar(animated=False).render(safe=True)
        expr = render_to_string(template_name='components/progressbar/test_animated_false.html', context={})
        self.assertEqual(first=progress_bar, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_striped_argument(self):
        progress_bar = ProgressBar(striped=False).render(safe=True)
        expr = render_to_string(template_name='components/progressbar/test_striped_false.html', context={})
        self.assertEqual(first=progress_bar, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)


class TestBadge(TestCase):
    """ This class contains all needed tests for testing Badge class
    """

    def test_inheritance_of_bootstrap_components(self):
        self.assertTrue(expr=issubclass(Badge, BootstrapComponent),
                        msg=MSG_SUBCLASS_DOES_NOT_INHERIT_FROM_BOOTSTRAP_COMPONENT.format('Badge'))

    def test_rendering_with_color_argument(self):
        badge = Badge(value='1234', color=BadgeColorEnum.PRIMARY).render(safe=True)
        expr = render_to_string(template_name='components/badge/test_badge_color_primary.html', context={})
        self.assertEqual(first=badge, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_pill_argument(self):
        badge = Badge(value='1234', pill=True).render(safe=True)
        expr = render_to_string(template_name='components/badge/test_badge_pill_true.html', context={})
        self.assertEqual(first=badge, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)

    def test_rendering_with_tooltip_argument(self):
        badge = Badge(value='1234', tooltip='nice tooltip').render(safe=True)
        expr = render_to_string(template_name='components/badge/test_badge_tooltip.html', context={})
        self.assertEqual(first=badge, second=expr, msg=MSG_RENDERED_TEMPLATE_IS_NOT_CORRECT)
