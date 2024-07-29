from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='LDC',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'countingmodule': ['working.weights.h5'],
    },
    install_requires=parse_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'count=countingmodule.main:main',
        ],
    },
)