#!/usr/bin/env python
from setuptools import find_namespace_packages, setup

package_name = "dbt-gpt"
# make sure this always matches dbt/adapters/{adapter}/__version__.py
package_version = "1.5.0b5"
description = """The Gpt adapter plugin for dbt"""

setup(
    name=package_name,
    version=package_version,
    description=description,
    long_description=description,
    author="Tyler Rouze",
    author_email="tyler@tylerrouze.com",
    url="https://github.com/trouze/dbt-gpt",
    packages=find_namespace_packages(include=["dbt", "dbt.*"]),
    include_package_data=True,
    install_requires=[
        "dbt-core==1.5.0b5",
        "openai"
    ],
)
