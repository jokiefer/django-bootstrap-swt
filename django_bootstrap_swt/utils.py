from django.http import HttpRequest
from django_bootstrap_swt.components import BootstrapComponent


class RenderHelper:

    def __init__(self, request: HttpRequest, user_permissions: [str] = None):
        self.request = request
        self.user_permissions = user_permissions if user_permissions else []

    def _check_render_permission(self, item: BootstrapComponent) -> bool:
        if not item.needs_perm or self.user_permissions and item.needs_perm in self.user_permissions:
            return True
        else:
            return False

    def render_item(self, item: BootstrapComponent) -> str:
        rendered_string = ''
        if self._check_render_permission(item):
            rendered_string = item.render()
        return rendered_string

    def render_list_coherent(self, items: [BootstrapComponent]) -> str:
        rendered_string = ''
        for item in items:
            rendered_string += self.render_item(item=item)
        return rendered_string
