'''
Author : hupeng
Time : 2021/8/6 14:27 
Description: 
'''
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fairy_tail",
    version="0.0.1",
    author="BenjyHu",
    license="MIT",
    author_email="m15227041551@163.com",
    description="A small smart package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BenjyHu/fairy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['flask', 'kazoo'],
    python_requires=">=3.6",
)
