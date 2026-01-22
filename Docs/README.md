# 🏀 Projecte Clustering FEB - Sistemes d'Aprenentatge Automàtic

[cite_start]Aquest projecte té com a objectiu descobrir patrons ocults i tipologies de jugadors/equips en competicions de la FEB (Federació Espanyola de Bàsquet) utilitzant tècniques de **Machine Learning no supervisat**[cite: 11, 14].

[cite_start]El projecte s'ha desenvolupat com a part del mòdul de Sistemes d'Aprenentatge Automàtic a l'Institut Sa Palomera (Curs 2025-2026)[cite: 3, 4, 8].

## 👥 Equip
* **Isaac Ruiz**
* **Pau Miró**

---

## 🚀 Objectius del Projecte
El flux de treball es divideix en tres fases principals:

1.  [cite_start]**ETL i Model de Dades (30%)**: Extracció de dades des de MongoDB, neteja de valors nuls/outliers i creació de mètriques avançades (Feature Engineering) com OER, DER i percentatges de tir[cite: 41, 64].
2.  [cite_start]**Model de Machine Learning (40%)**: Implementació d'algorismes de clustering (**K-Means** obligatori, **DBSCAN** opcional) per segmentar jugadors segons el seu rendiment[cite: 83, 88].
3.  [cite_start]**Visualització i Conclusions (30%)**: Generació de gràfics (Heatmaps, Scatter plots, t-SNE) per interpretar els clústers des d'una perspectiva esportiva[cite: 116, 121, 123].

---

## 🛠️ Stack Tecnològic
* **Llenguatge**: Python 3.12+
* [cite_start]**Base de Dades**: MongoDB (driver `pymongo`)[cite: 13, 45].
* **Data Science**: Pandas, NumPy, Scikit-learn.
* **Visualització**: Matplotlib, Seaborn.

---

## ⚙️ Instal·lació i Configuració

### 1. Clonar el repositori
```bash
git clone [https://github.com/isaacruiiizz/M5072_Ap1_PauMiro_IsaacRuiz.git](https://github.com/isaacruiiizz/M5072_Ap1_PauMiro_IsaacRuiz.git)
cd M5072_Ap1_PauMiro_IsaacRuiz