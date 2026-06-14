# TRABAJO EN NGSPICE

Mi intención en este proyecto es trabajar con simulaciones de circuitos electrónicos en ngspice. Fundamentalmente, realizar subcircuitos, conocer los distintos comandos para describir fuentes y fuentes dependientes, así como las distintas formas de realizar análisis.

## 1. Un circuito simple

Consistirá en una fuente de alimentación de voltage, una resistencia y un condensador. Los nodos serán `in` y `out`, además del nodo a tierra `gnd`.

La fuente estará entre los nodos `gnd` o `0` (el terminal negativo) y el nodo `in` (el terminal positivo). 

La resistencia irá del nodo `in` al `out`. 

El condensador irá del nodo `out` al nodo `gnd` o `0`.

```spice
* Circuito RC Simple
Vin in gnd DC 5
R1 in out 10k
C1 out gnd 10u IC=0

* Opcion necesaria para poder ver corrientes de resistencias y condensadores
.options savecurrents

* Bloque de control de ngspice para análisis
.control
    * 1. Análisis de punto de trabajo (Operating Point)
    op
    * Imprimir por pantalla los voltajes y corrientes en DC
    print all
    
    * 2. Análisis transitorio (paso, tiempo_final, tiempo_inicio, paso_subida, uic para usar el IC=0)
    * Vamos a simular hasta 100ms con pasos de 0.1ms, sin permitir que el paso de simulación sea menor a 0.5ms, guardando desde el instante 0ms.
    tran 0.1m 500m 0m 0.5m uic
    * Graficar el voltaje de entrada y el del condensador (salida)
    wrdata datos_rc.txt V(in) V(out) @R1[i]
.endc
.end
```

Esa es la descripción del circuito, además que está el bloque de control para análisis, en el que le pedimos que haga un análisis de punto de trabajo y un análisis transitorio.

El comando de simulación sería:
```bash
ngspice RC_simple.cir
```