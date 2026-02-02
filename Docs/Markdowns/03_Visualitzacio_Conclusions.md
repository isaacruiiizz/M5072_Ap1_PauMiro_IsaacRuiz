# Part 3: Visualització Avançada i Conclusions

## 1. Exploració Visual de l'Estructura de la Lliga
En aquesta fase final, utilitzem tècniques de reducció de dimensionalitat més avançades per confirmar que la divisió en 6 clústers és robusta.

### 1.1. Visualització t-SNE

![t-SNE](Imagenes/Part3/TSNE.png)

#### 1.1.1. Ànàlisi dels Resultats

L'algorisme **t-SNE** (*t-Distributed Stochastic Neighbor Embedding*) ens ofereix una visió molt més detallada que el PCA, ja que prioritza mantenir els "veïns propers" junts. L'anàlisi de la gràfica revela tres punts clau:

1. **Illes de Talent i Especialització:** S'observen agrupacions molt nítides i separades (illes) per als perfils més extrems. Per exemple, els **Tiradors purs (C0)** i els **Pivots defensius (C4)** formen clústers molt compactes als extrems de la visualització. Això confirma que el model ha detectat signatures estadístiques molt úniques que no es barregen amb la resta de la lliga.

2. **El "Nucli de Rotació" (C5):** El clúster de jugadors amb baixa participació apareix com una massa molt densa i centralitzada. Des d'un punt de vista de gestió de dades, això és un èxit: el model ha estat capaç d'identificar que, independentment de la seva posició teòrica, els jugadors amb pocs minuts es comporten de manera gairebé idèntica a nivell de dades.

3. **Zones de Transició i Rols Híbrids:** A diferència de les illes aïllades, els **Guards/bases (C3)** i els **Anotadors tot terreny (C2)** mostren una certa proximitat o "ponts" entre els seus punts. Com a entrenador, això té tot el sentit del món: reflecteix el bàsquet modern on la línia entre un base que anota i un escorta que genera joc és cada cop més difusa. El t-SNE és capaç de capturar aquesta continuïtat que el K-Means ha segmentat per necessitat operativa.

**Conclusió visual:** El fet que els clústers del K-Means apareguin com a taques de color homogènies i no barrejades en el mapa t-SNE, valida que el nombre de clústers ($k=6$) és l'òptim per capturar l'estructura real de la competició.

### 1.2. Comparativa: De les Dades en Brut als Resultats del Model

Per entendre el valor del model de Machine Learning, és necessari comparar l'estat inicial de les dades amb la segmentació final obtinguda.

#### 1.2.1. Les Dades de Partida: Un "Núvol" Indiferenciat

Abans del clustering, les dades de la FEB es presenten com un continu on és difícil traçar línies divisòries. Com s'observa a la imatge, si mirem la relació entre assistències i rebots, la majoria de jugadors s'acumulen en una zona central, barrejant posicions i estils de joc.

![Dades de Partida](Imagenes/Part3/DadesPartida.png)

#### 1.2.2. Els Resultats: Especialització i Rols Tàctics
Després d'aplicar el K-Means, el model és capaç d'"endreçar" aquest caos. A la imatge, veiem com els mateixos jugadors ara estan clarament agrupats:
* Els **Guards/bases (C3)** es desplacen cap a la dreta (més assistències).
* Els **Pivots defensius (C4)** i **Pivots oberts (C1)** es desplacen cap amunt (més rebots).
* Els **Anotadors (C2)** i **Tiradors (C0)** es mantenen en zones d'alt volum però amb ràtios d'assistència/rebot equilibrats segons la seva funció.

![Separació de rols](Imagenes/Part3/RebotsAsist.png)

#### 1.2.3. Perfil d'Anotació: Boxplot per Clúster
Un dels indicadors més clars de l'èxit del model és la distribució de punts. Com s'observa al gràfic de caixes, cada clúster té un "rang" d'anotació molt definit. El **C2 (Anotadors)** presenta la mediana més alta, mentre que el **C5 (Rotació)** queda clarament aïllat a la part baixa, confirmant que el model ha detectat correctament el pes ofensiu de cada jugador.

