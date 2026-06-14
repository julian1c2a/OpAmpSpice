# TRABAJO EN NGSPICE

Mi intención en este proyecto es trabajar con simulaciones de circuitos electrónicos en ngspice. Fundamentalmente, realizar subcircuitos, conocer los distintos comandos para describir fuentes y fuentes dependientes, así como las distintas formas de realizar análisis.

## 1. Un circuito simple

Consistirá en una fuente de alimentación de voltage, una resistencia y un condensador. Los nodos serán `in` y `out`, además del nodo a tierra `gnd`.

La fuente estará entre los nodos `gnd` o `0` (el terminal negativo) y el nodo `in` (el terminal positivo). 

La resistencia irá del nodo `in` al `out`. 

El condensador irá del nodo `out` al nodo `gnd` o `0`.

```spice
Vin gnd in DC 5
R1 in out 10k
C1 out gnd 10u
.end
```
