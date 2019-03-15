from setuptools import setup, find_namespace_packages

setup(
    name="weatherapp.core",
    version="0.1.0",
    author="Viacheslav Liash",
    author_email="author@example.com",
    description="A simple cli weather aggregator",
    long_descriptoin="",
    url = "https://github.com/midasinc/weatherapp.core",
    packages=find_namespace_packages(),
    entry_points={
        'console_scripts': 'wfapp=weatherapp.core.app:main'
    },
    install_requires=[
        'requests',
        'bs4',
        'lxml',
        'prettytable',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
