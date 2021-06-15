import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="selenium_firefox",
    version="2.0.7",
    author="Kovács Kristóf-Attila",
    description="selenium_firefox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kkristof200/selenium_firefox",
    packages=setuptools.find_packages(),
    install_requires=[
        'geckodriver-autoinstaller>=0.1.0',
        'kproxy>=0.0.1',
        'noraise>=0.0.16',
        'selenium>=3.141.0',
        'selenium-browser>=0.0.12'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True
)