# django-bootstrap-swt  - An app for creating bootstrap components on python level
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=jokiefer_django-bootstrap-swt&metric=alert_status)](https://sonarcloud.io/dashboard?id=jokiefer_django-bootstrap-swt)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=jokiefer_django-bootstrap-swt&metric=coverage)](https://sonarcloud.io/dashboard?id=jokiefer_django-bootstrap-swt)
[![Documentation Status](https://readthedocs.org/projects/django-bootstrap-swt/badge/?version=latest)](https://django-bootstrap-swt.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/django-bootstrap-swt.svg)](https://badge.fury.io/py/django-bootstrap-swt)

django-bootstrap-swt simplifies the task of building HTML pages with bootstrap components by using the java swt concept. This reduces your html code duplication, cause you can use predefined bootstrap components.

- Available on pypi as [django-bootstrap-swt](https://pypi.python.org/pypi/django-bootstrap-swt)
- [Documentation on readthedocs.org](https://django-bootstrap-swt.readthedocs.io/en/latest/)
- [Bug tracker](http://github.com/jokiefer/django-bootstrap-swt/issues)


Features:

- Create any bootstrap component on backend level.
- Creates uniq id's for bootstrap components like [accordion](https://getbootstrap.com/docs/4.0/components/collapse/#accordion-example) and [modal](https://getbootstrap.com/docs/4.0/components/modal/#live-demo) to avoid id conflicts in javascript.
- supports async data fetching for modal and accordion components.

## Example

Start by adding `django_bootstrap_swt` to your `INSTALLED_APPS` setting like this:

```python
INSTALLED_APPS = (
    ...,
    "django_bootstrap_swt",
)
```

Creating a bootstrap component is as simple as:

```python

item_list = [ListGroupItem(left='text-at-the-left', center='text-at-the-center', right='text-at-the-right')

list_group = ListGroup(items=item_list)

my_modal = Modal(title=f'Details of {self.object.title}',
                 modal_body=list_group,
                 btn_value='Open modal',
                 btn_color=ButtonColorEnum.SECONDARY,
                 btn_tooltip='Click this button to open modal',
                 size=ModalSizeEnum.LARGE,)
```
All django-bootstrap-swt components returns the rendered template as `string`. So you can simply concatenate the components:
```python

accordion_title = python_object.str_attribute + Badge(value='123')

```
If you need a `SafeString` instead of `string` you can call the `render()` function manually:
```python

safe_string = Badge(value='123').render(safe=True)

```


Check out the [documentation](https://django-bootstrap-swt.readthedocs.io/en/latest/) for more details.
