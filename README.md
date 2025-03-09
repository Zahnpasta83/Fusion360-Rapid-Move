This application is a GCode Rapid Move Converter designed to optimize CNC machining processes by automatically replacing linear feed moves (G1/G01) with rapid moves (G0/G00) when the tool height exceeds a specified threshold.

How It Works:

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

<img width="718" alt="Bildschirmfoto 2025-03-09 um 10 53 24" src="https://github.com/user-attachments/assets/f56c837b-a0a6-4f09-a8df-03d56b4e8996" />


Additional Features
Customizable threshold: Users can change the height at which rapid moves are applied.
Error handling: The app prevents invalid inputs and displays error messages if necessary.
Custom icon support: Users can replace the default app icon with their own .ico file.
Use Case
This application is useful for CNC programmers and machinists who want to optimize their toolpath movements. By replacing unnecessary feed moves with rapid moves above a certain height, machining time is reduced, and CNC machine efficiency is improved.