![Perfil d'Anotació](Imagenes/Part3/PerfilAnotacio.png)

### 1.3. Caracterització Multidimensional (Radar Chart)

Com a conclusió de l'anàlisi visual, el gràfic de radar ens permet validar la coherència esportiva dels clústers creats pel model K-Means. Aquesta visualització sintetitza les 5 dimensions clau del joc en una sola "signatura" per cada rol.

#### Conclusions del Perfilatge:
* **Validació de Rols:** El model ha separat amb èxit els perfils unidimensionals (especialistes en triple o rebot) dels jugadors versàtils.
* **Eficiència vs. Rol:** S'observa que el **Clúster 3** manté un OER alt tot i l'alt volum de joc, el que els defineix com els jugadors franquícia de la lliga.
* **Geometria del Joc:** La diferència de formes entre clústers confirma que la $k=6$ no és una divisió arbitrària, sinó que respon a necessitats tàctiques reals de la competició.

![Radar Final](Imagenes/Part3/Radar.png)

# 2. Conclusions Generals del Projecte

El present projecte de *clustering* aplicat a les lligues FEB ha permès transformar un dataset d'alt volum (més de 200.000 registres i un milió d'accions de tir) en una **eina d'intel·ligència esportiva** operativa. Més enllà de l'execució tècnica, s'han assolit els objectius tàctics inicials, permetent una comprensió de la competició basada en el comportament real i no en etiquetes nominals.

### 2.1. Eficàcia del Model i Validació Tècnica
L'elecció de **K-Means amb $k=6$** s'ha validat com la més robusta per a l'estructura de la lliga. 

* **Comparativa de Models:** Tot i explorar algorismes basats en densitat com el **DBSCAN**, la naturalesa contínua de les estadístiques de bàsquet —on els perfils sovint se solapen— ha fet que la segmentació per centroides del K-Means fos més útil per definir rols tàctics clars. 
* **Robustesa Visual:** La validació mitjançant **t-SNE** ha confirmat la cohesió dels grups, identificant "illes de talent" especialment definides en els extrems (tiradors purs i pivots defensius).

### 2.2. Descobriments Tàctics Clau
L'anàlisi ha revelat realitats que sovint queden ocultes en l'estadística tradicional:

* **L'evolució de les posicions clàssiques:** S'ha demostrat que jugadores amb la mateixa posició nominal (ex: Aler-Pivot) es divideixen en realitat entre "Pivots oberts" (C1) i "Anotadors tot terreny" (C2), amb funcions espacials radicalment oposades.
* **Especialització Negativa:** Els valors nuls en certes zones d'eficiència no s'han interpretat com a falta de qualitat, sinó com una **selecció de tir extrema** que defineix el rol (per exemple, el C0 ignorant la pintura per maximitzar l'*spacing*).
* **Identificació de la Rotació:** El model ha estat capaç d'aïllar el "soroll" de la banqueta (C5), permetent posar el focus de l'anàlisi en les jugadores que realment determinen el rendiment col·lectiu i l'OER.

### 2.3. Aplicació Pràctica per un club de futbol sala
Per a un cos tècnic de futbol sala, aquesta eina representa un avantatge competitiu en dos fronts clau:

1. **Scouting de Substitució:** Davant una possible baixa, el model permet trobar **"clons estadístics"** dins de la lliga que garantixin la continuïtat del rol tàctic necessari, minimitzant el risc en la incorporació de noves jugadores.
2. **Scouting de Rivals:** L'anàlisi de la densitat de clústers en les plantilles rivals permet preveure l'estil de joc de l'oponent (predomini del volum de triple vs. domini de pintura) i dissenyar ajustos defensius basats en evidències i no en percepcions subjectives.

> **Reflexió final:** Aquest flux de treball —des del processament inicial en Azure fins a la visualització avançada— demostra que la **Intel·ligència Artificial** és ja un component indispensable per a l'evolució tàctica i la gestió de talent en el bàsquet FEB actual.



