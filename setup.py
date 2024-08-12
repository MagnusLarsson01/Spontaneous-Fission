from setuptools import setup, find_packages

setup(
    name="SpontaneousFission",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        # If any package contains data files, include them:
        'SpontaneousFission': ['data/*.csv'],
    },
    install_requires=[
        # Dependencies
    ],
    author="Magnus Larsson",
    author_email="magnus.larsson01@gmail.com",
    description="Package for calculations of spontaneous fission in compound materials",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MagnusLarsson01/Spontaneous-Fission",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
