import httpx
import logging
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
logging.basicConfig(level=logging.INFO)

pocket_id_url = os.getenv('POCKET_ID_URL')
pocket_id_api_key = os.getenv('POCKET_ID_API_KEY')

async def main():
    if not pocket_id_url or not pocket_id_api_key:
        print("POCKET_ID_URL or POCKET_ID_API_KEY is not set.")
        return
        
    api_url = f"{pocket_id_url}/api/users"
    headers = {
        "X-API-KEY": pocket_id_api_key,
        "Accept": "application/json"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            if "data" not in data or not data["data"]:
                print("No users found.")
                return
                
            for user in data["data"]:
                email = user.get("email")
                groups = [g.get("name") for g in user.get("userGroups", [])]
                print(f"User {email} is in Pocket ID groups: {groups}")
                
    except Exception as e:
        print(f"Error fetching users: {e}")

if __name__ == "__main__":
    asyncio.run(main())
