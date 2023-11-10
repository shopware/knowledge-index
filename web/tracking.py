import httpx
from posthog import Posthog
import os

async def send_event(user, event, data = {}):
    if "POSTHOG_PROJECT_API_KEY" not in os.environ:
        return None
    
    posthog = Posthog(project_api_key=os.environ['POSTHOG_PROJECT_API_KEY'], host='https://eu.posthog.com')
    posthog.capture(user, event, data)
    
    return True