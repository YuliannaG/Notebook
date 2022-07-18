from setuptools import setup, find_namespace_packages

setup(
    name='smart_bot',
    version='0.1.0',
    description='bot with function adressbook, notes and sorter',
    author='AndrewAndrunin, YuliannaG, vitaliy-2607',
    author_email='andry.andrynin@gmail.com',
    license='MIT',
    classifiers=[
            "Programming Language :: Python :: 3.10",
            "License :: OSI Approved :: MIT License",
            "Operating System :: Windows",
    ],
    packages=find_namespace_packages(),
    entry_points={'console_scripts': [
        'smartbot=goit_project1.main:main']}
)