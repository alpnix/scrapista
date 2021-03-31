from setuptools import setup, find_packages

def get_readme():
    with open("README.md", encoding="utf-8") as fh:
        long_description = "\n" + fh.read()

    return long_description

VERSION = "1.0.8"
REQUIREMENTS = [
    'requests', 
    'beautifulsoup4'
]
DESCRIPTION = 'Scrape most popular websites easily'


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
    long_description=get_readme(),
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    keywords=['python', 'scrape', 'amazon', 'wikipedia', 'web', 'data mining', 'web scraping'],
    include_package_data=True,
)
