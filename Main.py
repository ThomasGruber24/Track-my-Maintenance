# Imports
import json
import os
import datetime
import tkinter as tk
import re

# Froms
from pathlib import Path
from logging import root
from cProfile import label
from tkinter import messagebox



VEHICLE_FOLDER = "vehicles"

# -------------------- MAIN --------------------
# User interface for adding/viewing maintenance records. Uses JSON file for storage.
# Moving from a console-based to a proper GUI using TKinter.
def main():

    """

    old code for console interface:
    print("Welcome Thomas to Track my Maintenance!")
    print("I hope your Miata is doing well.")
    print("-------------------------------------")
    print("What would you like to do today?")
    print("1. Add a maintenance record")
    print("2. View maintenance records")
    print("3. Exit")
    """
    # -------------------- TKINTER GUI --------------------
    root = tk.Tk()
    root.title("Maintenance Tracker")

    titleLabel = tk.Label(root, text="Maintenance Tracker", font=("Arial", 24))
    titleLabel.pack(pady=20)

    # -------------------- MENU --------------------

    # framework
    menuframe = tk.Frame(root)
    menuframe.columnconfigure(0, weight=1)
    menuframe.columnconfigure(1, weight=1)
    menuframe.columnconfigure(2, weight=1)
    menuframe.columnconfigure(3, weight=1)

    # content area
    content_frame = tk.Frame(root)
    content_frame.pack(fill="both", expand=True)


    # buttons for the framwork
    btn1 = tk.Button(menuframe, text="Add Record", font=("Arial", 12), command=lambda: add_record(content_frame))
    btn1.grid(row=0, column=0, sticky="ew") #sticky == ewwy
    btn2 = tk.Button(menuframe, text="View Records", font=("Arial", 12), command=lambda: view_records(content_frame))
    btn2.grid(row=0, column=1, sticky="ew")
    btn3 = tk.Button(menuframe, text="Create New Vehicle", font=("Arial", 12), command=lambda: create_new_vehicle(content_frame))
    btn3.grid(row=0, column=2, sticky="ew")
    btn4 = tk.Button(menuframe, text="Exit", font=("Arial", 12), command=root.quit)
    btn4.grid(row=0, column=3, sticky="ew")

    

    menuframe.pack(pady=10, fill="x")
    
    # --------------------- FULLSCREEN --------------------
    root.state("zoomed")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.geometry(f"{screen_width}x{screen_height}")

    root.mainloop()
    
"""
This section is for records. Here there is ADD record, VIEW records, and CREATE new records.
All of these will be using or creating a JSON file to store the data.
"""
# -------------------- ADD RECORD --------------------
# I will be # or """ out old code for the new code.
def add_record(frame):
    """
    print("Adding a maintenance record...")
    continue_adding = True

    while continue_adding:
        data = load_json_file()  # Load full JSON
        vehicle = data["vehicle"]
        service_defs = data["service_definitions"]

        date = datetime.date.today()
        current_mileage = vehicle["current_mileage"]
        print(f"Current recorded mileage: {current_mileage}")

        # ---------------- INPUT MILEAGE ----------------
        mileage_passed = False
        while not mileage_passed:
            try:
                mileage = int(input("Enter the mileage at the time of service: "))
            except ValueError:
                print("Please enter a valid number.")
                continue

            if mileage < current_mileage:
                print("Error: Mileage cannot be less than the previous recorded mileage.")
            else:
                mileage_passed = True

        # ---------------- SELECT SERVICE ----------------
        print("What type of service was performed?")
        for i, svc in enumerate(service_defs, 1):
            print(f"{i}. {svc['name']}")

        try:
            service_choice = int(input(f"Enter your choice (1-{len(service_defs)}): "))
        except ValueError:
            service_choice = None

        if service_choice and 1 <= service_choice <= len(service_defs):
            service = service_defs[service_choice - 1]
        else:
            # Manual entry if invalid choice
            service_name = input("Invalid choice. Enter service name manually: ")
            service = {
                "id": "other",
                "name": service_name,
                "interval_miles": None,
                "interval_months": None,
                "last_serviced_date": None,
                "last_serviced_mileage": None,
                "next_service_date": None,
                "next_service_mileage": None
            }
            # Add to definitions so future logs can use it
            service_defs.append(service)
        

        # ---------------- UPDATE SERVICE LOG ----------------
        record = {
            "date": str(date),
            "service": service["name"],
            "mileage": mileage
        }
        data["service_log"].append(record)

        # ---------------- UPDATE SERVICE DEFINITIONS ----------------
        service["last_serviced_date"] = str(date)
        service["last_serviced_mileage"] = mileage

        # Calculate next service
        if service.get("interval_miles"):
            service["next_service_mileage"] = mileage + service["interval_miles"]
        if service.get("interval_months"):
            next_date = date + datetime.timedelta(days=service["interval_months"] * 30)
            service["next_service_date"] = str(next_date)

        # ---------------- UPDATE VEHICLE ----------------
        vehicle["current_mileage"] = mileage

        # ---------------- SAVE ----------------
        save_json_file(data)

        print(f"Record added: Date: {date}, Service: {service['name']}, Mileage: {mileage}")

        # Continue?
        another = input("Would you like to add another record? (y/n): ").lower()
        if another != 'y':
            continue_adding = False

    print("Finished adding records.")
    """
    clear_frame()

    datta = load_json_file()
    vehicle = datta["vehicle"]
    service_defs = datta["service_definitions"]

    current_mileage = vehicle["current_mileage"]

    tk.Label(frame, text="Add Mainten")


