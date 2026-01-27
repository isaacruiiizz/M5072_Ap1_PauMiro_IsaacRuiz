# Part 1: ETL i Model de Dades

## Introducció i Objectius
En aquesta fase inicial, l'objectiu és transformar les dades "crues" de MongoDB en un dataset estructurat i net, preparat per a l'aprenentatge automàtic. Hem realitzat un procés ETL (Extract, Transform, Load) complet, integrant tecnologies de contenidorització i emmagatzematge al núvol.

## 0. Desplegament de la Infraestructura (Docker)
Per garantir la reproductibilitat de l'entorn i l'aïllament del servei de base de dades, hem implementat una arquitectura contenidoritzada utilitzant **Docker Compose**.

S'ha configurat el servei `mongodb` al fitxer `docker-compose.yaml`, definint:
* **Imatge:** `mongo:latest` per disposar de l'última versió estable.
* **Persistència:** Configuració de **Volums** (`mongo_data`) per assegurar que les dades sobrevisquin al reinici del contenidor.
* **Mapeig de Ports:** Exposició del port `27017` per permetre la connexió des del nostre entorn de desenvolupament local (Python).

## 1. Ingesta i Restauració de Dades
El procés de càrrega inicial de dades (Data Seeding) s'ha realitzat a partir d'un arxiu binari `.archive`. Aquest procés consta de dues fases crítiques:

**Fase A: Transferència al Contenidor**
Mitjançant la comanda `docker cp`, hem transferit l'arxiu de còpia de seguretat des del sistema host fins al directori temporal (`/tmp`) dins del contenidor en execució.

![alt text](Imagenes/Part1/CopiaBackupDocker.png)

**Fase B: Execució del Mongorestore**
Un cop l'arxiu és accessible pel contenidor, hem executat la utilitat `mongorestore` per reconstruir les col·leccions (`FEB3_players_statistics`, `FEB3_players_shots`, etc.) dins la nostra instància local.

![alt text](Imagenes/Part1/RestauracioDades.png)

## 2. Configuració de l'Entorn de Desenvolupament
Per interactuar programàticament amb la base de dades, hem establert un entorn de desenvolupament en Python basat en la gestió estricta de dependències i la modularitat del codi.

**Gestió de Dependències**
S'ha utilitzat un fitxer `requirements.txt` per definir i instal·lar les llibreries necessàries (`pymongo`, `pandas`, `azure-storage-blob`, `python-dotenv`), assegurant que tots els membres de l'equip treballin amb les mateixes versions.

![alt text](Imagenes/Part1/InstalacioLlibreries.png)

**Mòdul de Connexió (Modularització)**
Per evitar la duplicació de codi i millorar la seguretat, hem encapsulat la lògica de connexió en el mòdul `connMongo.py`. Aquest script implementa el patró **Singleton** per gestionar la connexió i carrega dinàmicament les variables d'entorn (IP, Port) segons si s'executa en local o via VPN (Tailscale).

A continuació, es mostra la validació de la connexió recuperant els primers registres de la col·lecció d'estadístiques:

![alt text](Imagenes/Part1/ProvaConnexio.png)

## 3. Definició de l'Arquitectura de Dades

Per tal d'estructurar el flux de dades de manera professional i escalable, hem decidit implementar una **Arquitectura Medallion (Multi-hop Architecture)** utilitzant **Azure Blob Storage** com a Data Lake.

### 3.1. Per què Azure Blob Storage?
Hem decidit externalitzar l'emmagatzematge al núvol (Cloud) per diversos motius tècnics:

* **Simulació d'entorn Big Data real:** En la indústria, les dades no es guarden en local, sinó en Data Lakes distribuïts.
* **Desacoblament (Decoupling):** Separem la *computació* (el nostre script Python local) de l'*emmagatzematge* (Azure). Això permet que tant l'Isaac com el Pau puguin accedir a les mateixes dades processades sense haver d'enviar-se fitxers CSV manualment.
* **Traçabilitat:** Podem mantenir l'històric de les dades originals encara que ens equivoquem en el processament posterior.

### 3.2. Estructura de Capes (The Medallion Architecture)

El nostre pipeline ETL mou les dades a través de tres contenidors al núvol:

#### Capa BRONZE (Raw Zone)
* **Descripció:** És la "zona d'aterratge". Conté una còpia exacta de les dades tal com s'han extret de MongoDB, sense cap modificació.
* **Format:** Fitxer `.csv` amb totes les columnes originals.
* **Funció:** Actua com a còpia de seguretat immutable. Si cometem un error en la neteja, sempre podem tornar a aquesta capa per regenerar el dataset sense haver de tornar a consultar la base de dades.
* **Contingut:** Totes les temporades i competicions (FEB3/EBA) amb registres "bruts" (inclosos jugadors amb 0 minuts, noms duplicats o dades errònies).

#### Capa SILVER (Clean Zone)
* **Descripció:** Dades netes, filtrades i tipificades.
* **Transformacions aplicades:**
    * **Filtratge de qualitat:** Eliminació de jugadors amb menys de X minuts o partits jugats (per evitar distorsions estadístiques per *small sample size*).
    * **Neteja d'estructures:** Eliminació de columnes innecessàries (IDs interns de Mongo) i estandardització de noms d'equips i temporades.
    * **Gestió de Nuls:** Imputació de valors `0` on hi ha `NaN` en estadístiques de comptatge.
* **Contingut:** Una taula estructurada on cada fila és un jugador/temporada vàlid per a l'anàlisi.

#### Capa GOLD (Business / ML Zone)
* **Descripció:** Dades enriquides i llestes per alimentar el model de Machine Learning.
* **Feature Engineering:** En aquesta capa és on apliquem el coneixement de domini (bàsquet) per crear noves mètriques que no existien a l'origen:
    * **OER (Offensive Efficiency Rating):** Punts per possessió.
    * **Possessions Estimades:** Fórmula avançada per calcular el volum de joc real.
    * **% Volum de Tirs:** Distribució de tirs (Triples vs Tirs de 2).
* **Contingut final:** Aquest és el dataset (`final_dataset.csv`) que llegirà l'algorisme **K-Means** a la Part 2 del projecte.

### 3.3. Esquema del Pipeline

```mermaid
graph LR
    A[("MongoDB (Origen)")] -->|Extract| B(Python Script)
    B -->|Load Raw| C[("Azure Blob: BRONZE")]
    C -->|Clean & Filter| D[("Azure Blob: SILVER")]
    D -->|Feature Engineering| E[("Azure Blob: GOLD")]
    E -->|Input| F{Model K-Means}
    
    style C fill:#cd7f32,stroke:#333,stroke-width:2px,color:white
    style D fill:#c0c0c0,stroke:#333,stroke-width:2px,color:black
    style E fill:#ffd700,stroke:#333,stroke-width:2px,color:black