from setuptools import setup, find_packages

setup(
    name="magick",
    version='0.2',
    packages=find_packages(include=['src', \
                    'src.experiments', \
                    'src.primitives', \
                    'src.utils']),
    author="bt3gl",
    install_requires=['python-dotenv'],
    entry_points={
        'console_scripts': ['magick=src.main:run']
    },
)
