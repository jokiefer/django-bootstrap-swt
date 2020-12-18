Ajax components
~~~~~~~~~~~~~~~

Sometimes you need to fetch some content asynchronous. For this use case this app provides the possibility to setup an `fetch_url` on the `Modal` and `Accordion` component::

    ...
    modal = Modal(title='nice modal',
                  body='',
                  btn_value='open modal',
                  btn_color=ButtonColorEnum.INFO,
                  fetch_url='http://example.com')
    ...

You also need to include our javascript bib to your html head::

    <head>
        ...
        <script type="text/javascript" src="{% static 'django_bootstrap_swt/js/django_bootstrap_swt.js' %}"></script>
        ...
    </head>

