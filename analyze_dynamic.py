import numpy as np
import subprocess

opamps = [
    "SupOpAmp", "SupOpAmp_LM741", "SupOpAmp_TL081", "SupOpAmp_TL071", "SupOpAmp_LM358",
    "SupOpAmp_NE5532", "SupOpAmp_MCP601", "SupOpAmp_OP07", "SupOpAmp_OP27",
    "SupOpAmp_AD8628", "SupOpAmp_LT1028", "SupOpAmp_AD797", "SupOpAmp_OPA2134",
    "SupOpAmp_AD8009", "SupOpAmp_LMH6702", "SupOpAmp_THS3001", "SupOpAmp_L272",
    "SupOpAmp_OPA541", "SupOpAmp_LM3886", "SupOpAmp_LT1210"
]

# Increase the TRAN simulation time to 50us to catch slower SR
tran_cir = """* TRAN Test
.include SupOpAmp.cir
Vcc vcc 0 15
Vee vee 0 -15
Vin in 0 PULSE(-0.5 0.5 10n 1n 1n 100u 200u)
"""
for i, name in enumerate(opamps):
    tran_cir += f"X{i} in 0 out{i} vcc vee 0 {name}\n"
tran_cir += ".control\n"
tran_cir += "tran 10n 50u\n"
tran_cir += "wrdata tran_data.txt " + " ".join([f"v(out{i})" for i in range(len(opamps))]) + "\n"
tran_cir += ".endc\n.end\n"

with open("test_tran.cir", "w") as f:
    f.write(tran_cir)

print("Running TRAN analysis...")
subprocess.run(["ngspice", "-b", "test_tran.cir"], check=True)

print("Analyzing data...")
ac_data = np.loadtxt("ac_data.txt")
freqs = ac_data[:, 0]

tran_data = np.loadtxt("tran_data.txt")
times = tran_data[:, 0]

results = []

for i, name in enumerate(opamps):
    col_mag = i * 4 + 1
    col_ph = i * 4 + 3
    
    mag = ac_data[:, col_mag]
    phase = ac_data[:, col_ph]
    
    dc_gain_db = mag[0]
    dc_gain_lin = 10**(dc_gain_db/20)
    
    idx_fc = np.where(mag <= dc_gain_db - 3)[0]
    fc = freqs[idx_fc[0]] if len(idx_fc) > 0 else np.nan
    gbw = dc_gain_lin * fc if not np.isnan(fc) else np.nan
    
    # Phase unwrapping can be tricky. Let's just track absolute cumulative shift
    # from the first frequency point.
    ph_rad = phase * np.pi / 180
    ph_unwrapped = np.unwrap(ph_rad) * 180 / np.pi
    ph_shift = np.abs(ph_unwrapped - ph_unwrapped[0])
    
    idx_p2 = np.where(ph_shift >= 135)[0]
    fp2_approx = freqs[idx_p2[0]] if len(idx_p2) > 0 else np.nan

    idx_p3 = np.where(ph_shift >= 225)[0]
    fp3_approx = freqs[idx_p3[0]] if len(idx_p3) > 0 else np.nan

    col_tran = i * 2 + 1
    v_tran = tran_data[:, col_tran]
    
    # SR: max abs derivative
    dt = np.diff(times)
    dv = np.diff(v_tran)
    # Avoid dt=0
    valid = dt > 0
    if np.any(valid):
        sr_v_s = np.max(np.abs(dv[valid] / dt[valid]))
        sr_v_us = sr_v_s / 1e6
    else:
        sr_v_us = 0.0
    
    # Limit max SR reported to realistic bounds to avoid numeric glitches at t=0
    # Let's ignore the first few points where the pulse just hits
    # Wait, the pulse rises from 10n to 11n, so 1ns transition. 
    # An ideal opamp will try to follow.
    # Instead of global max, we can find the 10% to 90% rise/fall time, 
    # but the output swings from +Vsat to -Vsat.
    # Let's just bound the SR to say 100,000 V/us max to avoid inf
    if sr_v_us > 100000:
        sr_v_us = np.nan
    
    results.append({
        "name": name,
        "gain_db": dc_gain_db,
        "fc": fc,
        "gbw": gbw,
        "fp2": fp2_approx,
        "fp3": fp3_approx,
        "sr": sr_v_us
    })

md = "## Resultados del Análisis Dinámico del SupOpAmp\n\n"
md += "| Modelo | Ganancia DC (dB) | F. Corte (3dB) | Ancho de Banda Efec. (GBW) | Freq. Fase -135° (Aprox Polo 2) | Freq. Fase -225° (Aprox Polo 3) | Slew Rate Estimado (V/µs) |\n"
md += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"

def fmt_freq(f):
    if np.isnan(f): return "N/A"
    if f >= 1e9: return f"{f/1e9:.2f} GHz"
    if f >= 1e6: return f"{f/1e6:.2f} MHz"
    if f >= 1e3: return f"{f/1e3:.2f} kHz"
    return f"{f:.2f} Hz"

for r in results:
    md += f"| {r['name'].replace('SupOpAmp_', '')} | {r['gain_db']:.1f} dB | {fmt_freq(r['fc'])} | {fmt_freq(r['gbw'])} | {fmt_freq(r['fp2'])} | {fmt_freq(r['fp3'])} | {r['sr']:.2f} V/µs |\n"

with open("dynamic_report.md", "w", encoding="utf-8") as f:
    f.write(md)
