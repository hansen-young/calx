# calx: simple ML pipeline builder
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Description
**calx** (or chalk) is a Python package that aims to **accelerate ML training pipeline development** without writing lots of code. This repository contains two main parts:
- CLI Tools, used for running CLI commands such as creating new project or running the pipeline
- Builtins Components, provide common steps that are used for model training

**Main Features:**
- Create ML Pipeline mostly by working on YAML files.
- Builtins components to retrieve, preprocess, train, evaluate models.
- Runs are tracked by backend server like MLFlow or wandb. (revisit)
- Create custom pipeline step.
- Create step from docker image or CLI command.
- Covert calx pipeline.yaml to other package's format such as Kubeflow Pipeline. (planned)

## Installation
The package is only available in this repository and can be installed using pip.
```sh
pip install git+https://github.com/haiyee99/calx.git
```

## Quick Start
To start a new calx project, run the following command:
```sh
calx-init -n project-name
```

This will create a new directory `./project-name` which will be the default project structure:
```
project-name/
├── components/     # directory to create custom components
├── tests/          # directory to write unit test
├── .env            # file to store credentials / secrets
└── pipeline.yaml   # file to define the ML pipeline
```

To run a single step in the pipeline:
```sh
calx-run -f pipeline.yaml -s retrieve_data .
```

To run the whole pipeline:
```sh
calx-run -f pipeline.yaml --all .
```

## Documentation
TBA

## Background
Calx is developed by a bored programmer who likes to play online games after (and during) office hour, which he then decided to create this tool as a side project (for fun). He is definitely not inspired by the more well established tool like Kubeflow Pipeline :smirk:.

## Contributing
This project is currently not open for contribution and has no plan for it to be in the near future. However you are free to fork this repository and create your own version.

## Disclaimer
- Please only use this project for local development only as it is not tested for security vulnerability, any incident that may happen is beyond my responsibility.
- This project is written and tested using `Python 3.7.13` on `WSL2 Ubuntu`, other version may or may not work as expected.
