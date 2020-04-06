import setuptools

with open("../README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chariot",
    version="0.1",
    author="chariot dev team",
    description="An IoT data collection system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    setup_requires=['wheel'],
    python_requires='>=3.7'
)
