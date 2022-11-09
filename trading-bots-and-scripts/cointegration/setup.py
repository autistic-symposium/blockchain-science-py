from setuptools import setup, find_packages

setup(
    name="cointbot",
    version='0.1',
    packages=find_packages(include=['src', 'src/bot']),
    author="steinkirch",
    install_requires=['python-dotenv'],
    entry_points={
        'console_scripts': ['cointbot=src.main:run']
    },
)