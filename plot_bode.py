import numpy as np
import matplotlib.pyplot as plt
import os

opamps = [
    "SupOpAmp", "SupOpAmp_LM741", "SupOpAmp_TL081", "SupOpAmp_TL071", "SupOpAmp_LM358",
    "SupOpAmp_NE5532", "SupOpAmp_MCP601", "SupOpAmp_OP07", "SupOpAmp_OP27",
    "SupOpAmp_AD8628", "SupOpAmp_LT1028", "SupOpAmp_AD797", "SupOpAmp_OPA2134",
    "SupOpAmp_AD8009", "SupOpAmp_LMH6702", "SupOpAmp_THS3001", "SupOpAmp_L272",
    "SupOpAmp_OPA541", "SupOpAmp_LM3886", "SupOpAmp_LT1210"
]

# Seleccionamos un grupo representativo para no saturar la gráfica
selected_indices = [1, 2, 5, 8, 10, 13, 18] # LM741, TL081, NE5532, OP27, LT1028, AD8009, LM3886
selected_names = [opamps[i].replace("SupOpAmp_", "") for i in selected_indices]

# Cargar datos
data = np.loadtxt("ac_data.txt")
freqs = data[:, 0]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
fig.suptitle("Diagrama de Bode - SupOpAmps (Compensación Av=200k)", fontsize=14)

for i, idx in enumerate(selected_indices):
    col_mag = idx * 4 + 1
    col_ph = idx * 4 + 3
    mag = data[:, col_mag]
    ph = data[:, col_ph]
    
    ax1.semilogx(freqs, mag, label=selected_names[i])
    
    # Ajuste para visualizar bien la fase (evitar saltos feos si hay wrap)
    ph_rad = ph * np.pi / 180
    ph_unwrapped = np.unwrap(ph_rad) * 180 / np.pi
    ax2.semilogx(freqs, ph_unwrapped, label=selected_names[i])

ax1.set_ylabel("Magnitud (dB)")
ax1.grid(True, which="both", ls="--", alpha=0.5)
ax1.legend(loc='lower left')
ax1.axhline(0, color='black', lw=1.5, ls=':') # Línea de 0dB

ax2.set_ylabel("Fase (grados)")
ax2.set_xlabel("Frecuencia (Hz)")
ax2.grid(True, which="both", ls="--", alpha=0.5)
ax2.axhline(0, color='black', lw=1.5, ls=':') 

# Ajustar ejes para mejor visualización
ax1.set_ylim(-20, 115)
ax2.set_ylim(-360, 45)

plt.tight_layout()
plt.savefig("bode_plot.png", dpi=300)
print("Gráfica guardada como bode_plot.png")
