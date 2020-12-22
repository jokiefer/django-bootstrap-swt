********
Examples
********

This shows how you can use the django-bootstrap-swt app by some examples.

For our examples we use the following models::

    # tutorial/models.py
    class Order(models.Model):
        name = models.CharField(max_length=100, verbose_name="full name")

    class Product(models.Model):
        name = models.CharField(max_length=100, verbose_name="product name")
        order = models.ForeignKey(Order, related_name="items")


Use-Case: Provide action buttons for models.
###########################################
So what if you like to provide the action buttons for all you can do with this models?

For this use case you can write a function under the model classes which returns the action buttons::

    # tutorial/models.py
    class Order(models.Model):
        ...
        def get_action_buttons(self):
            actions[LinkButton(url=self.edit_view_uri,
                               content='<i class="fas fa-edit"></i>',
                               color=ButtonColorEnum.WARNING,
                               tooltip=_l(f"Edit <strong>{self.name} [{self.id}]</strong> Order."),
                               needs_perm=PermissionEnum.CAN_EDIT_ORDER.value)),
                    LinkButton(url=self.delete_view_uri,
                               content='<i class="fas fa-trash-alt"></i>',
                               color=ButtonColorEnum.DANGER,
                               tooltip=_l(f"Delete <strong>{self.name} [{self.id}]</strong> Order."),
                               needs_perm=PermissionEnum.CAN_DELETE_ORDER.value)),
                    ]

On any view you then can call the `order.get_action_buttons()` function to get all possible actions.

Use-Case: Only renders buttons for that the user has permissions.
#################################################################
The next thing is, how can i only display the actions the user has permissions for?

For this use case you can use the `RenderHelper` class::

    class OrderListView(ListView):
        model = Order
        ...
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)

            permissions = self.request.user.get_all_permissions()
            user_permissions = []
            for permission in permissions:
                user_permissions.append(permission.codename)

            render_helper = RenderHelper(user_permissions=user_permissions)

            for order in context['object_list']:
                order.actions = render_helper.render_list_coherent(items=order.get_action_buttons())

            return context

Now the rendered buttons are stored in your context and you can use them in your template like::

    {% for object in object_list %}
        {{object.actions|safe}}
    {% endfor %}

Use-Case: Update some attributes of the html component before rendering.
########################################################################

Sometimes you don't want to specify some attributes of a component at constructing time.

For this use case you can use again the `RenderHelper` class:

1. Update url query parameters.
If you want to add or update some query parameters of your Action buttons you can do it with the following::

    class OrderListView(ListView):
        model = Order
        ...
        def get_context_data(self, **kwargs):
            ...

            update_url_qs_dict = {'key-1': 'value-1', 'key-2': 'value-2'}

            render_helper = RenderHelper(user_permissions=user_permissions, update_url_qs=update_url_qs_dict)

            for order in context['object_list']:
                order.actions = render_helper.render_list_coherent(items=order.get_action_buttons())

            return context


All elements with an `href` attribute are updated like `http://example.com?key-1=value-1&key-2=value-2`.

2. Update the html attributes.
You can also update any html attribute with the `RenderHelper`. For example you want to change the button size on every view::

    class OrderListView(ListView):
        model = Order
        ...
        def get_context_data(self, **kwargs):
            ...

            update_attrs = {'class': ['btn-sm']}

            render_helper = RenderHelper(user_permissions=user_permissions, update_attrs=update_attrs)

            for order in context['object_list']:
                order.actions = render_helper.render_list_coherent(items=order.get_action_buttons())

            return context

