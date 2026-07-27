from setuptools import setup, find_packages

setup(
    name="mobt-gal-api",
    version="0.1.0",
    author="Alfonso Pérez Sánchez",
    author_email="alfonso.perezsanchez@hotmail.com",
    description="API wrapper for MOBT",
    packages=find_packages(),
    keywords=['bus', 'public transport', 'galicia', 'api', "mobt"],
    install_requires=[
        "requests",
    ]
)