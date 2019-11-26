from setuptools import setup, find_packages

setup(
    name = 'SENG474 Final Project',
    version = '0.1.0',
    packages = find_packages(),
    package_data = {'data': ['heroes.json', 'raw_data.json']}
)
