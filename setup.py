from setuptools import find_packages, setup

setup(
    name="logninja",
    version="0.1.1",
    author="Pedro Cantidio",
    author_email="ppcantidio@gmail.com",
    description="A log configuration library for Python projects.",
    long_description="LogNinja is a library that provides a set of tools to configure logging in Python projects. It is designed to be used with the standard logging module and provides a set of classes and functions to help you configure your loggers, formatters, and filters. LogMancer is designed to be easy to use and flexible, allowing you to configure your loggers in a way that best suits your project.",
    long_description_content_type="text/plain",
    url="https://github.com/ppcantidio/logmancer.py",
    packages=find_packages(exclude=["tests"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
