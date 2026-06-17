import numpy as np
import subprocess

# Ganancia total deseada
Av_total = 200000

# Configuraciones a probar
configs = [
    {"name": "Equilibrada (Av1=58.5, Av2=58.5, Av3=58.5)", "Av1": 58.48, "Av2": 58.48, "Av3": 58.48},
    {"name": "Polo Dominante en Etapa 1 (Av1=2000, Av2=10, Av3=10)", "Av1": 2000, "Av2": 10, "Av3": 10},
    {"name": "Polo Dominante Extremo (Av1=20000, Av2=3.16, Av3=3.16)", "Av1": 20000, "Av2": 3.16, "Av3": 3.16},
    {"name": "Polo Dominante en Etapa 3 (Av1=10, Av2=10, Av3=2000)", "Av1": 10, "Av2": 10, "Av3": 2000}
]

cir_content = """* Analisis de Margen de Fase
.include SupOpAmp.cir

Vcc vcc 0 15
Vee vee 0 -15
Vin in 0 AC 1

"""

for i, cfg in enumerate(configs):
    cir_content += f"X{i} in 0 out{i} vcc vee 0 SupOpAmp_LM741 Av1={cfg['Av1']} Av2={cfg['Av2']} Av3={cfg['Av3']}\n"

cir_content += """
.control
ac dec 100 1 100Meg
"""
cir_content += "wrdata pm_data.txt " + " ".join([f"vdb(out{i}) vp(out{i})" for i in range(len(configs))]) + "\n"
cir_content += """
.endc
.end
"""

with open("test_pm.cir", "w") as f:
    f.write(cir_content)

print("Ejecutando simulacion...")
subprocess.run(["ngspice", "-b", "test_pm.cir"], check=True)

data = np.loadtxt("pm_data.txt")
freqs = data[:, 0]

print("\n--- RESULTADOS DE ESTABILIDAD ---")
for i, cfg in enumerate(configs):
    col_mag = i * 4 + 1
    col_ph = i * 4 + 3
    mag = data[:, col_mag]
    phase = data[:, col_ph]
    
    # Buscar frecuencia de cruce por 0 dB (Fug)
    idx_0db = np.where(mag <= 0)[0]
    if len(idx_0db) > 0:
        fug = freqs[idx_0db[0]]
        pm = 180 + phase[idx_0db[0]]
    else:
        fug = np.nan
        pm = np.nan
        
    print(f"\nConfiguracion: {cfg['name']}")
    print(f"Ganancia DC (dB): {mag[0]:.2f} dB")
    print(f"Frecuencia Unidad (0dB): {fug/1e6:.3f} MHz" if not np.isnan(fug) else "No cruza 0dB")
    print(f"Margen de Fase (PM): {pm:.2f} grados" if not np.isnan(pm) else "N/A")
    
    if pm > 45:
        print(">> ESTABLE en lazo cerrado")
    elif pm > 0:
        print(">> MARGINALMENTE ESTABLE (Oscilara con ringing enorme)")
    else:
        print(">> INESTABLE (Oscilador asegurado)")
