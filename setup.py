from setuptools import setup

import mmmpaste

setup(
    name = 'mmmpaste',
    version = '1.0dev',
    long_description = __doc__,
    packages = ['mmmpaste'],
    include_package_data = True,
    zip_safe = False,
    license = mmmpaste.__license__,
    install_requires = [
        'Flask==0.9',
        'SQLAlchemy==0.7.9',
        'WTForms==1.0.2',
    ],
    entry_points = {
        'console_scripts': [
            'mmmpaste-client = mmmpaste.client:main',
        ],
    },
)
