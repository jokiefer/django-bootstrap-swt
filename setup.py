import os

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-bootstrap-swt",
    version=os.getenv('RELEASE_VERSION'),
    author="Jonas Kiefer",
    author_email="jonas.kiefer@live.com",
    description="An app for creating bootstrap components on python level",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jokiefer/django-bootstrap-swt",
    include_package_data=True,
    packages=find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
