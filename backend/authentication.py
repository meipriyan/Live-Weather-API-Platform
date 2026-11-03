from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Customer


# Read API key from request header
api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False
)


def verify_api_key(
    api_key: str = Security(api_key_header),
    db: Session = Depends(get_db)
):

    # Check whether API key was provided
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API key is missing"
        )

    # Search for the API key in MySQL
    customer = (
        db.query(Customer)
        .filter(Customer.api_key == api_key)
        .first()
    )

    # Reject unknown or inactive customers
    if customer is None or not customer.is_active:
        raise HTTPException(
            status_code=401,
            detail="Invalid or inactive API key"
        )

    return customer