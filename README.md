# uma-tt-db
Tool for tracking and analyzing Team Trial results in the game UmaMusume: Pretty Derby

## Description

Track your Umas' Team Trials progress in UmaMusume: Pretty Derby (ウマ娘 プリティーダービー) and analyze the results with detailed charts.

## Getting Started

Program works on:
* Linux
* Windows 10 and 11

## Installing

This program is provided as source code. Installation steps vary depending on your operating system:
**Linux**:
Open a terminal in your desired destination folder and clone the repository:
`git clone https://github.com/jamrozmat/uma-tt-db`
`cd uma-tt-db`
Create and activate the virtual environment:
`python3 -m venv venv`
`source venv/bin/activate`
Install the required dependencies:
`python3 -m pip install -r requirements.txt `
Start the program:
`python3 uma.py`

**Windows**:
Download and install **Git** from the official website: [link](https://git-scm.com/install/windows)  
Download and install **Python3.13** from the official website: [link](https://www.python.org/downloads/windows/)
Open CMD, navigate to your destination folder, and clone the repository:
`cd your_destination_folder`
`git clone https://github.com/jamrozmat/uma-tt-db`
`cd uma-tt-db`
Create and activate a virtual environment:
`python -m venv venv`
`.\venv\Scripts\activate`
Install the required dependencies:
`python -m pip install -r requirements.txt `
Start the program:
`python uma.py`

## Updating the program

You can update the program to the latest version from the main branch by running the following command in your terminal:
Linux:
`python3 uma.py -U`
Windows:
`python uma.py -U`

To display the help message and all available options:
Linux:
`python3 uma.py -h`
Windows:
`python uma.py -h`

### Tips

For quicker access, you can set up an alias.
Just make sure your virtual environment is activated before running it!


## Version History

* 0.3.2
    * public release
    * Add README.md

### Issues

There is a known issue between the Matplotlib library and Python 3.14. Please use Python 3.13 instead.

## License

This project is licensed under the GNU GPL v3.0 License - see the LICENSE file for details
