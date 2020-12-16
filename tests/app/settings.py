INSTALLED_APPS = [
    "django_bootstrap_swt",
    "tests.app",
    "django_nose",
]

SECRET_KEY = "this is super secret"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    }
]

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-xunit',
    '--xunit-file=tests/nosetests.xml',
    '--with-coverage',
    '--cover-erase',
    '--cover-xml',
    '--cover-xml-file=tests/nosecover.xml',
]
