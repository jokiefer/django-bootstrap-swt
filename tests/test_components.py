import unittest

from django.utils.safestring import SafeString

from django_bootstrap_swt.components import BootstrapComponent

MSG_TYPE_AFTER_CONCATENATING_WRONG = 'The type after concatenating is not str.'
MSG_STRING_CONTENT_WRONG_AFTER_CONCATENATING = 'The content of the string is wrong after concatenating.'


class TestBoostrapComponent(unittest.TestCase):
    """ This class contains all needed tests for testing BoostrapComponent class
    """

    def setUp(self) -> None:
        self.bootstrap_component = BootstrapComponent(path_to_templates='', template_name='dummy.html')
        self.test_string = 'some string'
        self.dummy_content = 'dummy template contents'  # this is the content of the templates/dummy.html file

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
