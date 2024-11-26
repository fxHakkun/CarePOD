from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class OBXResult:
    set_id: str
    value_type: str
    observation_identifier: str
    observation_name: str
    value: str
    units: Optional[str]
    reference_range: Optional[str]
    abnormal_flags: Optional[str]
    status: str

@dataclass
class Patient:
    id: str
    name: str
    age: str
    sex: str
    race: Optional[str]

@dataclass
class OrderInfo:
    set_id: str
    sample_number: str
    device_id: str
    collection_time: datetime
    specimen_type: str
    examiner: str
    department: str

@dataclass
class HL7Message:
    sending_app: str
    sending_facility: str
    datetime: datetime
    message_type: str
    message_id: str
    version: str
    patient: Optional[Patient]
    order: Optional[OrderInfo]
    results: List[OBXResult]

class HL7Parser:
    def __init__(self):
        self.field_separator = '|'
        self.component_separator = '^'
        
    def parse_message(self, message: str) -> HL7Message:
        """Parse a complete HL7 message and return structured data"""
        segments = message.split('<CR>')
        segments = [s.strip() for s in segments if s.strip()]
        
        # Parse each segment type
        msh_segment = next(s for s in segments if s.startswith('MSH'))
        pid_segment = next((s for s in segments if s.startswith('PID')), None)
        obr_segment = next((s for s in segments if s.startswith('OBR')), None)
        obx_segments = [s for s in segments if s.startswith('OBX')]
        
        # Parse MSH (Message Header)
        msh_fields = self._split_segment(msh_segment)
        message_header = {
            'sending_app': msh_fields[2],
            'sending_facility': msh_fields[3],
            'datetime': msh_fields[6],
            'message_type': msh_fields[8],
            'message_id': msh_fields[9],
            'version': msh_fields[11]
        }
        
        # Parse PID (Patient Information)
        patient = None
        if pid_segment:
            pid_fields = self._split_segment(pid_segment)
            patient = Patient(
                id=pid_fields[2],
                name=pid_fields[5],
                age=pid_fields[7].split(self.component_separator)[0],
                sex=pid_fields[8],
                race=pid_fields[10] if pid_fields[10] != '' else None
            )
        
        # Parse OBR (Order Information)
        order = None
        if obr_segment:
            obr_fields = self._split_segment(obr_segment)
            order = OrderInfo(
                set_id=obr_fields[1],
                sample_number=obr_fields[3],
                device_id=obr_fields[4],
                collection_time=obr_fields[7],
                specimen_type=obr_fields[15],
                examiner=obr_fields[16],
                department=obr_fields[17]
            )
        
        # Parse OBX (Results)
        results = []
        for obx in obx_segments:
            fields = self._split_segment(obx)
            result = OBXResult(
                set_id=fields[1],
                value_type=fields[2],
                observation_identifier=fields[3],
                observation_name=fields[4],
                value=fields[5],
                units=fields[6] if fields[6] != '' else None,
                reference_range=fields[7] if fields[7] != '' else None,
                abnormal_flags=fields[8] if fields[8] != '' else None,
                status=fields[11]
            )
            results.append(result)
        
        return HL7Message(
            sending_app=message_header['sending_app'],
            sending_facility=message_header['sending_facility'],
            datetime=message_header['datetime'],
            message_type=message_header['message_type'],
            message_id=message_header['message_id'],
            version=message_header['version'],
            patient=patient,
            order=order,
            results=results
        )
    
    def _split_segment(self, segment: str) -> List[str]:
        """Split a segment into fields, handling the special case of MSH segment"""
        if segment.startswith('MSH'):
            # Special handling for MSH segment where the separator is part of the first field
            fields = ['MSH', segment[3:4]]  # First field is MSH, second is the separator
            fields.extend(segment[4:].split(self.field_separator))
        else:
            fields = segment.split(self.field_separator)
        return fields

    def format_results(self, message: HL7Message) -> str:
        """Format the parsed results into a human-readable string"""
        output = []
        output.append(f"Message Details:")
        output.append(f"Sending Application: {message.sending_app}")
        output.append(f"Sending Facility: {message.sending_facility}")
        output.append(f"DateTime: {message.datetime}")
        output.append(f"Message Type: {message.message_type}")
        output.append(f"Version: {message.version}\n")
        
        if message.patient:
            output.append(f"Patient Information:")
            output.append(f"Name: {message.patient.name}")
            output.append(f"ID: {message.patient.id}")
            output.append(f"Age: {message.patient.age}")
            output.append(f"Sex: {message.patient.sex}")
            if message.patient.race:
                output.append(f"Race: {message.patient.race}\n")
        
        if message.order:
            output.append(f"Order Information:")
            output.append(f"Sample Number: {message.order.sample_number}")
            output.append(f"Collection Time: {message.order.collection_time}")
            output.append(f"Specimen Type: {message.order.specimen_type}")
            output.append(f"Examiner: {message.order.examiner}")
            output.append(f"Department: {message.order.department}\n")
        
        output.append(f"Test Results:")
        for result in message.results:
            output.append(f"{result.observation_name}:")
            output.append(f"  Value: {result.value}")
            if result.units:
                output.append(f"  Units: {result.units}")
            if result.reference_range:
                output.append(f"  Reference Range: {result.reference_range}")
            if result.abnormal_flags:
                output.append(f"  Flag: {result.abnormal_flags}")
            output.append("")
        
        return "\n".join(output)

# Example usage:
def parse_hl7_message(message: str) -> Dict:
    """Main function to parse an HL7 message and return formatted results"""
    parser = HL7Parser()
    parsed_message = parser.parse_message(message)
    formatted_output = parser.format_results(parsed_message)
    
    return {
        'parsed_data': parsed_message,
        'formatted_output': formatted_output
    }