from hl7_seamaty import parse_hl7_message

# Example usage
message = """
MSH|^~\&|SMT|VChmey
S|||20201207150940||ORU^R01|9|P|2.3.1|A|||2||ASCII|||V1.00.00.79|<CR>
PID|9|||||||||||||||||0 |||||||||||||<CR>
OBR|9||1 | 120000001|||20201207150640|||||||||||10^^^Before surgery 9 item|0^0^0|QC1||||||||||||||||||||||||||||<CR> OBX| 1 |NM|BUN/CREA|BUN/CREA|68|||N |||F|||||||<CR>
OBX|2 |NM|U/C|U/C|68|||N |||F|||||||<CR>
OBX|3 |NM|CK|CK|381|U/L||N |||F|||||||<CR>
OBX|4 |NM|AST|AST|323|U/L|300^200|N|||F|||||||<CR>
OBX|5 |NM|GLU|GLU| 19|mg/dL||N|||F|||||||<CR>
OBX|6 |NM|ALP|ALP|8 |U/L| 10^10|N|||F|||||||<CR>
OBX|7 |NM|Crea|Crea|2.2|mg/dL||N|||F|||||||<CR>
OBX|8 |NM|ALT|ALT|650|U/L|600|N|> 650||F|||||||<CR>
OBX|9 |NM|BUN|BUN|37|mg/dL||H|||F|||||||<CR>
OBX| 10|NM|UREA|UREA|80|mg/dL||N|||F|||||||<CR>
OBX| 11|NM|LDH|LDH|86|U/L||N|||F|||||||<CR>
OBX| 12|NM|TP|TP|2.2|g/dL||N|||F|||||||<CR>
<EB><CR>
"""
print(message)

result = parse_hl7_message(message)
print(result['formatted_output'])

