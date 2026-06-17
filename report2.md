## Análisis Dinámico de la Colección SupOpAmp (Av=200k)

Configuración: Etapas 1 y 3 como buffers (Av=1.414), Etapa 2 polo dominante masivo (Av=100k).

| Modelo | Offset de Salida (mV) | Ganancia DC (dB) | F. Corte (3dB) | GBW (Lazo Abierto) | Frec. Unidad (0dB) | Margen de Fase (Unidad) | Slew Rate (V/µs) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| SupOpAmp | -2.41 mV | 99.9 dB | 0.02 kHz | 1.97 MHz | 0.78 MHz | 181.8° | 0.00 V/µs |
| LM741 | -2.41 mV | 102.4 dB | 0.02 kHz | 2.00 MHz | 0.78 MHz | 181.5° | 0.50 V/µs |
| TL081 | -7.23 mV | 102.4 dB | 0.04 kHz | 5.91 MHz | 2.34 MHz | 181.6° | 12.99 V/µs |
| TL071 | -7.23 mV | 102.4 dB | 0.04 kHz | 5.91 MHz | 2.34 MHz | 181.6° | 12.99 V/µs |
| LM358 | -4.79 mV | 99.7 dB | 0.02 kHz | 1.89 MHz | 0.76 MHz | 181.8° | 0.00 V/µs |
| NE5532 | -1.20 mV | 99.9 dB | 0.20 kHz | 19.75 MHz | 7.76 MHz | 181.8° | 0.00 V/µs |
| MCP601 | -4.75 mV | 84.7 dB | 0.31 kHz | 5.32 MHz | 2.14 MHz | 181.7° | 0.00 V/µs |
| OP07 | -0.07 mV | 104.3 dB | 0.01 kHz | 1.22 MHz | 0.47 MHz | 181.8° | 0.00 V/µs |
| OP27 | -0.06 mV | 105.5 dB | 0.09 kHz | 15.94 MHz | 6.31 MHz | 181.7° | 0.00 V/µs |
| AD8628 | -0.00 mV | 105.7 dB | 0.03 kHz | 4.97 MHz | 1.95 MHz | 181.8° | 0.00 V/µs |
| LT1028 | -0.05 mV | 105.9 dB | 0.76 kHz | 149.56 MHz | 58.88 MHz | 181.8° | 11.05 V/µs |
| AD797 | -0.10 mV | 105.2 dB | 1.20 kHz | 218.39 MHz | 87.10 MHz | 181.8° | 20.07 V/µs |
| OPA2134 | -1.21 mV | 105.2 dB | 0.09 kHz | 16.20 MHz | 6.31 MHz | 181.8° | 20.00 V/µs |
| AD8009 | -4.83 mV | 75.3 dB | 346.74 kHz | 2010.93 MHz | nan MHz | nan° | 2700.75 V/µs |
| LMH6702 | -2.41 mV | 79.5 dB | 363.08 kHz | 3444.66 MHz | nan MHz | nan° | 3078.92 V/µs |
| THS3001 | -2.41 mV | 85.2 dB | 46.77 kHz | 848.38 MHz | nan MHz | nan° | 15.30 V/µs |
| L272 | -24.13 mV | 96.4 dB | 0.01 kHz | 0.60 MHz | 0.22 MHz | 182.2° | 0.00 V/µs |
| OPA541 | -2.41 mV | 96.5 dB | 0.05 kHz | 3.26 MHz | 1.26 MHz | 181.7° | 0.00 V/µs |
| LM3886 | -2.41 mV | 100.0 dB | 0.16 kHz | 16.22 MHz | 6.31 MHz | 182.0° | 19.00 V/µs |
| LT1210 | -7.24 mV | 85.2 dB | 3.89 kHz | 70.57 MHz | 26.92 MHz | 182.1° | 211.32 V/µs |
