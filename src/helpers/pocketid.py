import httpx
from dotenv import load_dotenv
import os
import logging
import re

load_dotenv()
logger = logging.getLogger("oa-connector")

group_pattern = os.getenv('SYNC_GROUP_REGEX', default=None)
group_regex = None
if group_pattern:
    group_regex = re.compile(group_pattern, re.IGNORECASE)

async def get_pocketid_groups_of_user(email: str) -> list:
    pocketid_groups = []
    
    pocket_id_url = os.getenv('POCKET_ID_URL')
    pocket_id_api_key = os.getenv('POCKET_ID_API_KEY')
    
    if not pocket_id_url or not pocket_id_api_key:
        logger.error("POCKET_ID_URL or POCKET_ID_API_KEY is not set.")
        return pocketid_groups
        
    api_url = f"{pocket_id_url}/api/users"
    headers = {
        "X-API-KEY": pocket_id_api_key,
        "Accept": "application/json"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{api_url}?search={email}", headers=headers)
            response.raise_for_status()
            
            data = response.json()
            if "data" not in data or not data["data"]:
                logger.debug(f"No Pocket ID user found matching email {email}")
                return pocketid_groups
                
            target_user = None
            for user in data["data"]:
                if user.get("email") == email:
                    target_user = user
                    break
                    
            if not target_user:
                logger.debug(f"No Pocket ID user found with exact email {email}")
                return pocketid_groups
                
            user_groups = target_user.get("userGroups", [])
            
            for group in user_groups:
                group_name = group.get("name")
                if group_name:
                    if (group_regex and group_regex.match(group_name)) or not group_regex:
                        pocketid_groups.append(group_name)
                        
    except Exception as e:
        logger.error(f"Error fetching groups from Pocket ID: {e}")
        
    logger.info(f"Got {len(pocketid_groups)} groups for user {email} from Pocket ID (after regex filtering, if applied)")
    return pocketid_groups
