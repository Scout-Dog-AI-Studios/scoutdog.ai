from fastapi import APIRouter, Depends, HTTPException
from cassandra.cluster import Session  # Import Session for type hinting
from pydantic import BaseModel  # Import BaseModel for response model

# Import dependencies
from app.api.v1.dependencies import get_current_user_token_payload
from app.db.session import get_db_session  # Import DB session dependency

# Import the service function
from app.services.greeting import get_greeting_message

router = APIRouter()


class GreetResponse(BaseModel):
    message: str


@router.get("/greet", response_model=GreetResponse)
async def greet(
    payload=Depends(get_current_user_token_payload),
    session: Session = Depends(get_db_session),
):
    """
    Secured endpoint that returns a greeting from the database.
    Requires a valid JWT token.
    """
    try:
        message = get_greeting_message(session)
        if not message:
            # Fallback message if DB returns no rows or empty string
            return GreetResponse(message="No greeting found")
        return GreetResponse(message=message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch greeting: {e}")
