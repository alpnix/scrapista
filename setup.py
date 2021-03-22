from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))
__version__ = find_version('scrapista/__init__.py')

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = __version__
REQUIREMENTS = [
    'requests', 
    'bs4'
]
DESCRIPTION = 'Scrape most popular websites easily'
LONG_DESCRIPTION = 'This is a Python package that helps with scraping some of the most popular websites such as Wikipedia, Amazon, etc.'

# Setting up
setup(
    name="scrapista",
    version=VERSION,
    license='MIT',
    author="Alp Niksarlı",
    author_email="alp.niksarli@gmail.com",
    url='https://github.com/alpnix/scrapista',
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        'License :: MIT License',
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Web Scraping :: Data Mining",
    ],
    keywords=['python', 'scrape', 'amazon', 'wikipedia', 'web', 'data mining', 'web scraping']
)
