from pydantic import BaseModel, Field

class ProcessEventSchema(BaseModel):
    event_id: str = Field(min_length=1, max_length=255)
    card_id: str = Field(min_length=1, max_length=255)
    client_email: str = Field(min_length=1, max_length=255)
    timestamp: str = Field(min_length=1, max_length=255)