import numpy as np
import subprocess

configs = [
    {"name": "Equilibrada (Av1=58.5, Av2=58.5, Av3=58.5)", "Av1": 58.48, "Av2": 58.48, "Av3": 58.48},
    {"name": "Polo Dominante en Etapa 1 (Av1=2000, Av2=10, Av3=10)", "Av1": 2000, "Av2": 10, "Av3": 10},
    {"name": "Polo Dominante Extremo (Av1=20000, Av2=3.16, Av3=3.16)", "Av1": 20000, "Av2": 3.16, "Av3": 3.16},
    {"name": "Polo Dominante en Etapa 3 (Av1=10, Av2=10, Av3=2000)", "Av1": 10, "Av2": 10, "Av3": 2000}
]

data = np.loadtxt("pm_data.txt")
freqs = data[:, 0]

print("\n--- DETALLES DE FASE ---")
for i, cfg in enumerate(configs):
    col_mag = i * 4 + 1
    col_ph = i * 4 + 3
    mag = data[:, col_mag]
    phase = data[:, col_ph]
    
    idx_0db = np.where(mag <= 0)[0]
    if len(idx_0db) > 0:
        idx = idx_0db[0]
        fug = freqs[idx]
        ph_0db = phase[idx]
        
        # SupOpAmp es inversor, arranca en 180 (o -180). 
        # Si arranca en 180, la inestabilidad ocurre cuando la fase cae a 0 (180 - 180 de desfase interno).
        # Por tanto, el Margen de Fase para un inversor es la distancia entre la fase en 0dB y 0 grados.
        # Si la fase empieza en 180 y cae, PM = ph_0db. Si empezó en -180 y sube (o cae a -360), ajustamos.
        ph_dc = phase[0]
        
        # Desfase total acumulado
        ph_rad = phase * np.pi / 180
        ph_unwrapped = np.unwrap(ph_rad) * 180 / np.pi
        total_shift = np.abs(ph_unwrapped[idx] - ph_unwrapped[0])
        
        # Margen de fase: 180 - total_shift
        pm = 180 - total_shift
        
    print(f"\nConfiguracion: {cfg['name']}")
    print(f"Fase DC: {ph_dc:.1f} grados")
    print(f"Fase en 0dB: {ph_0db:.1f} grados")
    print(f"Desfase acumulado hasta 0dB: {total_shift:.1f} grados")
    print(f"Margen de Fase REAL: {pm:.2f} grados")
