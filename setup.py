from setuptools import setup

setup(
    name = 'Mmm Paste',
    version = '1.0',
    long_description = __doc__,
    packages = ['mmmpaste'],
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'Flask==0.9',
        'SQLAlchemy==0.7.9',
        'WTForms==1.0.2',
    ],
)