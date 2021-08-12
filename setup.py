from setuptools import setup, find_packages

name = "ecosysteme"

version = "1.0.0"

description = "A game of life inspired simulation where dears and wolves are wandering in grassland eating each other."


requirements = []

setup(
    name=name,
    version=version,
    author="Thibault Charmet",
    author_email="",
    description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/Chthi/ecosysteme",
    project_urls={},
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    py_modules=[],
    entry_points={
        "console_scripts": [
            # package=module.file:function
            "ecosysteme=ecosysteme.__main__:main",
        ]
    },
    python_requires='>=3.6',
    install_requires=requirements,
    include_package_data=True,
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    keywords='simulation life',
)
