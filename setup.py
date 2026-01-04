from setuptools import setup, find_packages

setup(
    name="soplos-welcome",
    version="2.0.2",
    packages=find_packages(),
    install_requires=[
        'PyGObject>=3.40.0',
        'python-xlib>=0.29',
        'psutil>=5.8.0'
    ],
    entry_points={
        'console_scripts': [
            'soplos-welcome=main:main',
        ],
    },
    author="Sergi Perich",
    author_email="info@soploslinux.com",
    description="The world's most advanced welcome application for Linux distributions",
    license="GPL-3.0",
)
