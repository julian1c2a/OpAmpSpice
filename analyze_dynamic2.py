import numpy as np
import subprocess
import os

opamps = [
    "SupOpAmp", "SupOpAmp_LM741", "SupOpAmp_TL081", "SupOpAmp_TL071", "SupOpAmp_LM358",
    "SupOpAmp_NE5532", "SupOpAmp_MCP601", "SupOpAmp_OP07", "SupOpAmp_OP27",
    "SupOpAmp_AD8628", "SupOpAmp_LT1028", "SupOpAmp_AD797", "SupOpAmp_OPA2134",
    "SupOpAmp_AD8009", "SupOpAmp_LMH6702", "SupOpAmp_THS3001", "SupOpAmp_L272",
    "SupOpAmp_OPA541", "SupOpAmp_LM3886", "SupOpAmp_LT1210"
]

cir_content = """* Dynamic Analysis of SupOpAmps
.include SupOpAmp.cir

Vcc vcc 0 15
Vee vee 0 -15
Vin in 0 DC 0 AC 1 pulse(-5 5 10u 10n 10n 40u 100u)

"""
for i, name in enumerate(opamps):
    cir_content += f"X{i} in 0 out{i} vcc vee 0 {name}\n"

cir_content += """
.control
* 1. DC Operating Point (Offset)
op
"""
cir_content += "wrdata offset_data.txt " + " ".join([f"v(out{i})" for i in range(len(opamps))]) + "\n"
cir_content += """
* 2. AC Analysis
ac dec 100 1 100Meg
"""
cir_content += "wrdata ac_data.txt " + " ".join([f"vdb(out{i}) vp(out{i})" for i in range(len(opamps))]) + "\n"
cir_content += """
* 3. Transient Analysis (Slew Rate)
* Ponemos SupOpAmps en modo seguidor (realimentacion total) para Slew Rate realista
"""
for i, name in enumerate(opamps):
    cir_content += f"X_tran{i} in out_tran{i} out_tran{i} vcc vee 0 {name}\n"

cir_content += """
tran 50n 60u
"""
cir_content += "wrdata tran_data.txt " + " ".join([f"v(out_tran{i})" for i in range(len(opamps))]) + "\n"
cir_content += """
.endc
.end
"""

with open("test_dyn2.cir", "w") as f:
    f.write(cir_content)

print("Running SPICE...")
subprocess.run(["ngspice", "-b", "test_dyn2.cir"], check=True)

# Parse DC offset
# format of offset_data.txt: x1 y1 x2 y2 ...
with open("offset_data.txt", "r") as f:
    lines = f.readlines()
    if len(lines) > 0:
        parts = lines[0].strip().split()
        offsets = [float(parts[i*2 + 1]) for i in range(len(opamps))]
    else:
        offsets = [0.0]*len(opamps)

# Parse AC
ac_data = np.loadtxt("ac_data.txt")
freqs = ac_data[:, 0]
results = []

for i in range(len(opamps)):
    col_mag = i*4 + 1
    col_ph = i*4 + 3
    mag = ac_data[:, col_mag]
    ph = ac_data[:, col_ph]
    
    dc_gain = mag[0]
    
    # 3dB Bandwidth
    idx_3db = np.where(mag <= dc_gain - 3)[0]
    fc = freqs[idx_3db[0]] if len(idx_3db) > 0 else np.nan
    
    gbw = fc * (10**(dc_gain/20))
    
    # Unity gain frequency and Phase Margin
    idx_0db = np.where(mag <= 0)[0]
    if len(idx_0db) > 0:
        fug = freqs[idx_0db[0]]
        pm = 180 + ph[idx_0db[0]]
    else:
        fug = np.nan
        pm = np.nan
        
    results.append({"dc_gain": dc_gain, "fc": fc, "gbw": gbw, "fug": fug, "pm": pm})

# Parse TRAN
tran_data = np.loadtxt("tran_data.txt")
times = tran_data[:, 0]
for i in range(len(opamps)):
    col = i*2 + 1
    v = tran_data[:, col]
    
    # find slew rate: max positive deriv
    dt = np.diff(times)
    dv = np.diff(v)
    valid = dt > 1e-12
    deriv = dv[valid] / dt[valid]
    
    sr = np.max(deriv) / 1e6 # V/us
    results[i]["sr"] = sr if sr > 0 else 0.0

# Generate Markdown
md = "## Análisis Dinámico de la Colección SupOpAmp (Av=200k)\n\n"
md += "Configuración: Etapas 1 y 3 como buffers (Av=1.414), Etapa 2 polo dominante masivo (Av=100k).\n\n"
md += "| Modelo | Offset de Salida (mV) | Ganancia DC (dB) | F. Corte (3dB) | GBW (Lazo Abierto) | Frec. Unidad (0dB) | Margen de Fase (Unidad) | Slew Rate (V/µs) |\n"
md += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"

for i, name in enumerate(opamps):
    r = results[i]
    off_mv = offsets[i] * 1000
    md += f"| {name.replace('SupOpAmp_', '')} | {off_mv:.2f} mV | {r['dc_gain']:.1f} dB | {r['fc']/1000:.2f} kHz | {r['gbw']/1e6:.2f} MHz | {r['fug']/1e6:.2f} MHz | {r['pm']:.1f}° | {r['sr']:.2f} V/µs |\n"

with open("report2.md", "w", encoding="utf-8") as f:
    f.write(md)
print("Report generated: report2.md")
