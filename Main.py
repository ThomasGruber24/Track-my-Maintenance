import json
import datetime
from pathlib import Path

RECORDS_FILE = Path("maintenance_records.json")

# -------------------- MAIN --------------------
def main():
    print("Welcome Thomas to Track my Maintenance!")
    print("I hope your Miata is doing well.")
    print("-------------------------------------")
    print("What would you like to do today?")
    print("1. Add a maintenance record")
    print("2. View maintenance records")
    print("3. Exit")

    choice = input("Enter your choice (1-3): ")
    if choice == '1':
        add_record()
    elif choice == '2':
        view_records()
    elif choice == '3':
        print("Goodbye!")
    else:
        print("Invalid choice. Please try again.")
        main()

# -------------------- ADD RECORD --------------------
def add_record():
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

# -------------------- JSON HELPERS --------------------
def load_json_file():
    if not RECORDS_FILE.exists():
        # Create a default JSON structure if file doesn't exist
        default_data = {
            "vehicle": {"name": "1995 Mazda Miata NA", "current_mileage": 0},
            "service_definitions": [],
            "service_log": []
        }
        save_json_file(default_data)
        return default_data

    try:
        with open(RECORDS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Error: JSON file is malformed. Resetting file.")
        default_data = {
            "vehicle": {"name": "1995 Mazda Miata NA", "current_mileage": 0},
            "service_definitions": [],
            "service_log": []
        }
        save_json_file(default_data)
        return default_data

def save_json_file(data):
    with open(RECORDS_FILE, "w") as f:
        json.dump(data, f, indent=2)

# -------------------- RUN --------------------
if __name__ == "__main__":
    main()
