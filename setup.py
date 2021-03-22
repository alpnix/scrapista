from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.11'
DESCRIPTION = 'Scrape most popular websites easily'
LONG_DESCRIPTION = 'This is a Python package that helps with scraping some of the most popular websites such as Wikipedia, Amazon, etc.'

# Setting up
setup(
    name="scrapista",
    version=VERSION,
    author="Alp Niksarlı",
    author_email="<alp.niksarli@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests', 'beautifulsoup4'],
    keywords=['python', 'scrape', 'amazon', 'wikipedia', 'web', 'data mining', 'web scraping'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
