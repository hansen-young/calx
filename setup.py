import setuptools
import os

from importlib.machinery import SourceFileLoader

version = SourceFileLoader("calx.version", "calx/version.py").load_module().VERSION
setuptools.setup(
    name="calx",
    version=version,
    author="HYHY",
    author_email="hansenyoung0707@gmail.com",
    description="Python package for rapid ML training pipeline development",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/haiyee99/calx",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    entry_points={
        "console_scripts": [
            "calx-init=calx.scripts.calx_init:main",
            "calx-run=calx.scripts.calx_run:main",
        ],
    },
    install_requires=[
        "PyYAML==5.4.1",
        "omegaconf==2.1.2",
    ],
    include_package_data=True,
    python_requires=">=3.7",
)
