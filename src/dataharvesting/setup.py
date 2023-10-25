from setuptools import setup

setup(
    name='data_harvester',
    version='0.0.1',
    entry_points={
    # TO BE TESTED.
        'console_scripts': [
            'my_command=data_harvester:main',
        ],
    },
)
