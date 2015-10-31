from setuptools import setup

setup(
    name='bcimob',
    version='0.1',
    py_modules=['bcimob'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        bcimob=bcimob.bcimob:cli
    ''',
)
