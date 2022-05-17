from setuptools import setup, find_packages


setup(
    name="registry_client",
    version="0.1",
    packages=find_packages(),
    install_requires=["requests"],
    author="Jacob Livin Stanly",
    author_email="jacob.livin.stanly@iais.fraunhofer.de",
    description="A service registry client to be used by other ATLAS projects",
    long_description_content_type="text/markdown",
    url="https://github.com/atlasH2020/atlas_registry_client"
)