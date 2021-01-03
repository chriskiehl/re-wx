import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="re-wx",
    version="0.0.1",
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
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics :: Capture :: Screen Capture",
        "Topic :: Multimedia :: Graphics :: Capture"
    ],
    python_requires='>=3.6',
)