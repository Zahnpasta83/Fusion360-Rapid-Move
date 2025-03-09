import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re

def select_input_file():
    file_path = filedialog.askopenfilename(
        title="Eingabedatei auswählen",
        filetypes=[("GCode Files", "*.nc *.gcode"), ("Alle Dateien", "*.*")]
    )
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)

def select_output_folder():
    folder_path = filedialog.askdirectory(title="Zielordner auswählen")
    if folder_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, folder_path)

def convert_file():
    input_file = input_entry.get()
    output_folder = output_entry.get()
    
    if not input_file:
        messagebox.showerror("Fehler", "Bitte wählen Sie eine Eingabedatei aus!")
        return
    if not output_folder:
        messagebox.showerror("Fehler", "Bitte wählen Sie einen Zielordner aus!")
        return
    
    # Nur Dateien mit gültiger Endung verarbeiten
    valid_extensions = ('.nc', '.gcode')
    if not input_file.lower().endswith(valid_extensions):
        messagebox.showerror("Fehler", "Die ausgewählte Datei hat keine gültige Endung (.nc oder .gcode)!")
        return

    # Schwellwert aus dem Eingabefeld lesen
    try:
        threshold_height = float(threshold_entry.get())
    except ValueError:
        messagebox.showerror("Fehler", "Bitte geben Sie eine gültige Zahl für den Schwellwert ein!")
        return

    Above_Height_Threshold_prev = 1
    Current_Height = 0
    
    # Neuen Dateinamen erstellen (z. B. "Dateiname_Rapid.nc")
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    new_file_name = base_name + "_Rapid.nc"
    new_file_path = os.path.join(output_folder, new_file_name)
    
    try:
        with open(input_file, "r", encoding="utf-8", errors="ignore") as f_input, \
             open(new_file_path, "w", encoding="utf-8") as f_output:
            
            for line in f_input:
                # Kommentare und leere Zeilen überspringen
                if ";" in line or line.strip() == "" or "(" in line or ")" in line:
                    continue

                # Wenn ein Z-Wert in der Zeile vorhanden ist, diesen auswerten
                if re.search(r'[Zz]', line):
                    tokens = line.split()
                    for token in tokens:
                        if token.upper().startswith("Z"):
                            try:
                                Current_Height = float(token[1:])
                            except ValueError:
                                Current_Height = 0
                            break
                    if Current_Height > threshold_height:
                        Above_Height_Threshold = 1
                    else:
                        Above_Height_Threshold = 0
                else:
                    # Falls kein Z-Befehl vorhanden, Zustand beibehalten
                    Above_Height_Threshold = Above_Height_Threshold_prev
                
                # Zerlegen der Zeile in Tokens und Anpassen des G-Befehls
                tokens = line.split()
                new_tokens = []
                found_G = False
                for token in tokens:
                    if token.upper().startswith("G"):
                        # Bei Bewegungsbefehlen G1 oder G01:
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
                # Falls kein G-Befehl in der Zeile vorhanden, aber die Bedingungen passen, G00 einfügen
                if not found_G and Above_Height_Threshold and Above_Height_Threshold_prev:
                    new_tokens.insert(0, "G00")
                
                # Neue Zeile zusammenfügen und schreiben
                new_line = " ".join(new_tokens)
                f_output.write(new_line + "\n")
                Above_Height_Threshold_prev = Above_Height_Threshold
        
        messagebox.showinfo("Erfolg", f"Datei erfolgreich konvertiert:\n{new_file_path}")
    except Exception as e:
        messagebox.showerror("Fehler", str(e))

# Tkinter GUI aufbauen
root = tk.Tk()
root.title("GCode Rapid Move Converter")

# Eigenes Icon setzen (ICO-Datei im gleichen Verzeichnis erforderlich)
try:
    root.iconbitmap("icon.ico")  # Ersetze "icon.ico" mit dem Pfad zu deiner Icon-Datei
except:
    print("Icon konnte nicht geladen werden. Standard-Icon wird verwendet.")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# Eingabedatei-Auswahl
input_label = tk.Label(frame, text="Eingabedatei:")
input_label.grid(row=0, column=0, sticky="w")
input_entry = tk.Entry(frame, width=50)
input_entry.grid(row=0, column=1, padx=5)
input_button = tk.Button(frame, text="Auswählen", command=select_input_file)
input_button.grid(row=0, column=2, padx=5)

# Zielordner-Auswahl
output_label = tk.Label(frame, text="Zielordner:")
output_label.grid(row=1, column=0, sticky="w")
output_entry = tk.Entry(frame, width=50)
output_entry.grid(row=1, column=1, padx=5)
output_button = tk.Button(frame, text="Auswählen", command=select_output_folder)
output_button.grid(row=1, column=2, padx=5)

# Schwellwert-Eingabe
threshold_label = tk.Label(frame, text="Schwellwert (mm):")
threshold_label.grid(row=2, column=0, sticky="w")
threshold_entry = tk.Entry(frame, width=10)
threshold_entry.grid(row=2, column=1, padx=5, sticky="w")
threshold_entry.insert(0, "4")  # Standardwert auf 4 mm setzen

# Konvertieren-Button
convert_button = tk.Button(frame, text="Konvertieren", command=convert_file, width=20)
convert_button.grid(row=3, column=0, columnspan=3, pady=10)

root.mainloop()
