import tkinter as tk
from tkinter import messagebox

# Declare global variables
global num_processes
num_processes = 0

global num_resources
num_resources = 0

def bankers_algorithm(total_resources, available_resources, current_allocation, maximum_need, request_process,
                      request_resources):
    num_resources = len(total_resources)
    num_processes = len(current_allocation)

    # Step 1: Initialize data structures
    need = []
    for i in range(num_processes):
        need.append([maximum_need[i][j] - current_allocation[i][j] for j in range(num_resources)])

    # Step 2: Check if the requested resources are within the available resources
    for i in range(num_resources):
        if request_resources[i] > available_resources[i]:
            return False, "Resources not available"

    # Step 3: Check if the requested resources are within the need of the requesting process
    process_index = request_process - 1
    for i in range(num_resources):
        if request_resources[i] > need[process_index][i]:
            return False, "Request exceeds process need"

    # Step 4: Simulate resource allocation to determine if the system is in a safe state
    temp_available = available_resources[:]
    temp_allocation = [allocation[:] for allocation in current_allocation]

    for i in range(num_resources):
        temp_available[i] -= request_resources[i]
        temp_allocation[process_index][i] += request_resources[i]

    finish = [False] * num_processes
    safe_sequence = []
    work = temp_available[:]

    while True:
        found = False
        for i in range(num_processes):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(num_resources)):
                work = [work[j] + temp_allocation[i][j] for j in range(num_resources)]
                finish[i] = True
                safe_sequence.append(i + 1)
                found = True

        if not found:
            break

    if all(finish):
        return True, "Request can be granted. System is in a safe state.", safe_sequence
    else:
        return False, "Request cannot be granted. System is in an unsafe state.", []


def submit_request():
    # Get the input values from the GUI
    total_resources = [int(total_entries[i].get()) for i in range(num_resources)]
    available_resources = [int(available_entries[i].get()) for i in range(num_resources)]

    current_allocation = []
    maximum_need = []

    for i in range(num_processes):
        allocation_row = [int(allocation_entries[i][j].get()) for j in range(num_resources)]
        maximum_row = [int(max_entries[i][j].get()) for j in range(num_resources)]
        current_allocation.append(allocation_row)
        maximum_need.append(maximum_row)

    request_process = int(request_process_entry.get())
    request_resources = [int(request_entries[i].get()) for i in range(num_resources)]

    # Apply the Banker's algorithm to determine if the request can be granted
    is_safe, message, safe_sequence = bankers_algorithm(total_resources, available_resources, current_allocation,
                                                       maximum_need, request_process, request_resources)

    # Show the result in a message box
    messagebox.showinfo("Banker's Algorithm Result", message)

    # Print the safe sequence
    if is_safe:
        print("Safe sequence:", safe_sequence)


# Add resource entry fields
def add_resource():
    global num_resources

    resource_label = tk.Label(resources_frame, text="Resource {}".format(num_resources + 1))
    resource_label.grid(row=0, column=num_resources + 2, padx=5, pady=5)

    total_entry = tk.Entry(resources_frame, width=10)
    total_entry.grid(row=1, column=num_resources + 2, padx=5, pady=5)

    available_entry = tk.Entry(resources_frame, width=10)
    available_entry.grid(row=2, column=num_resources + 2, padx=5, pady=5)

    total_entries.append(total_entry)
    available_entries.append(available_entry)

    for i in range(num_processes):
        allocation_entry = tk.Entry(processes_frame, width=10)  # <-- Modify this line
        allocation_entry.grid(row=i + 1, column=num_resources + 2, padx=5, pady=5)  # <-- Modify this line
        allocation_entries[i].append(allocation_entry)

        max_entry = tk.Entry(max_frame, width=10)
        max_entry.grid(row=i + 1, column=num_resources + 2, padx=5, pady=5)
        max_entries[i].append(max_entry)

    num_resources += 1


# Add process entry fields
def add_process():
    global num_processes
    global max_frame  # Declare max_frame as a global variable

    process_label = tk.Label(processes_frame, text="Process {}".format(num_processes + 1))
    process_label.grid(row=num_processes + 2, column=0, padx=5, pady=5)

    allocation_entries.append([])
    max_entries.append([])

    for i in range(num_resources):
        allocation_entry = tk.Entry(processes_frame, width=10)
        allocation_entry.grid(row=num_processes + 2, column=i + 1, padx=5, pady=5)
        allocation_entries[num_processes].append(allocation_entry)

        max_entry = tk.Entry(max_frame, width=10)
        max_entry.grid(row=num_processes + 2, column=i + 1, padx=5, pady=5)
        max_entries[num_processes].append(max_entry)

    num_processes += 1

