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
        "dirhash==0.2.1",
        "docker==5.0.3",
        "matplotlib==3.5.3",
        "mysqlclient==2.1.1",
        "networkx==2.6.2",
        "omegaconf==2.1.2",
        "pandas==1.3.5",
        "psycopg2==2.9.3",
        "pybigquery==0.10.2",
        "python-dotenv==0.20.0",
        "PyYAML==5.4.1",
        "requests==2.28.1",
        "SQLAlchemy==1.4.40",
    ],
    include_package_data=True,
    python_requires=">=3.7",
)
