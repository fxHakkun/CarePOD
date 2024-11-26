import uuid
from datetime import datetime
from hl7_seamaty import parse_hl7_message

# Function to generate unique IDs
def generate_unique_id():
    return str(uuid.uuid4())

# Placeholder for server communication (empty, to be filled based on actual implementation)
def send_to_server(hl7_message: str):
    # Implement the server communication logic here
    # Example: Use HTTP, TCP/IP, or other protocol
    pass

# Gather patient information (PID)
def gather_patient_information():
    print("Enter Patient Information:")
    patient_id = input("Patient ID: ").strip()
    name = input("Patient Name: ").strip()
    age = input("Age: ").strip()
    sex = input("Sex (M/F/O/U): ").strip().upper()
    race = input("Race (Optional, leave blank if none): ").strip()
    
    return {
        "id": patient_id,
        "name": name,
        "age": age,
        "sex": sex,
        "race": race if race else None
    }

# Gather message details (MSH)
def gather_message_details():
    print("Enter Message Header Details:")
    sending_app = input("Sending Application: ").strip()
    sending_facility = input("Sending Facility: ").strip()
    message_type = input("Message Type (e.g., ORU^R01): ").strip()
    version = input("HL7 Version (e.g., 2.3.1): ").strip()
    
    return {
        "sending_app": sending_app,
        "sending_facility": sending_facility,
        "datetime": datetime.now().strftime("%Y%m%d%H%M%S"),
        "message_type": message_type,
        "message_id": generate_unique_id(),
        "version": version
    }

# Gather observation results (OBX)
def gather_observation_results():
    print("Enter Observation Results (OBX):")
    results = []
    while True:
        observation_name = input("Observation Name (or 'done' to finish): ").strip()
        if observation_name.lower() == 'done':
            break
        value = input(f"Value for {observation_name}: ").strip()
        units = input(f"Units for {observation_name} (Optional, leave blank if none): ").strip()
        reference_range = input(f"Reference Range for {observation_name} (Optional, leave blank if none): ").strip()
        abnormal_flags = input(f"Abnormal Flags for {observation_name} (Optional, leave blank if none): ").strip()
        status = input(f"Status for {observation_name} (e.g., F - Final): ").strip()

        result = {
            "set_id": generate_unique_id(),
            "value_type": "NM",  # Assuming numeric for this template
            "observation_identifier": observation_name,
            "observation_name": observation_name,
            "value": value,
            "units": units if units else None,
            "reference_range": reference_range if reference_range else None,
            "abnormal_flags": abnormal_flags if abnormal_flags else None,
            "status": status
        }
        results.append(result)
    return results

# Main program
if __name__ == "__main__":
    print("Starting CarePod Data Gathering...")
    
    # Generate unique board ID
    board_unique_id = generate_unique_id()
    print(f"Board Unique ID: {board_unique_id}")
    
    # Gather patient information
    patient_info = gather_patient_information()
    
    # Gather message details
    message_details = gather_message_details()
    
    # Gather observation results
    obx_results = gather_observation_results()
    
    # Construct the HL7 message
    hl7_message = {
        "sending_app": message_details["sending_app"],
        "sending_facility": message_details["sending_facility"],
        "datetime": message_details["datetime"],
        "message_type": message_details["message_type"],
        "message_id": message_details["message_id"],
        "version": message_details["version"],
        "patient": patient_info,
        "order": {
            "set_id": "1",  # Hardcoded for this example
            "sample_number": generate_unique_id(),
            "device_id": board_unique_id,
            "collection_time": message_details["datetime"],
            "specimen_type": "TBD",  # Replace with actual specimen type
            "examiner": "TBD",       # Replace with actual examiner details
            "department": "TBD"      # Replace with actual department details
        },
        "results": obx_results
    }
    
    # Convert to HL7 formatted string
    print("\nGenerating HL7 message...\n")
    formatted_hl7 = parse_hl7_message(hl7_message)["formatted_output"]
    print(formatted_hl7)
    
    # Send HL7 message to server
    print("\nSending HL7 message to server...\n")
    send_to_server(formatted_hl7)
