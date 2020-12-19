import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dp2rathena",
    version="0.0.1",
    license="MIT",
    author="Eric Liu",
    author_email="latiosworks@gmail.com",
    description="Convert Divine-Pride API data to rAthena YAML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Latiosu/dp2rathena",
    project_urls={
        "Changelog": ("https://github.com/Latiosu/dp2rathena/blob/master/CHANGELOG.md")
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)