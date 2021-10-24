from setuptools import setup, find_packages

setup(
    name="bmservice",
    version="0.0.1",
    description="Bookmarker service.",
    packages=find_packages(exclude=["tests"]),
    install_requires=["requests"],
    url="https://github.com/avilay/bookmarker-all/backend/bookmarker-service",
    author="Avilay Parekh",
    author_email="avilay@gmail.com",
)
