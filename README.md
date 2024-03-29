# SENG 474 Final Project
Originally created [here](https://github.com/maxUser/seng474_assignments) by [**@maxUser**](https://github.com/maxUser) and myself.  Was moved here as a part of a clean-up and to make development easier.

## Setup
To run the program create and enter a python3 (3.6+) virtual environment.
```
$ python3 -m venv venv
$ source venv/bin/activate
```

Install requirements (there aren't many).
```
(venv)$ pip3 install -r requirements.txt
(venv)$ pip3 install .
```

If you run into trouble you may need to update `pip` with:
```
(venv)$ pip3 install --upgrade pip
```
or:
```
(venv)$ curl https://bootstrap.pypa.io/get-pip.py | python3
```

You can then install and open up jupyter from here using:
```
(venv)$ pip3 install jupyter
(venv)$ jupyter notebook
```

## Run
TODO: some examples

## Components Breakdown
Descriptions of all stuff in this project.

### Data
Data collected is stored here.

##### `heroes.json`
Hero names and IDs.

##### `training_data.json`
DotA 2 match data used for training.

##### `testing_data.json`
DotA 2 match data used for testing.

### Modules
Base python code that interacts with API, cleans and processes data.

##### `collect.py`
Responsible for collecting DotA 2 match data from Steam API.

##### `process.py`
Responsible for processing the data collected.

### Notebooks
Any analysis of the dataset will be done using jupyter notebooks.

##### `analysis.ipynb`
The main analysis file where we run our code for final project output.

### Scripts
Contains python scripts that use the modules.

##### `get_data.py`
Uses `collect` module to get DotA 2 match data.
