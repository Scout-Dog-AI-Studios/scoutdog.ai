from cassandra.cluster import Session, ResponseFuture
from cassandra import ConsistencyLevel  # Import Consistency Level
from cassandra.query import SimpleStatement  # Import SimpleStatement
import logging

logger = logging.getLogger(__name__)

# Define consistency level (optional, defaults to LOCAL_ONE or ONE depending on setup)
# Read operations often use LOCAL_QUORUM or QUORUM for consistency
READ_CONSISTENCY = ConsistencyLevel.LOCAL_QUORUM


def get_greeting_message(session: Session) -> str:
    """
    Fetches a greeting message from the 'greetings' table.
    Returns the message or a default string if none found or on error.
    """
    logger.info("Attempting to fetch greeting from database...")
    default_greeting = "Hello from the backend (DB fetch failed)!"
    query = "SELECT message FROM greetings LIMIT 1"  # Simple query for now

    # Prepare statement for better performance and security if parameters were used
    try:
        statement = SimpleStatement(query, consistency_level=READ_CONSISTENCY)
        result_set: ResponseFuture = session.execute_async(
            statement
        )  # Use async execute
        row = result_set.result().one()  # Wait for result and get one row

        if row:
            logger.info("Successfully fetched greeting from DB.")
            return row.message
        else:
            logger.warning("No greeting found in the database.")
            return "Hello from the backend (No greeting in DB)!"

    except Exception as e:
        logger.exception(f"Error fetching greeting from database: {e}")
        # In a real app, you might want to raise a specific exception
        return default_greeting
