import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="re-wx",
    version="0.00.2",
    author="Chris Kiehl",
    author_email="me@chriskiehl.com",
    description="A library for building modern declarative desktop applications in WX",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chriskiehl/re-wx",
    include_package_data=True,
    data_files=[('rewx', ['rewx/icon.png'])],
    install_requires=['wxpython>=4.1.0'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Software Development :: User Interfaces"
    ],
    python_requires='>=3.6',
)