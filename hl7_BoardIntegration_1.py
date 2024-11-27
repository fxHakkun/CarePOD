import uuid
from datetime import datetime
import hl7_seamaty  # Importing your HL7 processing module

# Function to generate unique IDs
def generate_unique_id():
    return str(uuid.uuid4())

# Establish connection to the server
def connect_to_server():
    """Establishes a connection to the server to retrieve MSH and PID data."""
    # Placeholder for server connection logic
    # Example: Replace with actual communication (HTTP, TCP/IP, WebSocket, etc.)
    print("Connecting to server...")
    # Mocking received data for MSH and PID
    msh_data = {
        "sending_app": "SMT",
        "sending_facility": "VChmey",
        "datetime": datetime.now().strftime("%Y%m%d%H%M%S"),
        "message_type": "ORU^R01",
        "message_id": generate_unique_id(),
        "version": "2.3.1"
    }
    pid_data = {
        "id": "9",
        "name": "John Doe",
        "age": "25",
        "sex": "M",
        "race": "White"
    }
    print("Data retrieved from server.")
    return msh_data, pid_data

# Establish connection to the POCT device
def connect_to_poct_device():
    """Establishes a connection to the POCT device to retrieve OBX data."""
    # Placeholder for POCT connection logic (e.g., serial, GPIO)
    # Example: Replace with actual hardware communication
    print("Connecting to POCT device...")
    obx_results = []  # Mock data for testing purposes
    for i in range(1, 6):  # Simulate 5 test results
        obx_results.append({
            "set_id": generate_unique_id(),
            "value_type": "NM",
            "observation_identifier": f"Test{i}",
            "observation_name": f"Test{i} Name",
            "value": f"{i * 10}",
            "units": "mg/dL" if i % 2 == 0 else None,
            "reference_range": "10-100" if i % 2 == 0 else None,
            "abnormal_flags": "N" if i % 2 == 0 else "H",
            "status": "F"  # Final
        })
    print("Data retrieved from POCT device.")
    return obx_results

# Send HL7 message to the server
def send_to_server(hl7_message: str):
    """Sends the constructed HL7 message to the server."""
    # Placeholder for server sending logic
    # Example: Use HTTP POST or TCP/IP to send the message
    print("Sending message to the server...")
    print(hl7_message)  # Display for testing
    # Implement actual communication logic here

def construct_hl7_message(message) -> str:
    """Constructs and returns a raw HL7 message string."""
    segments = []

    # Construct MSH
    msh = f"MSH|^~\\&|{message.sending_app}|{message.sending_facility}|||" \
          f"{message.datetime}||{message.message_type}|{message.message_id}|P|{message.version}|"
    segments.append(msh)

    # Construct PID
    if message.patient:
        pid = f"PID|1|{message.patient.id}||||{message.patient.name}|||" \
              f"{message.patient.age}^{message.patient.sex}|{message.patient.race or ''}|"
        segments.append(pid)

    # Construct OBR
    if message.order:
        obr = f"OBR|{message.order.set_id}||{message.order.sample_number}|" \
              f"{message.order.device_id}|||{message.order.collection_time}|||||||||" \
              f"{message.order.specimen_type}|{message.order.examiner}|{message.order.department}|"
        segments.append(obr)

    # Construct OBX
    for result in message.results:
        obx = f"OBX|{result.set_id}|{result.value_type}|{result.observation_identifier}|" \
              f"{result.observation_name}|{result.value}|{result.units or ''}|{result.reference_range or ''}|" \
              f"{result.abnormal_flags or ''}|||{result.status}|"
        segments.append(obx)

    # Join all segments with <CR>
    return "<CR>".join(segments) + "<CR>"

# Main program
if __name__ == "__main__":
    print("Starting CarePod Medical Kiosk system...")

    # Generate a unique ID for the board
    board_unique_id = generate_unique_id()
    print(f"Generated Board Unique ID: {board_unique_id}")

    # Step 1: Connect to the server to retrieve MSH and PID data
    msh_data, pid_data = connect_to_server()

    # Step 2: Connect to the POCT device to retrieve OBX data
    obx_results = connect_to_poct_device()

    # Step 3: Construct the HL7 message

    # Create the HL7 message as a dictionary
    hl7_message = {
        "sending_app": msh_data["sending_app"],
        "sending_facility": msh_data["sending_facility"],
        "datetime": msh_data["datetime"],
        "message_type": msh_data["message_type"],
        "message_id": msh_data["message_id"],
        "version": msh_data["version"],
        "patient": pid_data,
        "order": {
            "set_id": "1",  # Example: Hardcoded order ID
            "sample_number": generate_unique_id(),
            "device_id": board_unique_id,
            "collection_time": msh_data["datetime"],
            "specimen_type": "TBD",  # Placeholder
            "examiner": "TBD",       # Placeholder
            "department": "TBD"      # Placeholder
        },
        "results": obx_results
    }

    print("Constructing HL7 message...")

    message = hl7_seamaty.HL7Message(
            sending_app=hl7_message["sending_app"],
            sending_facility=hl7_message["sending_facility"],
            datetime=hl7_message["datetime"],
            message_type=hl7_message["message_type"],
            message_id=hl7_message["message_id"],
            version=hl7_message["version"],
            patient=hl7_seamaty.Patient(
                id=hl7_message["patient"]["id"],
                name=hl7_message["patient"]["name"],
                age=hl7_message["patient"]["age"],
                sex=hl7_message["patient"]["sex"],
                race=hl7_message["patient"]["race"] ),
            order=hl7_seamaty.OrderInfo(
                set_id=hl7_message["order"]["set_id"],
                sample_number=hl7_message["order"]["sample_number"],
                device_id=hl7_message["order"]["device_id"],
                collection_time=hl7_message["order"]["collection_time"],
                specimen_type=hl7_message["order"]["specimen_type"],
                examiner=hl7_message["order"]["examiner"],
                department=hl7_message["order"]["department"]),
            results=[
                hl7_seamaty.OBXResult(
                    set_id=result["set_id"],
                    value_type=result["value_type"],
                    observation_identifier=result["observation_identifier"],
                    observation_name=result["observation_name"],
                    value=result["value"],
                    units=result["units"],
                    reference_range=result["reference_range"],
                    abnormal_flags=result["abnormal_flags"],
                    status=result["status"])
                for result in hl7_message["results"]]
        )
    raw_hl7_message = construct_hl7_message(message)
    formatted_hl7 = hl7_seamaty.HL7Parser().format_results(message)

    # Print the raw HL7 message
    print("\nRaw HL7 Message:\n")
    print(raw_hl7_message)
    # Print the formatted HL7 message
    print("\nFormatted HL7 Message:\n")
    print(formatted_hl7)

    # Send the HL7 message to the server
    send_to_server(raw_hl7_message)
