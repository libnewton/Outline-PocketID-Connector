# Outline Pocket ID Connector

Heavily based on [Outline Authentik Connector](https://github.com/burritosoftware/Outline-Authentik-Connector).

Syncs groups between Pocket ID and Outline. Users will be added/removed from Outline groups depending on what Pocket ID groups they're in, on each sign in.

This was inspired by [this similar connector for Outline and Keycloak](https://gist.github.com/Frando/aa561ca7e6c72ab64b5d17df911c0b1f)!

## How It Works
Outline groups that are named the same as Pocket ID groups will be linked together. Users who are in a Pocket ID group but not in a linked Outline group will be added to the Outline group. Conversely, if a user is not in a linked Pocket ID group, but is in an Outline group, they will be removed from that group.

This connector listens for `users.signin` webhook events from Outline. Once a user signs into Outline, this connector will check for matching groups, and add/remove the user to those groups accordingly.

## Features

### Group Synchronization
When a user signs in to Outline, the connector automatically syncs their group memberships between Pocket ID and Outline.

### Auto-Creation of Groups (optional)
When the `AUTO_CREATE_GROUPS` environment variable is set to `True`, the connector will automatically create Outline groups that:
- Exist in Pocket ID but don't yet exist in Outline
- The signing-in user is a member of

This on-demand approach creates groups only when needed rather than creating all groups at once, optimizing resources and keeping your Outline workspace clean.

### Group Filtering (optional)
The `SYNC_GROUP_REGEX` environment variable allows you to filter which groups should be synced between Pocket ID and Outline using a regular expression (case-insensitive). Only groups matching the pattern will be considered for synchronization from both Pocket ID and Outline, letting you selectively sync specific groups while ignoring others. If not set, all groups will be synced.

**Examples:**
- `^wiki-.*` - Only sync groups starting with "wiki-" (e.g., wiki-admins, wiki-editors)
- `.*-outline$` - Only sync groups ending with "-outline" (e.g., dev-outline, sales-outline)
- `^(admins|editors|viewers)$` - Only sync groups named exactly "admins", "editors", or "viewers"

## Requirements
- Outline API key
- Pocket ID API key
- Reverse proxy to apply HTTPS
- Python 3.11.1 or higher (not required if using Docker)
- Docker and Docker Compose (optional)

## Outline Setup
1. Login to your Outline instance. Click your profile in the bottom left, then go to **Preferences**.
2. On the sidebar, click **API**. At the top right, select **New API Key...**, and give it a name like `Outline Pocket ID Connector`.
3. Save the API key somewhere safe to fill in later.
4. On the sidebar, click **Webhooks**. At the top right, select **New webhook...**, and give it a name like `Outline Pocket ID Connector`. Copy the signing secret and save it somewhere safe to fill in later.
5. Enter in the URL of a subdomain you plan to host the connector on, and **make sure it ends in `/sync`. This is important.** Then, tick the box for **users.signin**, and then scroll all the way down and click **Create**.

## Pocket ID Setup
1. Login to your Pocket ID instance as an administrator. Navigate to **Settings -> Admin -> API Keys**.
2. Click **Add API Key**, give it a name like `Outline Connector`, set an expiration date if desired, and provide a description.
3. Click **Generate API Key** and copy the generated key. Make sure to save it somewhere safe, as it won't be displayed again.

Now, choose whether to setup the connector [with Docker](#docker-setup) or [manually](#manual-setup).

## Docker Setup
The connector can be deployed with Docker Compose for quick and easy setup.
1. [Grab the `docker-compose.yml` file here](./docker-compose.yml), as well as [the `.env.example` file here](./.env.example).
2. Change `.env.example` to `.env`, and fill it in with your Pocket ID and Outline configuration.
3. Start the connector with `docker compose up -d`. By default, the connector will be exposed on port `8430`.
4. Use a reverse proxy to proxy the connector to a subdomain with HTTPS.

## Manual Setup
1. Create and activate a virtual environment.
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install requirements.
```sh
pip install -r requirements.txt
```

3. Copy the environment configuration, and fill it in with your Pocket ID and Outline configuration.
```sh
cp .env.example .env
nano .env
```

4. Start the connector.
```sh
fastapi run connect.py --port 8430
```
5. Use a reverse proxy to proxy the connector to a subdomain with HTTPS.

**Note:** Always activate the virtual environment (`source venv/bin/activate`) before running the connector or installing new dependencies.