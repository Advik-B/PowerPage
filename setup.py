from setuptools import setup, find_packages
from wattpad import VERSION
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

with codecs.open(os.path.join(here, "requirements.txt"), encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

DESCRIPTION = "A no-compromises wrapper for the Wattpad API"

# Setting up
setup(
    name="wattpad-api",
    version=VERSION,
    author="Advik",
    author_email="<advik.b@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=requirements,
    keywords=["Wattpad", "Wattpad Wrapper", "Watppad API", "API", "Wrapper"],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/Advik-B/wattpad-api",
    options={'bdist_wheel':{'universal':True}}
)