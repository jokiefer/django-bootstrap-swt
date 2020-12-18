from unittest import TestCase
from django.test import RequestFactory

from django_bootstrap_swt.components import Link, Badge
from django_bootstrap_swt.utils import RenderHelper


class TestRenderHelper(TestCase):
    """ This class contains all needed tests for testing TestRenderHelper class
    """

    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.request = self.factory.get('http://example.com', )

    def test_init_with_user_permissions_arg(self):
        user_perms = ['test_perm_1', 'test_perm_2']
        render_helper = RenderHelper(request=self.request, user_permissions=['test_perm_1', 'test_perm_2'])

        self.assertEqual(first=self.request, second=render_helper.request)
        self.assertEqual(first=user_perms, second=render_helper.user_permissions)

    def test_init_without_user_permissions_arg(self):
        render_helper = RenderHelper(request=self.request)

        self.assertEqual(first=self.request, second=render_helper.request)
        self.assertEqual(first=[], second=render_helper.user_permissions)

    def test__check_render_permission_user_perm_empty_not_needs_perm(self):
        render_helper = RenderHelper(request=self.request)
        has_perm = render_helper._check_render_permission(
            item=Link(url='http://example.com', value='http://example.com'))
        self.assertTrue(has_perm)

    def test__check_render_permission_user_perm_empty_needs_perm(self):
        render_helper = RenderHelper(request=self.request)
        item = Link(url='http://example.com', value='http://example.com', needs_perm='some_perm')
        has_perm = render_helper._check_render_permission(item=item)

        self.assertFalse(has_perm)

    def test__check_render_permission_user_perm_needs_perm(self):
        render_helper = RenderHelper(request=self.request, user_permissions=['some_perm', 'some_perm2'])
        has_perm = render_helper._check_render_permission(
            item=Link(url='http://example.com', value='http://example.com'))
        self.assertTrue(has_perm)

    def test__check_render_permission_user_perm_no_attribute_needs_perm(self):
        render_helper = RenderHelper(request=self.request, user_permissions=['some_perm', 'some_perm2'])
        has_perm = render_helper._check_render_permission(
            item=Badge(value='1234'))
        self.assertTrue(has_perm)

    def test_render_item_no_attribute_needs_perm(self):
        render_helper = RenderHelper(request=self.request, user_permissions=['some_perm', 'some_perm2'])
        rendered_item = render_helper.render_item(item=Badge(value='1234'))
        self.assertTrue(expr=rendered_item != '')

    def test_render_item_attribute_needs_perm(self):
        render_helper = RenderHelper(request=self.request, user_permissions=['some_perm', 'some_perm2'])
        rendered_item = render_helper.render_item(item=Badge(value='1234', needs_perm="some_perm"))
        self.assertTrue(expr=rendered_item != '')

    def test_render_item_attribute_needs_perm_wrong(self):
        render_helper = RenderHelper(request=self.request, user_permissions=['some_perm', 'some_perm2'])
        rendered_item = render_helper.render_item(item=Badge(value='1234', needs_perm="some_perm3"))
        self.assertTrue(expr=rendered_item == '')

    def test_render_items(self):
        render_helper = RenderHelper(request=self.request, user_permissions=['some_perm', 'some_perm2'])
        items = [Badge(value='', needs_perm='some_perm3'), Badge(value='', needs_perm='some_perm')]
        rendered_list = render_helper.render_list_coherent(items=items)
        expr = Badge(value='').render()
        self.assertEqual(first=rendered_list, second=expr)
