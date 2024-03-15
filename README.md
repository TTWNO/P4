# P4

Source code for our compiler to compile a natural like language to Python, with the aim of automating Excel tasks.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them

```
Python at least 3.10
poetry
```

### Installing


```
# assuming you have python installed, and it is in your path as python or python3. For these instructions, we will use python

# install poetry
curl -sSL https://install.python-poetry.org | python -

# clone the repository
git clone	git@github.com:MikailGuzel/P4.git

# change directory to the repository
cd P4

# install the dependencies
poetry install
```

## Running the compiler

To run the compiler, you can use the following command.

**Note:** You need to have completed the installation steps above.

```

poetry run python compiler.py <path to the file to compile>

```

### Updaing the compiler

To update the compiler, you can use the following command.

**Note:** You need to have completed the installation steps above.

```

git pull
poetry install

```

### Packaging the compiler

Packaging the compiler makes it possible to run the compiler without having to install the dependencies, poetry or python

```

poetry run pyinstaller compoer.spec

```

The compiled binary will be in the dist folder

