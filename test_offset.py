import numpy as np
import subprocess

opamps = [
    "SupOpAmp", "SupOpAmp_LM741", "SupOpAmp_TL081", "SupOpAmp_TL071", "SupOpAmp_LM358",
    "SupOpAmp_NE5532", "SupOpAmp_MCP601", "SupOpAmp_OP07", "SupOpAmp_OP27",
    "SupOpAmp_AD8628", "SupOpAmp_LT1028", "SupOpAmp_AD797", "SupOpAmp_OPA2134",
    "SupOpAmp_AD8009", "SupOpAmp_LMH6702", "SupOpAmp_THS3001", "SupOpAmp_L272",
    "SupOpAmp_OPA541", "SupOpAmp_LM3886", "SupOpAmp_LT1210"
]

cir_content = """* DC Offset Test
.include SupOpAmp.cir
Vcc vcc 0 15
Vee vee 0 -15
Vin in 0 DC 0

"""

for i, name in enumerate(opamps):
    cir_content += f"X{i} in 0 out{i} vcc vee 0 {name}\n"

cir_content += ".control\n"
cir_content += "op\n"
cir_content += "print " + " ".join([f"v(out{i})" for i in range(len(opamps))]) + "\n"
cir_content += ".endc\n.end\n"

with open("test_offset.cir", "w") as f:
    f.write(cir_content)

subprocess.run(["ngspice", "-b", "test_offset.cir"], check=True)