# -------------------- VIEW RECORDS --------------------
def view_records():
    data = load_json_file()
    service_log = data.get("service_log", [])

    if not service_log:
        print("No maintenance records logged yet.")
        return

    print("\nService Log:\n")
    for record in service_log:
        print(json.dumps(record, indent=2))
        print("-" * 40)

# -------------------- CREATE NEW VEHICLE --------------------
def create_new_vehicle(frame):
    clear_frame(frame)

    tk.Label(frame, text="Create New Vehicle", font=("Arial", 18)).pack(pady=10)

    # ----------------- VEHICLE INFO INPUTS -----------------
    # ----------------------- TKinter -----------------------
    # Year
    tk.Label(frame, text="Year:", font=("Arial", 12)).pack()
    year_entry = tk.Entry(frame, font=("Arial", 12))
    year_entry.pack()

    # Make
    tk.Label(frame, text="Make:", font=("Arial", 12)).pack()
    make_entry = tk.Entry(frame, font=("Arial", 12))
    make_entry.pack()

    # Model
    tk.Label(frame, text="Model:", font=("Arial", 12)).pack()
    model_entry = tk.Entry(frame, font=("Arial", 12))
    model_entry.pack()

    # Millage
    tk.Label(frame, text="Current Mileage:", font=("Arial", 12)).pack()
    mileage_entry = tk.Entry(frame, font=("Arial", 12))
    mileage_entry.pack()

    # ----------------------- SUBMIT BUTTON -----------------------
    def submit_vehicle():
        year = year_entry.get()
        make = make_entry.get()
        model = model_entry.get()
        mileage = mileage_entry.get()   

        if not (year and make and model):
            messagebox.showerror("Error", "All fields are required.")
            return

        success, msg = create_json_file(year, make, model, mileage)
        if success:
            messagebox.showinfo("Success", msg)
            view_records()  # Go to view records after creating vehicle
        else:
            messagebox.showerror("Error", msg)
    
    submit_btn = tk.Button(frame, text="Create Vehicle", font=("Arial", 12), command=submit_vehicle).pack(pady=10)

# -------------------- JSON HELPERS --------------------

# --------------------- LOAD/ SAVE JSON --------------------
def load_json_file(vehicle_file):
    if not vehicle_file:
        raise ValueError("No vehicle file provided!")

    filepath = os.path.join(VEHICLE_FOLDER, vehicle_file)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Vehicle file not found: {filepath}")

    with open(filepath, "r") as file:
        data = json.load(file)
    return data


def save_json_file(data, vehicle_file):
    filepath = os.path.join(VEHICLE_FOLDER, vehicle_file)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


# -------------------- VEHICLE JSON CREATION --------------------
def create_json_file(year, make, model, mileage):
    folder = "vehicles"

    # Ensure folder exists
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Remove spaces from make/model
    filename = f"{year}{make.replace(' ', '')}{model.replace(' ', '')}.json"
    filepath = os.path.join(folder, filename)

    # Prevent overwriting existing vehicle
    if os.path.exists(filepath):
        return False, "Vehicle already exists."

    data = {
        "vehicle": {
            "year": int(year),
            "make": make,
            "model": model,
            "current_mileage": int(mileage)
        },
        "service_definitions": [],
        "service_log": []
    }

    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)

    return True, "Vehicle created successfully."

# -------------------- GENERAL HELPERS --------------------
"""
This sections is for the general things that dont really have a place to go.
"""
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def get_vehicle_files():
    if not os.path.exists(VEHICLE_FOLDER):
        os.makedirs(VEHICLE_FOLDER)
    return [f for f in os.listdir(VEHICLE_FOLDER) if f.endswith(".json")]

def format_vehicle_name(filename):
    name=filename.replace(".json", "")
    year = name[:4]
    make_model = name[4:]

    parts = re.findall(r'[A-Z][a-z]*', make_model)
    return f"{year} {' '.join(parts)}" 

def add_record(frame):
    clear_frame(frame)
    selected_vehicle = [None]  # mutable container to store current selection

    # Vehicle selector at the top
    def vehicle_chosen(vehicle_file):
        selected_vehicle[0] = vehicle_file
        load_add_form(vehicle_file)  # Load the form for this vehicle

    build_vehicle_selector(frame, vehicle_chosen)

def load_add_form(vehicle_file):
    # Example: Add labels, entries, buttons
    # This function assumes 'frame' is already cleared below the selector
    print("Loading form for:", vehicle_file)

# -------------------- UNIVERSAL DISPLAY --------------------
"""
This section is for display items that will be used multiple times.
"""


def build_vehicle_selector(frame, callback):
    selector_frame = tk.Frame(frame)
    selector_frame.pack(pady=10, fill="x")

    vehicle_files = get_vehicle_files()
    if not vehicle_files:
        tk.Label(selector_frame, text="No vehicles found.").pack()
        return None

    # Map display names to actual filenames
    display_map = {format_vehicle_name(f): f for f in vehicle_files}
    selected_display = tk.StringVar()
    selected_display.set(list(display_map.keys())[0])

    dropdown = tk.OptionMenu(selector_frame, selected_display, *display_map.keys())
    dropdown.pack(side="left", padx=10)

    def on_select():
        vehicle_file = display_map[selected_display.get()]
        callback(vehicle_file)  # Tell the screen which vehicle to operate on

    tk.Button(selector_frame, text="Select Vehicle", command=on_select).pack(side="left", padx=10)

    return selector_frame

# -------------------- RUN --------------------
if __name__ == "__main__":
    main()
