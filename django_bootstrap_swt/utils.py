from django.http import HttpRequest
from django_bootstrap_swt.components import BootstrapComponent


class RenderHelper:
    """
    This class provides some functions for permission checked rendering.
    """
    def __init__(self, user_permissions: [str] = None):
        """
        :param user_permissions: a list which holds all user permission codenames
        """
        self.user_permissions = user_permissions if user_permissions else []

    def _check_render_permission(self, item: BootstrapComponent) -> bool:
        if not item.needs_perm or self.user_permissions and item.needs_perm in self.user_permissions:
            return True
        else:
            return False

    def render_item(self, item: BootstrapComponent) -> str:
        """
        Use this function to render one item based on the self.user_permissions list. The item.needs_perm attribute
        value will be checked against the self.user_permissions list. If the needs_perm attribute value is not
        in the self.user_permissions list, the item will not be rendered.

        :param item: the BoostrapComponent which will be rendered or not
        :return: empty string if the user does not have the right permission |
                 the rendered BootstrapComponent if the user does have the permission
        """
        rendered_string = ''
        if self._check_render_permission(item):
            rendered_string = item.render()
        return rendered_string

    def render_list_coherent(self, items: [BootstrapComponent]) -> str:
        """
        Use this function to render a list of items based on the self.user_permissions list. All items which needs
        permission will be checked against the self.user_permissions list. If the needs_perm attribute value is not
        in the self.user_permissions list, the item will not be rendered and concatenated.

        :param items: the list of BootstrapComponent which shall be rendered
        :return: empty string if the user does not have the right permissions for any item |
                 the concatenated string with all rendered items for that the user has permissions
        """
        rendered_string = ''
        for item in items:
            rendered_string += self.render_item(item=item)
        return rendered_string
