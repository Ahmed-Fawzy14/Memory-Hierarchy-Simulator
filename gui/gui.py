from tkinter import *
from tkinter import filedialog, messagebox
from backend import *  # Ensure this is correctly implemented

def load_file_to_textbox(textbox):
    """Allows the user to load a file and populate the specified Text widget."""
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            data = file.read()
            textbox.delete("1.0", END)
            textbox.insert(END, data)

def validate_addresses(addresses, format_type):
    """Validates the addresses based on the selected format (binary or decimal)."""
    address_list = [addr.strip() for addr in addresses.split(",") if addr.strip()]
    if format_type == "decimal":
        for addr in address_list:
            if not addr.isdigit():
                raise ValueError(f"Invalid decimal address: {addr}")
    elif format_type == "binary":
        for addr in address_list:
            if not all(char in "01" for char in addr):  # Validate binary format
                raise ValueError(f"Invalid binary address: {addr}")
    return address_list

def preprocess_addresses(addresses, format_type):
    """
    Validates and converts addresses to integers based on the format type (binary or decimal).
    """
    address_list = validate_addresses(addresses, format_type)
    if format_type == "binary":
        # Convert binary strings to integers
        return [int(addr, 2) for addr in address_list]
    # Convert decimal strings to integers
    return [int(addr) for addr in address_list]


root = Tk()
root.title("Memory Hierarchy Simulator")
root.geometry("900x650")
root.configure(bg="#f7f7f7")

# Title Label
titleLabel = Label(root, text="Memory Hierarchy Simulator", font=("Helvetica", 18, "bold"), bg="#f7f7f7")
titleLabel.grid(row=0, column=0, columnspan=4, pady=(10, 10), padx=(10, 10), sticky="w")

# Syntax Instructions
syntaxText = """Instructions:
This simulator uses direct mapping to analyze memory hierarchy hits and misses.
Input addresses manually or load from files, and choose the input format (binary or decimal).

Examples:
  Decimal: 800, 200, 50, 54, 40
  Binary: 1100100, 1011, 110, 100010, 110111

Separate addresses with commas. Enjoy using the simulator! :) """

syntaxLabel = Label(root, text=syntaxText, font=("Helvetica", 10), justify="left", bg="#f7f7f7", wraplength=400)
syntaxLabel.grid(row=1, column=0, columnspan=2, pady=(10, 10), padx=(10, 10), sticky="w")

# Input Format Selection
format_frame = LabelFrame(root, text="Address Input Format", font=("Helvetica", 12), bg="#f7f7f7", padx=5, pady=5)
format_frame.grid(row=1, column=2, columnspan=2, pady=(10, 10), padx=(10, 10), sticky="nsew")

address_format = StringVar(value="decimal")  # Default format is decimal
decimal_button = Radiobutton(format_frame, text="Decimal", variable=address_format, value="decimal", font=("Helvetica", 10), bg="#f7f7f7")
binary_button = Radiobutton(format_frame, text="Binary", variable=address_format, value="binary", font=("Helvetica", 10), bg="#f7f7f7")
decimal_button.pack(anchor="w", pady=2)
binary_button.pack(anchor="w", pady=2)

# Textbox Frames
textbox_frame = Frame(root, bg="#f7f7f7")
textbox_frame.grid(row=2, column=0, columnspan=4, pady=(10, 10), padx=(10, 10), sticky="nsew")

# Data Addresses Frame
data_frame = LabelFrame(textbox_frame, text="Data Addresses", font=("Helvetica", 12), bg="#f7f7f7", padx=5, pady=5)
data_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

dataBox = Text(data_frame, height=10, width=40, font=("Courier", 10), wrap="word")
dataBox.pack(side="left", fill="both", expand=True)
dataScrollbar = Scrollbar(data_frame, command=dataBox.yview)
dataScrollbar.pack(side="right", fill="y")
dataBox.config(yscrollcommand=dataScrollbar.set)

dataLoadButton = Button(data_frame, text="Load from File", command=lambda: load_file_to_textbox(dataBox), bg="#d9d9d9")
dataLoadButton.pack(pady=5)

# Instruction Addresses Frame
instruction_frame = LabelFrame(textbox_frame, text="Instruction Addresses", font=("Helvetica", 12), bg="#f7f7f7", padx=5, pady=5)
instruction_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

instructionBox = Text(instruction_frame, height=10, width=40, font=("Courier", 10), wrap="word")
instructionBox.pack(side="left", fill="both", expand=True)
instructionScrollbar = Scrollbar(instruction_frame, command=instructionBox.yview)
instructionScrollbar.pack(side="right", fill="y")
instructionBox.config(yscrollcommand=instructionScrollbar.set)

instructionLoadButton = Button(instruction_frame, text="Load from File", command=lambda: load_file_to_textbox(instructionBox), bg="#d9d9d9")
instructionLoadButton.pack(pady=5)

# Input Fields for Parameters
parameter_frame = Frame(root, bg="#f7f7f7")
parameter_frame.grid(row=3, column=0, columnspan=4, pady=(10, 10), padx=(10, 10), sticky="nsew")

params = {
    "Total Size": IntVar(value=0),
    "Line Size": IntVar(value=0),
    "Access Time": IntVar(value=0),
    "Memory Access Time": IntVar(value=0),
    "Byte Size": IntVar(value=1),
}

for idx, (label_text, var) in enumerate(params.items()):
    frame = Frame(parameter_frame, bg="#f7f7f7")
    frame.grid(row=0, column=idx, padx=(5, 10), pady=(5, 5), sticky="w")
    label = Label(frame, text=label_text, font=("Helvetica", 12), bg="#f7f7f7")
    label.pack(anchor="w")
    entry = Entry(frame, textvariable=var, font=("Courier", 12), width=10)
    entry.pack()

def simulate():
    try:
        dataAddresses = dataBox.get("1.0", END).strip()
        instructionAddresses = instructionBox.get("1.0", END).strip()

        if not dataAddresses or not instructionAddresses:
            raise ValueError("Data or instruction addresses cannot be empty.")

        format_type = address_format.get()
        dataAddresses = preprocess_addresses(dataAddresses, format_type)
        instructionAddresses = preprocess_addresses(instructionAddresses, format_type)

        for key, value in params.items():
            if value.get() <= 0:
                raise ValueError(f"{key} must be a positive integer.")

        totalSize = params["Total Size"].get()
        lineSize = params["Line Size"].get()
        accessTime = params["Access Time"].get()
        memoryAccessTime = params["Memory Access Time"].get()

        sim_window = Toplevel(root)
        sim_window.title("Simulation Results")
        sim_window.geometry("600x400")

        sim_output = Text(sim_window, wrap="word", font=("Courier", 10))
        sim_output.pack(side="left", fill="both", expand=True)
        scrollbar = Scrollbar(sim_window, command=sim_output.yview)
        scrollbar.pack(side="right", fill="y")
        sim_output.config(yscrollcommand=scrollbar.set)

        def output_to_gui(*args):
            sim_output.insert(END, " ".join(map(str, args)) + "\n")
            sim_output.yview_moveto(1)

        run_Program(totalSize, lineSize, accessTime, memoryAccessTime, instructionAddresses, dataAddresses, output_to_gui, format_type)

    except Exception as e:
        messagebox.showerror("Simulation Error", str(e))

simulateButton = Button(root, text="Run Simulation", command=simulate, font=("Helvetica", 14), bg="#666666", fg="white", padx=20, pady=5)
simulateButton.grid(row=4, column=0, columnspan=4, pady=(10, 20), sticky="n")

root.mainloop()