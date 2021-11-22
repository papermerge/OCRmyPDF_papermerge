from setuptools import setup, find_packages
#
# jinja2 == 3.0.3
# ocrmypdf == 12.0.3
# lxml == 4.6.2
#

setup(
    packages=find_packages(),
    install_requires=[
        "ocrmypdf == 12.7.2",
        "Jinja2 == 3.0.3",
        "lxml == 4.6.2"
    ],
    python_requires='>=3.7',
)
