"""
Build Ubuntu images independent of Launchpad's infrastructure
"""

from setuptools import find_packages, setup

dependencies = [
    'pyyaml',
]

setup(
    name='ubuntu_standalone_builder',
    version='0.1.0',
    author='Canonical Ltd.',
    author_email='daniel.watkins@canonical.com',
    description='Build Ubuntu images without Launchpad',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'cloud-test-framework = ubuntu_standalone_builder:main',
        ],
    },
)