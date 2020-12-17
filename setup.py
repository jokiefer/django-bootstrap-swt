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
    packages=find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
