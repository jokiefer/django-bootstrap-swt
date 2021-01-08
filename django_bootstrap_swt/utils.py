from urllib import parse
from django_bootstrap_swt.components import BootstrapComponent, Modal


class RenderHelper:
    """
    This class provides some functions for permission checked rendering.
    """
    def __init__(self, user_permissions: [str] = None, update_url_qs: dict = None, update_attrs: dict = None):
        """
        :param user_permissions: a list which holds all user permission codenames
        :param update_url_qs: a dict which contains the key:value pairs to update the query of url items
        :param update_attrs: Optional: the dict with the update key value pairs. Value shall be a list
        """
        self.user_permissions = user_permissions if user_permissions else []
        self.update_url_qs = update_url_qs
        self.update_attrs = update_attrs

    def _check_render_permission(self, item: BootstrapComponent) -> bool:
        if not item.needs_perm or self.user_permissions and item.needs_perm in self.user_permissions:
            return True
        else:
            return False

    def update_queryparams(self, item: BootstrapComponent):
        """
        Updates the query string of a given url
        :param item: the BootstrapComponent to update
        :return: the updated item
        """
        if hasattr(item, 'attrs') and 'href' in item.attrs:
            url_parts = list(parse.urlparse(item.attrs['href'][0]))
            query = dict(parse.parse_qsl(url_parts[4]))
            query.update(self.update_url_qs)
            url_parts[4] = parse.urlencode(query)
            item.attrs['href'] = [parse.urlunparse(url_parts)]
        return item

    def render_item(self, item, safe: bool = False) -> str:
        """
        Use this function to render one item based on the self.user_permissions list. The item.needs_perm attribute
        value will be checked against the self.user_permissions list. If the needs_perm attribute value is not
        in the self.user_permissions list, the item will not be rendered.

        :param item: the BoostrapComponent which will be rendered or not
        :param safe: switches if the rendered component is returned as SafeString or str
        :return: empty string if the user does not have the right permission |
                 the rendered BootstrapComponent if the user does have the permission
        """
        rendered_string = ''
        if self._check_render_permission(item):
            if self.update_url_qs:
                self.update_queryparams(item=item)
            if self.update_attrs:
                if isinstance(item, Modal):
                    item.button.update_attributes(update_attrs=self.update_attrs)
                else:
                    item.update_attributes(update_attrs=self.update_attrs)
            rendered_string = item.render(safe=safe)
        return rendered_string

    def render_list_coherent(self, items: [], safe: bool = False) -> str:
        """
        Use this function to render a list of items based on the self.user_permissions list. All items which needs
        permission will be checked against the self.user_permissions list. If the needs_perm attribute value is not
        in the self.user_permissions list, the item will not be rendered and concatenated.

        :param items: the list of BootstrapComponent which shall be rendered
        :param safe: Optional: switches if the rendered component is returned as SafeString or str
        :return: empty string if the user does not have the right permissions for any item |
                 the concatenated string with all rendered items for that the user has permissions
        """
        rendered_string = ''
        for item in items:
            rendered_string += self.render_item(item=item, safe=safe)
        return rendered_string
