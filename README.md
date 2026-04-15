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

<details>
<summary><b>Linux:</b></summary>

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

</details>

<details>
<summary><b>Windows:</b></summary>

Download and install **Git** from the official website: [link](https://git-scm.com/install/windows)

Download and install **Python3.13** from the official website: [link](https://www.python.org/downloads/windows/)

- IMPORTANT: In the Python installer, make sure to check the "Add Python to PATH" box before proceeding.

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

</details>

## Rerunning the Application

To run the program again, you must ensure that the virtual environment is active. Follow these steps:

### 1. Activate the Virtual Environment

If your virtual environment is not already active, use the command appropriate for your operating system:

`.\venv\Scripts\activate` - Windows

`source venv/bin/activate` - Linux

### 2. Launch the Program

Once the virtual environment is activated (you should see `(venv)` in your terminal prompt), run the script using:

`python uma.py` - Windows

`python3 uma.py` - Linux

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

* 0.3.9
    * Added Uma Score display in the 'View Results' window within the Uma list
    * Updated README.md
    * Optimized the chart
    * Refined TAB navigation in the 'Add Results' window for a better user experience

### Issues

There is a known issue between the Matplotlib library and Python 3.14. Please use Python 3.13 instead.

## License

This project is licensed under the GNU GPL v3.0 License - see the LICENSE file for details
