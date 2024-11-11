# **DKC-BRO**

## Inleiding
Deze DataKwaliteitsControle-BasisRegistratieOndergrond (DKC-BRO) applicatie controleert brondocumenten op geldende kwaliteitsregels. Dit wordt gedaan middels de poller die de brondocumenten ophaalt van het Bronhouderportaal. De applicatie bestaat uit een frontend, backend en database.

## Vereisten
Zorg ervoor dat je de volgende tools hebt geïnstalleerd:

- [Docker](https://www.docker.com/) - Docker is nodig om de database te draaien in een container.
- [Node.js](https://nodejs.org/) - De versie wordt gespecificeerd in `frontend/.nvmrc`. Het wordt aanbevolen om [Node Version Manager (nvm)](https://github.com/nvm-sh/nvm) te gebruiken om gemakkelijk tussen Node-versies te schakelen. Je kunt de juiste Node-versie activeren met `nvm use`.
- [Python](https://www.python.org/) - De versie wordt gespecificeerd in `backend/.python-version`. Het wordt aanbevolen om [pyenv](https://github.com/pyenv/pyenv) te gebruiken om tussen Python-versies te schakelen.
- [Make] (https://www.gnu.org/software/make/) - Make is nodig om de handige commando's uit te voeren.

## Installatie
Zorg ervoor dat je in de root van het project zit.

### Omgevingsvariabelen
De omgevingsvariabelen worden gelezen uit een `.env`-bestand in zowel src/backend als src/frontend. Hierin staan de gegevens zoals de database- en API-gegevens. Let op, voor de poller naar het bronhoudersportaal moet je een gebruikersnaam en token hebben.

0. Maak een kopie van het `.env.example`-bestand in zowel src/backend als src/frontend en hernoem het naar `.env`:
   ```
   cd src/backend && cp .env.example .env && cd ../frontend && cp .env.example .env
   ```
### Backend (met pip)
#### Windows
1. Open een terminal en navigeer naar de backend-directory met:
   ```
   cd src/backend
   ```
2. Maak een nieuwe virtuele omgeving aan genaamd "env" dmv virtualenv:
   ```
   python3 -m virtualenv env
   ```
   
   Indien je conda gebruikt:
   ```
   conda create -n env python=3.10
   ```
3. Activeer de virtuele omgeving:
   ```
   env/Scripts/activate
   ```

   Indien je conda gebruikt:
   ```
   conda activate env
   ```
4. Installeer de vereiste Python-pakketten:
   ```
   pip install -r app/requirements.txt
   ```

#### Linux
1. Open een terminal en navigeer naar de backend-directory met:
   ```
   cd src/backend
   ```
2. Maak een nieuwe virtuele omgeving aan genaamd "env" met Python 3.10:
   ```
   python3.10 -m virtualenv env
   ```
3. Activeer de virtuele omgeving:
   ```
   source env/bin/activate
   ```
4. Installeer de vereiste Python-pakketten:
   ```
   python3 -m pip install -r app/requirements.txt
   ```

### Frontend
1. Open een terminal en navigeer naar de frontend-directory met:
   ```
   cd src/frontend
   ```
2. Installeer de vereiste Node.js-pakketten:
   ```
   npm install
   ```

## Uitvoeren
Voor gemak zijn er enkele handige commando's opgenomen in een `Makefile`. Deze commando's kunnen worden uitgevoerd met `make` gevolgd door de naam van het commando. Zorg ervoor dat je in de root van het project zit.

### Database opzetten in een container
0. Initialiseer de database in een container via Docker:
   ```
   make db_dev
   ```

### Zonder containers
1. Voer database-migraties uit:
   ```
   make migration_head
   ```
   Open de database client in je browser op `http://localhost:8091`.
2. Start de backend-server in development-modus:
   ```
   make backend_dev_dkc
   ```
   Open de api-docs in je browser op `http://localhost:8000/docs`.
3. Start de frontend-server in een nieuwe terminal:
   ```
   make frontend_dev
   ```
   Open de applicatie in je browser op `http://localhost:8080`.
4. Start de backend-poller in een nieuwe terminal:
   ```
   make backend_dev_poller
   ```

### Met containers
1. Start de volledige applicatie (backend, frontend en database) in Docker-containers:
   ```
   make dkc_bro_app
   ```
   De frontend is nu beschikbaar op `http://localhost:8080`.
   De backend swagger docs is nu beschikbaar op `http://localhost:8000/docs`.
   De DbGate client is nu beschikbaar op `http://localhost:8091`.

### Overige
- Reset database en start DbGate client opnieuw op:
   ```
   make dev_db_reset
   ```
- Code formatteren en linting uitvoeren
   ```
   make type_fix
   ```