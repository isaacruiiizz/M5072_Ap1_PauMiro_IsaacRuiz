# Projecte Clustering FEB - Sistemes d'Aprenentatge Automàtic

Aquest projecte té com a objectiu descobrir patrons ocults i tipologies de jugadors/equips en competicions de la FEB (Federació Espanyola de Bàsquet) utilitzant tècniques de **Machine Learning no supervisat**.

El projecte s'ha desenvolupat com a part del mòdul de Sistemes d'Aprenentatge Automàtic a l'Institut Sa Palomera (Curs 2025-2026).

## Equip
* **Pau Miró**
* **Isaac Ruiz**

---

## Objectius del Projecte
El flux de treball es divideix en tres fases principals:

1. **ETL i Model de Dades (30%)**: Extracció de dades des de MongoDB, neteja de valors nuls/outliers i creació de mètriques avançades (Feature Engineering) com OER, DER i percentatges de tir.
2. **Model de Machine Learning (40%)**: Implementació d'algorismes de clustering (**K-Means** obligatori, **DBSCAN** opcional) per segmentar jugadors segons el seu rendiment.
3. **Visualització i Conclusions (30%)**: Generació de gràfics (Heatmaps, Scatter plots, t-SNE) per interpretar els clústers des d'una perspectiva esportiva.

---

## Stack Tecnològic
* **Llenguatge**: Python 3.12+
* **Base de Dades**: MongoDB (driver `pymongo`).
* **Data Science**: Pandas, NumPy, Scikit-learn.
* **Visualització**: Matplotlib, Seaborn.