# BasicApi For Reconcept

Dit is een basis api voor een twitter achtige applicatie. Deze api beheerd de data van gebruikers, hun berichten en de tags gerelateerd aan deze berichten. Het gebruikt een SQLite database om locaal te runnen. Ik heb zelf postman gebruikt om de routes te testen maar andere software testing tools zouden ook moeten kunnen werken.

## Installatie

1. Installeer de vereiste pakketten met behulp van `pip`. Voer het volgende commando uit in je terminal:

    ```bash
    pip install -r requirements.txt
    ```

2. Voer de applicatie uit:

    ```bash
    python api.py
    ```

De applicatie wordt standaard uitgevoerd op http://localhost:5000/

## Endpoints

### populate database
- **vult de database met wat standaard data:**
  - **URL:** `/api/db_populate`
  - **Methode:** GET
  - **Voorbeeld:** http://localhost:5000/api/db_populate

### Gebruikers
- **Gebruiker ophalen op basis van ID:**
  - **URL:** `/get-user/<user_id>`
  - **Methode:** GET
  - **Voorbeeld:** http://localhost:5000/get-user/1

- **Haalt alle gebruikers op:**
  - **URL:** `/get-users`
  - **Methode:** GET
  - **Voorbeeld:** http://localhost:5000/get-users

- **Maakt een gebruiker aan:**
  - **URL:** `/create-user`
  - **Methode:** POST
  - **Voorbeeld body:** 
    ```json
    {
        "name": "gebruikersnaam",
        "email": "voorbeeld@email.com"
    }
    ```

- **Verwijderd een gebruiker:**
  - **URL:** `/delete-user/<user_id>`
  - **Methode:** DELETE
  - **Voorbeeld:** http://localhost:5000//delete-user/1

- **Update een gebruiker:**
  - **URL:** `/update-user/<user_id>`
  - **Methode:** PUT
  - **Voorbeeld body:** 
    ```json
    {
        "name": "updatednaam",
        "email": "updated@email.com"
    }
    ```

### messages

- **Message ophalen op basis van gebruiker ID:**
  - **URL:** `/messages/<user_id>`
  - **Methode:** GET
  - **Voorbeeld:** http://localhost:5000/messages/1

- **Alle messages ophalen:**
  - **URL:** `/messages`
  - **Methode:** GET
  - **Voorbeeld:** http://localhost:5000/messages

- **Maakt een message aan gebaseert op userId:**
  - **URL:** `/create-message`
  - **Methode:** POST
  - **Voorbeeld body:** 
    ```json
    {
        "message": "test message",
        "userId": "1"
    }
    ```

### tags

- **Alle tags ophalen:**
  - **URL:** `/tags`
  - **Methode:** GET
  - **Voorbeeld:** http://localhost:5000/tags

- **Alle tags en message combinaties ophalen:**
  - **URL:** `/tagMessage`
  - **Methode:** GET
  - **Voorbeeld:** http://localhost:5000/tagMessage

- **Alle messages ophalen met een bepaalde tag:**
  - **URL:** `/tags/<tag_name>`
  - **Methode:** GET
  - **Voorbeeld:** http://localhost:5000/tag1

- **Voegt tags toe aan een message:**
  - **URL:** `/tags/<message_id>`
  - **Methode:** POST
  - **Voorbeeld body:** 
    ```json
    {
        "tags": ["tag1", "test tag"]
    }
    ```

- **Verwijderd tags van een bericht:**
  - **URL:** `/tags/<message_id>`
  - **Methode:** DELETE
  - **Voorbeeld body:** 
    ```json
    {
        "tags": ["tag1"]
    }
    ```

