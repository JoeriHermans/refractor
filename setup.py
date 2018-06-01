from setuptools import Command, find_packages, setup

setup(
    name = 'fluodonut',
    description = 'Gravitational lensing simulator.',
    url = 'https://github.com/montefiore-ai/fluodonut',
    author = 'Joeri R. Hermans',
    author_email = 'joeri.hermans@doct.uliege.be',
    classifiers = [
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Programming Language :: Python :: 3'
    ],
    packages = find_packages(exclude=['docs']),
    install_requires = ['numpy', 'PIL']
)
