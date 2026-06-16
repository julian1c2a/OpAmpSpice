import numpy as np
import matplotlib.pyplot as plt
import subprocess  # <--- IMPORTANTE AÑADIR ESTO

# 1. Ejecutar ngspice en modo batch (-b) para que no abra su propia consola
print("Ejecutando simulación en ngspice...")
subprocess.run(["ngspice", "-b", "RC_simple.cir"], check=True)
print("Simulación completada. Generando gráfica...")

# 2. Cargar los datos (el resto del código sigue igual)
datos = np.loadtxt('datos_rc.txt')

# Extraer las columnas (ngspice repite el tiempo por cada variable)
# Col 0, 2, 4 son tiempo. Col 1 es V(in), Col 3 es V(out), Col 5 es I(R1)
tiempo = datos[:, 0]
v_in = datos[:, 1]
v_out = datos[:, 3]
i_r1 = datos[:, 5]  # ¡Aquí está la intensidad!

# Crear la figura y el eje principal para los voltajes
fig, ax1 = plt.subplots()

ax1.plot(tiempo, v_in, label='V(in)', color='blue')
ax1.plot(tiempo, v_out, label='V(out)', color='green')
ax1.set_xlabel('Tiempo (s)')
ax1.set_ylabel('Voltaje (V)', color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.grid(True)

# Crear un segundo eje Y compartiendo el mismo eje X
ax2 = ax1.twinx()  
# Pintar la intensidad en este segundo eje multiplicando por 1000 para verla en mA
ax2.plot(tiempo, i_r1 * 1000, label='I(R1)', color='purple', linestyle=':')
ax2.set_ylabel('Intensidad (mA)', color='purple')
ax2.tick_params(axis='y', labelcolor='purple')

# Dibujar la línea vertical en 1 Tau (R=10k, C=10uF -> Tau = 100ms = 0.1s)
tau = 0.1
ax1.axvline(x=tau, color='red', linestyle='--')
ax1.text(tau, 1, ' 1 $\\tau$', color='red')

ax1.axvline(x=2*tau, color='orange', linestyle='--')
ax1.text(2*tau, 1, ' 2 $\\tau$', color='orange')

ax1.axvline(x=3*tau, color='yellow', linestyle='--')
ax1.text(3*tau, 1, ' 3 $\\tau$', color='yellow')

ax1.axvline(x=4*tau, color='pink', linestyle='--')
ax1.text(4*tau, 1, ' 4 $\\tau$', color='pink')

ax1.axvline(x=5*tau, color='green', linestyle='--')
ax1.text(5*tau, 1, ' 5 $\\tau$', color='green')

# Juntar las leyendas de ambos ejes
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='center right')

plt.title("Circuito RC - Voltaje e Intensidad")
plt.show() # O plt.savefig('grafica.png') si te daba problemas
