from setuptools import setup, find_packages

setup(
    packages=find_packages(),
    install_requires=[
        "ocrmypdf == 12.0.3",
    ],
    python_requires='>=3.7',
)
