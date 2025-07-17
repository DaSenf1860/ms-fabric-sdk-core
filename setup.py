from setuptools import setup, find_packages

setup(
    name='msfabricpysdkcore',
    version='2.8',
    packages=find_packages(),
    install_requires=[
        'requests>=2.30.0',
        'azure-identity>=1.15.0',
        'msal>=1.28.0'
    ]
)
