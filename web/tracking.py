import httpx
from posthog import Posthog

async def send_event(user, event, data = {}):
    posthog = Posthog(project_api_key='', host='https://eu.posthog.com')
    posthog.capture(user, event, data)


async def send_ga4_event(event_category, event_action):
    # Example usage
    secret = ""
    measurement_id = 'G-HZ6YQPQ2NR'
    client_id = '1133884939.1673614912'

    endpoint_url = f'https://www.google-analytics.com/mp/collect?measurement_id={measurement_id}&api_secret={secret}'
    payload = {
        "client_id": client_id,
        "events": [
            {
                "name": "qa",
                "params": {}
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(endpoint_url, data=payload)

    if response.status_code == 204:
        print("Event sent successfully!")
    else:
        print(response)
        print(f"Error sending event. Status code: {response.status_code}")