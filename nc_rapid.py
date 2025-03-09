import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re

# Sprach-Strings
LANGUAGES = {
    "de": {
        "title": "GCode Rapid Move Konverter",
        "input_label": "Eingabedatei:",
        "output_label": "Zielordner:",
        "threshold_label": "Schwellwert (mm):",
        "convert_button": "Konvertieren",
        "select_file": "Eingabedatei auswählen",
        "select_folder": "Zielordner auswählen",
        "success": "Datei erfolgreich konvertiert:\n{}",
        "error_no_file": "Bitte wählen Sie eine Eingabedatei aus!",
        "error_no_folder": "Bitte wählen Sie einen Zielordner aus!",
        "error_extension": "Die ausgewählte Datei hat keine gültige Endung (.nc oder .gcode)!",
        "error_generic": "Fehler: {}",
        "use_at_own_risk": "⚠️ Nutzung auf eigenes Risiko! Änderungen am G-Code können zu unerwartetem Maschinenverhalten führen."
    },
    "en": {
        "title": "GCode Rapid Move Converter",
        "input_label": "Input File:",
        "output_label": "Target Folder:",
        "threshold_label": "Threshold (mm):",
        "convert_button": "Convert",
        "select_file": "Select Input File",
        "select_folder": "Select Target Folder",
        "success": "File successfully converted:\n{}",
        "error_no_file": "Please select an input file!",
        "error_no_folder": "Please select a target folder!",
        "error_extension": "The selected file does not have a valid extension (.nc or .gcode)!",
        "error_generic": "Error: {}",
        "use_at_own_risk": "⚠️ Use at your own risk! G-code modifications can lead to unexpected machine behavior."
    }
}

# Standardwerte
language = "de"
threshold_value = 4  # Standard-Schwellwert

def update_texts():
    """Aktualisiert alle Texte basierend auf der gewählten Sprache."""
    lang = LANGUAGES[language]
    root.title(lang["title"])
    input_label.config(text=lang["input_label"])
    output_label.config(text=lang["output_label"])
    threshold_label.config(text=lang["threshold_label"])
    convert_button.config(text=lang["convert_button"])
    lang_label.config(text="Sprache:" if language == "de" else "Language:")

def change_language(selected_lang):
    """Wechselt die Sprache und aktualisiert die GUI."""
    global language
    language = selected_lang
    update_texts()

def select_input_file():
    file_path = filedialog.askopenfilename(
        title=LANGUAGES[language]["select_file"],
        filetypes=[("GCode Files", "*.nc *.gcode"), ("All Files", "*.*")]
    )
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)

def select_output_folder():
    folder_path = filedialog.askdirectory(title=LANGUAGES[language]["select_folder"])
    if folder_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, folder_path)

def convert_file():
    global threshold_value
    try:
        threshold_value = float(threshold_entry.get())  # Neuen Schwellwert übernehmen
    except ValueError:
        messagebox.showerror("Fehler", "Ungültiger Schwellwert!") if language == "de" else messagebox.showerror("Error", "Invalid threshold value!")
        return

    input_file = input_entry.get()
    output_folder = output_entry.get()
    
    if not input_file:
        messagebox.showerror("Fehler", LANGUAGES[language]["error_no_file"])
        return
    if not output_folder:
        messagebox.showerror("Fehler", LANGUAGES[language]["error_no_folder"])
        return
    
    if not input_file.lower().endswith(('.nc', '.gcode')):
        messagebox.showerror("Fehler", LANGUAGES[language]["error_extension"])
        return
    
    Above_Height_Threshold_prev = 1
    Current_Height = 0

    base_name = os.path.splitext(os.path.basename(input_file))[0]
    new_file_name = f"{base_name}_Rapid.nc"
    new_file_path = os.path.join(output_folder, new_file_name)
    
    try:
        with open(input_file, "r", encoding="utf-8", errors="ignore") as f_input, \
             open(new_file_path, "w", encoding="utf-8") as f_output:
            
            for line in f_input:
                if ";" in line or line.strip() == "" or "(" in line or ")" in line:
                    continue

                if re.search(r'[Zz]', line):
                    tokens = line.split()
                    for token in tokens:
                        if token.upper().startswith("Z"):
                            try:
                                Current_Height = float(token[1:])
                            except ValueError:
                                Current_Height = 0
                            break
                    if Current_Height > threshold_value:
                        Above_Height_Threshold = 1
                    else:
                        Above_Height_Threshold = 0
                else:
                    Above_Height_Threshold = Above_Height_Threshold_prev
                
                tokens = line.split()
                new_tokens = []
                found_G = False
                for token in tokens:
                    if token.upper().startswith("G"):
                        if token.upper() in ["G1", "G01"]:
                            if Above_Height_Threshold and Above_Height_Threshold_prev:
                                new_tokens.append("G00")
                            else:
                                new_tokens.append(token)
                            found_G = True
                        else:
                            new_tokens.append(token)
                    else:
                        new_tokens.append(token)
                if not found_G and Above_Height_Threshold and Above_Height_Threshold_prev:
                    new_tokens.insert(0, "G00")
                
                new_line = " ".join(new_tokens)
                f_output.write(new_line + "\n")
                Above_Height_Threshold_prev = Above_Height_Threshold
        
        messagebox.showinfo("Erfolg", LANGUAGES[language]["success"].format(new_file_path))
    except Exception as e:
        messagebox.showerror("Fehler", LANGUAGES[language]["error_generic"].format(str(e)))

# Tkinter GUI aufbauen
root = tk.Tk()
root.title(LANGUAGES[language]["title"])

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# Eingabedatei
input_label = tk.Label(frame, text=LANGUAGES[language]["input_label"])
input_label.grid(row=0, column=0, sticky="w")
input_entry = tk.Entry(frame, width=50)
input_entry.grid(row=0, column=1, padx=5)
input_button = tk.Button(frame, text="...", command=select_input_file)
input_button.grid(row=0, column=2, padx=5)

# Zielordner
output_label = tk.Label(frame, text=LANGUAGES[language]["output_label"])
output_label.grid(row=1, column=0, sticky="w")
output_entry = tk.Entry(frame, width=50)
output_entry.grid(row=1, column=1, padx=5)
output_button = tk.Button(frame, text="...", command=select_output_folder)
output_button.grid(row=1, column=2, padx=5)

# Schwellwert-Eingabe
threshold_label = tk.Label(frame, text=LANGUAGES[language]["threshold_label"])
threshold_label.grid(row=2, column=0, sticky="w")
threshold_entry = tk.Entry(frame, width=10)
threshold_entry.insert(0, str(threshold_value))
threshold_entry.grid(row=2, column=1, padx=5, sticky="w")

# Sprache umschalten
lang_label = tk.Label(frame, text="Sprache:")
lang_label.grid(row=3, column=0, sticky="w")
lang_menu = tk.OptionMenu(frame, tk.StringVar(value=language), "de", "en", command=change_language)
lang_menu.grid(row=3, column=1, sticky="w")

# Konvertieren-Button
convert_button = tk.Button(frame, text=LANGUAGES[language]["convert_button"], command=convert_file)
convert_button.grid(row=4, column=0, columnspan=3, pady=10)

root.mainloop()

