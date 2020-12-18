Examples
~~~~~~~~

This shows how you can use the django-bootstrap-swt app by some examples.

For our examples we use the following models::

    # tutorial/models.py
    class Order(models.Model):
        name = models.CharField(max_length=100, verbose_name="full name")

    class Product(models.Model):
        name = models.CharField(max_length=100, verbose_name="product name")
        order = models.ForeignKey(Order, related_name="items")

So what if you like to provide the action buttons for all you can do with this models?

For this use case you can write a function under the model classes which returns the action buttons::

    # tutorial/models.py
    class Order(models.Model):
        ...
        def get_action_buttons(self):
            actions[LinkButton(url=self.edit_view_uri,
                               value='<i class="fas fa-edit"></i>',
                               color=ButtonColorEnum.WARNING,
                               tooltip=_l(f"Edit <strong>{self.name} [{self.id}]</strong> Order."),
                               needs_perm=PermissionEnum.CAN_EDIT_ORDER.value)),
                    LinkButton(url=self.delete_view_uri,
                               value='<i class="fas fa-trash-alt"></i>',
                               color=ButtonColorEnum.DANGER,
                               tooltip=_l(f"Delete <strong>{self.name} [{self.id}]</strong> Order."),
                               needs_perm=PermissionEnum.CAN_DELETE_ORDER.value)),
                    ]

On any view you then can call the `order.get_action_buttons()` function to get all possible actions.
The next thing is, how can i only display the actions the user has permissions for?

For this use case you can use the `RenderHelper` class::

    class OrderListView(ListView):
        model = Order
        ...
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)

            render_helper = RenderHelper(request=self.request, )

            for order in context['object_list']:
                order.actions =

            return context