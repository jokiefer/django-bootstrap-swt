from django.contrib.auth.models import AbstractUser
from django.http import HttpRequest

from django_bootstrap_swt.components import BootstrapComponent
from django_bootstrap_swt.settings import CURRENT_VIEW_QUERYPARAM, CURRENT_VIEW_ARG_QUERYPARAM


class Bootstrap4Helper:

    def __init__(self, request: HttpRequest, requesting_user: AbstractUser, add_current_view_params: bool = False):
        self.permission_lookup = {}
        self.request = request
        self.requesting_user = requesting_user
        self.add_current_view_params = add_current_view_params

        self.url_querystring = ''
        if add_current_view_params:
            current_view = self.request.GET.get(CURRENT_VIEW_QUERYPARAM, self.request.resolver_match.view_name)
            if self.request.resolver_match.kwargs:
                # if kwargs are not empty, this is a detail view
                if 'pk' in self.request.resolver_match.kwargs:
                    current_view_arg = self.request.resolver_match.kwargs['pk']
                else:
                    current_view_arg = self.request.resolver_match.kwargs['slug']
                current_view_arg = self.request.GET.get(CURRENT_VIEW_ARG_QUERYPARAM, current_view_arg)
                self.url_querystring = \
                    f'?{CURRENT_VIEW_QUERYPARAM}={current_view}&{CURRENT_VIEW_ARG_QUERYPARAM}={current_view_arg}'
            else:
                self.url_querystring = f'?{CURRENT_VIEW_QUERYPARAM}={current_view}'

    def check_render_permission(self, permission: str) -> bool:
        has_perm = self.permission_lookup.get(permission, None)
        if has_perm is None:
            has_perm = self.requesting_user.has_perm(permission)
            self.permission_lookup[permission] = has_perm
        return has_perm

    def render_item(self, item: BootstrapComponent, ignore_current_view_params: bool = False) -> str:
        rendered_string = ''
        has_perm = self.check_render_permission(item.needs_perm) if hasattr(item, 'needs_perm') else True
        if has_perm:
            if self.add_current_view_params and hasattr(item, 'url') and not ignore_current_view_params:
                item.url += self.url_querystring
            rendered_string = item.render()
        return rendered_string

    def render_list_coherent(self, items: [BootstrapComponent], ignore_current_view_params: bool = False) -> str:
        rendered_string = ''
        for item in items:
            rendered_string += self.render_item(item=item, ignore_current_view_params=ignore_current_view_params)
        return rendered_string
