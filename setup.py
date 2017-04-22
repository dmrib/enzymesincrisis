"""Setup script."""


from setuptools import setup, find_packages

setup(
    name='enzymes-on-crisis',
    version='0.1.0',
    description='Data visualization on enzyme nomenclature changes over time.',
    url='https://github.com/dmrib/enzymes-on-crisis',
    author='Danilo Miranda Ribeiro',
    author_email='dmrib.cs@gmail.com',
    license='MIT',
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3.6',
                 'Intended Audience :: Science/Research'],
    keywords='datavis enzymes',
    packages=find_packages(),
    install_requires=['Flask', 'glob2', 'BeautifulSoup4']
)
