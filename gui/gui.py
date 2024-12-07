from tkinter import *
from backend import *
root = Tk()
root.title("Memory Hierarchy Simulator")
root.geometry("800x600")
root.configure(bg="#f0f0f0") 

titleLabel = Label(root, text="Memory Hierarchy Simulator", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
titleLabel.grid(row=0, column=0, columnspan=3, pady=(10, 20), sticky="w", padx=(20, 0))

syntaxText = """INSTRUCTIONS:\nThis is a memory-hierarchy simulator that uses direct mapping to output statistics regarding the hits and misses.\n
The user has full control of the dimensions of the memory, and the memory locations that ar read into the memory.\n
Please sepereate the memory addresses with a coma, all of which must be decimal integers.\n
Below is an example of the required syntax:\n
\t800, 200, 50, 54, 40\n
\t100, 3, 6, 34, 55, 77\n
Enjoy using the simulator :)"""

syntaxLabel = Label(root, text=syntaxText, font=("Helvetica", 10), justify="left", anchor="nw", bg="#f0f0f0", wraplength=300)
syntaxLabel.grid(row=1, column=0, padx=(20, 10), sticky="nw")

# Frame to hold the data Text box and scrollbar
data_frame = Frame(root)
data_frame.grid(row=1, column=1, padx=(10, 5), pady=(10, 0), sticky="nsew")

# Label for Data Text box
dataLabel = Label(data_frame, text="Data Addresses", font=("Helvetica", 12, "bold"), bg="#f0f0f0")
dataLabel.pack(anchor="w")

# Data Text box
dataBox = Text(data_frame, height=20, width=35, font=("Courier", 10), wrap="word")
dataBox.pack(side="left", fill="both", expand=True)
dataScrollbar = Scrollbar(data_frame, command=dataBox.yview)
dataScrollbar.pack(side="right", fill="y")
dataBox.config(yscrollcommand=dataScrollbar.set)



# Frame to hold the memory Text box and scrollbar
instruction_frame = Frame(root)
instruction_frame.grid(row=1, column=2, padx=(10, 5), pady=(10, 0), sticky="nsew")

# Label for Memory Text box
memoryLabel = Label(instruction_frame, text="Instruction Addresses", font=("Helvetica", 12, "bold"), bg="#f0f0f0")
memoryLabel.pack(anchor="w")

# Memory Text box
instruction_frameBox = Text(instruction_frame, height=20, width=35, font=("Courier", 10), wrap="word")
instruction_frameBox.pack(side="left", fill="both", expand=True)
instruction_frameScrollbar = Scrollbar(instruction_frame, command=instruction_frameBox.yview)
instruction_frameScrollbar.pack(side="right", fill="y")
instruction_frameBox.config(yscrollcommand=instruction_frameScrollbar.set)


total_size_frame = Frame(root, bg="#f0f0f0")
total_size_frame.grid(row=2, column=0, padx=(5, 20), pady=(10, 10), sticky="nw")

total_size_label = Label(total_size_frame, text="Total Size", font=("Helvetica", 12, "bold"), bg="#f0f0f0")
total_size_label.pack(anchor="w")

total_size_value = IntVar(value=0)  # Default value is 0
total_size_entry = Entry(total_size_frame, textvariable=total_size_value, font=("Courier", 12), width=10)
total_size_entry.pack(side="left", padx=(0, 10))



line_size_frame = Frame(root, bg="#f0f0f0")
line_size_frame.grid(row=2, column=1, padx=(5, 20), pady=(10, 10), sticky="nw")

line_size_label = Label(line_size_frame, text="Line Size", font=("Helvetica", 12, "bold"), bg="#f0f0f0")
line_size_label.pack(anchor="w")

line_size_value = IntVar(value=0)  # Default value is 0
line_size_entry = Entry(line_size_frame, textvariable=line_size_value, font=("Courier", 12), width=10)
line_size_entry.pack(side="left", padx=(0, 10))


access_time_frame = Frame(root, bg="#f0f0f0")
access_time_frame.grid(row=2, column=2, padx=(5, 20), pady=(10, 10), sticky="nw")

access_time_label = Label(access_time_frame, text="Access Time", font=("Helvetica", 12, "bold"), bg="#f0f0f0")
access_time_label.pack(anchor="w")

access_time_value = IntVar(value=0)  # Default value is 0
access_time_entry = Entry(access_time_frame, textvariable=access_time_value, font=("Courier", 12), width=10)
access_time_entry.pack(side="left", padx=(0, 10))



memory_access_time_frame = Frame(root, bg="#f0f0f0")
memory_access_time_frame.grid(row=2, column=3, padx=(5, 20), pady=(10, 10), sticky="nw")

memory_access_time_label = Label(memory_access_time_frame, text="Memory Access Time", font=("Helvetica", 12, "bold"), bg="#f0f0f0")
memory_access_time_label.pack(anchor="w")

memory_access_time_value = IntVar(value=0)  # Default value is 0
memory_access_time_entry = Entry(memory_access_time_frame, textvariable=memory_access_time_value, font=("Courier", 12), width=10)
memory_access_time_entry.pack(side="left", padx=(0, 10))


# Button to run the simulation

def simulate():
    dataAddresses = dataBox.get("1.0", END)
    instructionAddresses = instruction_frameBox.get("1.0", END)
    #total_Size, line_Size, access_Time, memory_Access_Time, instruction_Sequence, data_Sequence

    totalSize = total_size_value.get()
    lineSize = line_size_value.get()
    accessTime = access_time_value.get()
    memoryAccessTime = memory_access_time_value.get()

    sim_window = Toplevel(root)
    sim_window.title("Simulation Results")
    sim_window.geometry("600x600")

    frame = Frame(sim_window)
    frame.pack(fill="both", expand=True)

    # Text widget to display the simulation output
    sim_output = Text(frame, wrap="word", font=("Courier", 10))
    sim_output.pack(side="left", fill="both", expand=True)

    # Scrollbar widget
    scrollbar = Scrollbar(frame, orient="vertical", command=sim_output.yview)
    scrollbar.pack(side="right", fill="y")

    # Configure the Text widget to work with the scrollbar
    sim_output.config(yscrollcommand=scrollbar.set)

    def output_to_gui(*args):
        text = " ".join(str(arg) for arg in args)  # Join multiple arguments as a single string
        sim_output.insert(END, text + "\n")
        sim_output.yview_moveto(0)  # Scroll to the top after each insert

    run_Program(totalSize, lineSize, accessTime, memoryAccessTime, instructionAddresses, dataAddresses, output_to_gui)

simulateButton = Button(root, text="Run Simulation", command=simulate, font=("Helvetica", 12), bg="#666666", fg="white")
simulateButton.grid(row=3, column=0, pady=(10, 20), sticky="w", padx=(20, 0))
root.mainloop()