# Create the main window
root = tk.Tk()
root.title("Banker's Algorithm")

# Create frames
resources_frame = tk.Frame(root)
resources_frame.pack(padx=10, pady=10)

processes_frame = tk.Frame(root)
processes_frame.pack(padx=10, pady=10)

buttons_frame = tk.Frame(root)
buttons_frame.pack(padx=10, pady=10)

allocation_frame = tk.Frame(root)
allocation_frame.pack(padx=10, pady=10)

max_frame = tk.Frame(root)
max_frame.pack(padx=10, pady=10)


# Create a function to add a new request entry field
def add_request():
    global num_resources

    request_label = tk.Label(request_frame, text="Resource {}".format(num_resources + 1))
    request_label.grid(row=num_resources + 3, column=0, padx=5, pady=5)

    request_entry = tk.Entry(request_frame, width=10)
    request_entry.grid(row=num_resources + 3, column=1, padx=5, pady=5)

    request_labels.append(request_label)
    request_entries.append(request_entry)

    num_resources += 1

# Create the main window
window = tk.Tk()
window.title("Banker's Algorithm")

# Create a frame for resources
resources_frame = tk.Frame(window)
resources_frame.pack(pady=10)

# Create a label for resources
resources_label = tk.Label(resources_frame, text="Resources")
resources_label.grid(row=0, column=0, padx=5, pady=5)

# Create a list to store the total resource entry fields
total_entries = []
available_entries = []

# Create initial resource entry fields
num_resources = 0
add_resource()

# Create an "Add Resource" button
add_resource_button = tk.Button(resources_frame, text="Add Resource", command=add_resource)
add_resource_button.grid(row=3, column=0, padx=5, pady=5)

# Create a frame for processes
processes_frame = tk.Frame(window)
processes_frame.pack(pady=10)

# Create a label for processes
processes_label = tk.Label(processes_frame, text="Processes")
processes_label.grid(row=0, column=0, padx=5, pady=5)

# Create lists to store the allocation and maximum need entry fields
allocation_entries = []
max_entries = []

# Create initial process entry fields
num_processes = 0
add_process()

# Create an "Add Process" button
add_process_button = tk.Button(processes_frame, text="Add Process", command=add_process)
add_process_button.grid(row=0, column=1, padx=5, pady=5)

# Create frames for current allocation and maximum need
allocation_frame = tk.Frame(window)
allocation_frame.pack(pady=10)

max_frame = tk.Frame(window)
max_frame.pack(pady=10)

# Create a label for current allocation
allocation_label = tk.Label(allocation_frame, text="Current Allocation")
allocation_label.grid(row=0, column=0, padx=5, pady=5)

# Create a label for maximum need
max_label = tk.Label(max_frame, text="Maximum Need")
max_label.grid(row=0, column=0, padx=5, pady=5)

# Create a frame for the request
request_frame = tk.Frame(window)
request_frame.pack(pady=10)

# Create a label for the request
request_label = tk.Label(request_frame, text="Request")
request_label.grid(row=0, column=0, padx=5, pady=5)

# Create entry fields for the request
request_process_label = tk.Label(request_frame, text="Process:")
request_process_label.grid(row=1, column=0, padx=5, pady=5)

request_process_entry = tk.Entry(request_frame, width=10)
request_process_entry.grid(row=1, column=1, padx=5, pady=5)

request_labels = []
request_entries = []

# Create an "Add Resource" button
add_request_button = tk.Button(request_frame, text="Add Resource", command=add_request)
add_request_button.grid(row=2, column=0, padx=5, pady=5)

def add_request():
    global num_resources

    request_label = tk.Label(request_frame, text="Resource {}".format(num_resources + 1))
    request_label.grid(row=num_resources + 3, column=0, padx=5, pady=5)

    request_entry = tk.Entry(request_frame, width=10)
    request_entry.grid(row=num_resources + 3, column=1, padx=5, pady=5)

    request_labels.append(request_label)
    request_entries.append(request_entry)

    num_resources += 1

# Create a submit button
submit_button = tk.Button(window, text="Submit", command=submit_request)
submit_button.pack(pady=10)

# Run the main loop
window.mainloop()


