from fastapi.security import APIKeyHeader
from fastapi import Security, HTTPException
import os

protected_route = APIKeyHeader(
    name="X-Shopware-Api-Key"
)

async def require_api_key(api_key_header: str = Security(protected_route)):
    if len(api_key_header) > 0 and api_key_header == os.environ.get("KNOWLEDGE_API_KEY"):
        return api_key_header

    raise HTTPException(
        status_code=403,
        detail="Could not validate API KEY",
    )