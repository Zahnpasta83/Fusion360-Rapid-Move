This application is a GCode Rapid Move Converter designed to optimize CNC machining processes by automatically replacing linear feed moves (G1/G01) with rapid moves (G0/G00) when the tool height exceeds a specified threshold.

## How It Works:

User Interface (GUI)
The app provides an easy-to-use Tkinter-based GUI.

Users can select an input GCode file (.nc or .gcode).

Users can choose an output folder where the modified file will be saved.

A threshold height (in millimeters) can be set via an input field (default: 4 mm).

Clicking the "Convert" button processes the file.
Conversion Process

The app reads the input GCode file line by line.
It ignores comments and empty lines.

It extracts Z-values from movement commands.

If the tool height (Z-value) is above the specified threshold:
The linear feed move (G1/G01) is replaced with a rapid move (G0/G00).

The modified GCode is then saved as a new file (*_Rapid.nc).

<img width="650" alt="Bildschirmfoto 2025-03-09 um 10 58 47" src="https://github.com/user-attachments/assets/8f1e1a56-57c3-40e4-a47d-3bda0d45a157" />



## Additional Features
Customizable threshold: Users can change the height at which rapid moves are applied.
Error handling: The app prevents invalid inputs and displays error messages if necessary.

## Use Case
This application is useful for CNC programmers and machinists who want to optimize their toolpath movements. 
By replacing unnecessary feed moves with rapid moves above a certain height, machining time is reduced, and CNC machine efficiency is improved.

## ⚠️ Use at Your Own Risk!

This software is provided without any guarantees or liability. Use it at your own risk.

## 📌 Why this warning?

Incorrect G-code modifications could lead to unexpected behavior of your CNC machine.
A wrong threshold value or misinterpretation of movements may cause crashes or damage.
Always review the generated code before running it on your machine.
The developer assumes no responsibility for any damage, malfunction, or loss resulting from the use of this software.

## How to Run the App on a Mac
To run the GCode Rapid Move Converter on a Mac, follow these steps:

## 1. Install Python
The app is written in Python, so you need to have Python installed.

Check if Python is already installed by running:
```
python3 --version
```
If Python is not installed, download and install it from:
https://www.python.org/downloads/mac-osx/

Make sure pip (Python's package manager) is installed as well:
```
python3 -m ensurepip --default-pip
```

## 2. Install Required Dependencies
The app requires tkinter (for the GUI) and re (for text processing). tkinter is usually pre-installed with Python, but if it's missing, install it with:
```
brew install python-tk
```
Then, install any additional dependencies from requirements.txt (if provided):
```
pip3 install -r requirements.txt
```
## 3. Run the APP
Navigate to the folder where the script is located and execute the APP
