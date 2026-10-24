# Métricas (estándares de la industria aplicados a MDQ)

> Implementación y fórmulas finales: [`07_bd_y_metricas.md`](07_bd_y_metricas.md).

P1 = obligatoria para el finde. P2 = si hay tiempo/datos.

## Volumen

| Métrica | Definición | Fuente | P |
|---|---|---|---|
| Movimientos totales | aterrizajes + despegues en MDQ (todas las clases) | ANAC | P1 |
| Movimientos comerciales (ATM) | movimientos con clase regular + no regular | ANAC | P1 |
| Pasajeros totales | Σ pasajeros de movimientos en MDQ (embarcados + desembarcados, estándar ACI) | ANAC | P1 |
| Pasajeros por movimiento comercial | pax / ATM | ANAC | P1 |
| Variación interanual (YoY) | (x_t / x_{t−12}) − 1, solo meses definitivos | ANAC | P1 |
| CAGR | (x_fin / x_ini)^(1/n) − 1 | ANAC | P1 |
| Recuperación post-COVID | x_año / x_2019 | ANAC | P1 |

## Oferta y eficiencia

| Métrica | Definición | Fuente | P |
|---|---|---|---|
| Asientos ofrecidos | Σ asientos | Yvera | P1 |
| Load factor | pasajeros / asientos (misma fuente) | Yvera | P1 |
| Asientos por vuelo | asientos / vuelos | Yvera | P2 |
| Frecuencia semanal por ruta | vuelos ruta-mes / semanas del mes | ANAC/Yvera | P2 |

## Estacionalidad (el problema central de MDQ)

| Métrica | Definición | P |
|---|---|---|
| Índice estacional mensual | pax_mes / promedio mensual del año | P1 |
| Ratio pico/valle | máx mensual / mín mensual del año | P1 |
| Share de temporada alta | pax dic–mar / pax año | P1 |
| Coeficiente de variación mensual | desvío / media de pax mensuales | P2 |

## Estructura de mercado

| Métrica | Definición | P |
|---|---|---|
| Aerolíneas activas | aerolíneas con ≥ 1 ATM en el año | P1 |
| Share por aerolínea | pax aerolínea / pax total | P1 |
| HHI | Σ share² × 10.000 (> 2.500 = muy concentrado) | P1 |
| Destinos directos | origen_destino distintos con ATM regular | P1 |
| Share internacional | pax internacional / pax total | P1 |

## Tipo de aviación / flota

| Métrica | Definición | P |
|---|---|---|
| Mix por clase de vuelo | % movimientos regular / no regular / privado / escuela / oficial | P1 |
| Mix por categoría de aeronave | % movimientos jet narrowbody / jet regional / turbohélice / aviación general / helicóptero | P1 |
| Top aeronaves | ranking por movimientos | P1 |
| Hora pico | movimientos por hora local (p95 de movimientos/hora) | P2 |

## Benchmark (pares sugeridos — confirmar)

Bariloche (BRC/SAZS), Neuquén (NQN/SAZN), Bahía Blanca (BHI/SAZB), Mendoza (MDZ/SAME),
Salta (SLA/SASA). Criterio: destinos turísticos o regionales no-hub de escala similar.
Comparar: pax anual, CAGR, ratio pico/valle, HHI, destinos directos, pax/ATM.
