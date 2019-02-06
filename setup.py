import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jpyextra",
    version="0.0.1",
    author="Patrice Ferlet",
    author_email="metal3d@gmail.com",
    description="Some extra tools to work with Jupyter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/metal3d/jupyter-extra",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
