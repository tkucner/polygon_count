import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="polygon_count",
    version="0.1.0",
    author="Tomasz Kucner",
    author_email="tomasz.kucner@oru.se",
    description="Implementation of paper Counting Convex k-gons in an Arrangments of Line Sgements by M. Fink, "
                "N. Kumar and S. Suri.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={'Source': 'https://github.com/tkucner/polygon_count',
                  'Author': 'https://mro.oru.se/people/tomasz-kucner/',
                  'Tracker': 'https://github.com/tkucner/polygon_count/issues',
                  },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires = ['matplotlib>=3.1.2',
                        'numpy>=1.18.0',
                        'networkx>=2.3',
                        ],
)