from pydantic import AliasChoices, BaseModel, Field

class ProcessEventSchema(BaseModel):
    event_id: str = Field(min_length=1, max_length=255)
    card_id: str = Field(min_length=1, max_length=255)
    client_email: str = Field(min_length=1,max_length=255,validation_alias=AliasChoices("client_email", "cliente_email"))
    timestamp: str = Field(min_length=1, max_length=255)
