'''
Author : hupeng
Time : 2021/8/6 14:27 
Description: 
'''
import dandan

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fairy",
    version="0.0.1",
    author="BenjyHu",
    author_email="m15227041551@163.com",
    description="A small smart package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['flask', 'kazoo'],
    python_requires=">=3.6",
)
