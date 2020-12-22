from unittest import TestCase
from django_bootstrap_swt.components import Link, Badge
from django_bootstrap_swt.utils import RenderHelper


class TestRenderHelper(TestCase):
    """ This class contains all needed tests for testing TestRenderHelper class
    """

    def test_init_with_user_permissions_arg(self):
        user_perms = ['test_perm_1', 'test_perm_2']
        render_helper = RenderHelper(user_permissions=['test_perm_1', 'test_perm_2'])

        self.assertEqual(first=user_perms, second=render_helper.user_permissions)

    def test_init_with_update_url_qs_arg(self):
        update_url_qs = {'key': 'content', 'key2': 'content2'}
        render_helper = RenderHelper(update_url_qs=update_url_qs)

        self.assertEqual(first=update_url_qs, second=render_helper.update_url_qs)

    def test_init_without_args(self):
        render_helper = RenderHelper()

        self.assertEqual(first=[], second=render_helper.user_permissions)
        self.assertEqual(first=None, second=render_helper.update_url_qs)

    def test__check_render_permission_user_perm_empty_not_needs_perm(self):
        render_helper = RenderHelper()
        has_perm = render_helper._check_render_permission(
            item=Link(url='http://example.com', content='http://example.com'))
        self.assertTrue(has_perm)

    def test__check_render_permission_user_perm_empty_needs_perm(self):
        render_helper = RenderHelper()
        item = Link(url='http://example.com', content='http://example.com', needs_perm='some_perm')
        has_perm = render_helper._check_render_permission(item=item)

        self.assertFalse(has_perm)

    def test__check_render_permission_user_perm_needs_perm(self):
        render_helper = RenderHelper(user_permissions=['some_perm', 'some_perm2'])
        has_perm = render_helper._check_render_permission(
            item=Link(url='http://example.com', content='http://example.com'))
        self.assertTrue(has_perm)

    def test__check_render_permission_user_perm_no_attribute_needs_perm(self):
        render_helper = RenderHelper(user_permissions=['some_perm', 'some_perm2'])
        has_perm = render_helper._check_render_permission(
            item=Badge(content='1234'))
        self.assertTrue(has_perm)

    def test_render_item_no_attribute_needs_perm(self):
        render_helper = RenderHelper(user_permissions=['some_perm', 'some_perm2'])
        rendered_item = render_helper.render_item(item=Badge(content='1234'))
        self.assertTrue(expr=rendered_item != '')

    def test_render_item_attribute_needs_perm(self):
        render_helper = RenderHelper(user_permissions=['some_perm', 'some_perm2'])
        rendered_item = render_helper.render_item(item=Badge(content='1234', needs_perm="some_perm"))
        self.assertTrue(expr=rendered_item != '')

    def test_render_item_attribute_needs_perm_wrong(self):
        render_helper = RenderHelper(user_permissions=['some_perm', 'some_perm2'])
        rendered_item = render_helper.render_item(item=Badge(content='1234', needs_perm="some_perm3"))
        self.assertTrue(expr=rendered_item == '')

    def test_render_items(self):
        render_helper = RenderHelper(user_permissions=['some_perm', 'some_perm2'])
        items = [Badge(content='', needs_perm='some_perm3'), Badge(content='', needs_perm='some_perm')]
        rendered_list = render_helper.render_list_coherent(items=items)
        expr = Badge(content='').render()
        self.assertEqual(first=rendered_list, second=expr)

    def test_render_item_with_update_url_qs_url_has_key(self):
        url_before_update = 'http://example.com?key=xxx'
        url_after_update = 'http://example.com?key=content'
        test_link_rendered = Link(content='1234', url=url_after_update).render()

        render_helper = RenderHelper(update_url_qs={'key': 'content'})
        rendered_item = render_helper.render_item(item=Link(content='1234', url=url_before_update))

        self.assertEqual(first=rendered_item, second=test_link_rendered)

    def test_render_item_with_update_url_qs_url_has_no_key(self):
        url_before_update = 'http://example.com'
        url_after_update = 'http://example.com?key=content'
        test_link_rendered = Link(content='1234', url=url_after_update).render()

        render_helper = RenderHelper(update_url_qs={'key': 'content'})
        rendered_item = render_helper.render_item(item=Link(content='1234', url=url_before_update))

        self.assertEqual(first=rendered_item, second=test_link_rendered)

    def test_render_item_with_update_url_qs_url_has_other_keys(self):
        url_before_update = 'http://example.com?key2=content123'
        url_after_update = 'http://example.com?key2=content123&key=content'
        test_link_rendered = Link(content='1234', url=url_after_update).render()

        render_helper = RenderHelper(update_url_qs={'key': 'content'})
        rendered_item = render_helper.render_item(item=Link(content='1234', url=url_before_update))

        self.assertEqual(first=rendered_item, second=test_link_rendered)

    def test_render_item_with_update_attrs(self):
        test_link_rendered = Link(content='1234', url="http://example.com")
        test_link_rendered.update_attribute('key', ['value-1', 'value-2'])
        render_helper = RenderHelper(update_attrs={'key': ['value-1', 'value-2']})
        rendered_item = render_helper.render_item(item=Link(content="1234", url="http://example.com"))

        self.assertMultiLineEqual(first=rendered_item, second=test_link_rendered.render())
