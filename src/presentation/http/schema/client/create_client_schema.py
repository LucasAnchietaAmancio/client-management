from pydantic import BaseModel, Field, StrictInt

class CreateClientRequestSchema(BaseModel):
    client_name: str = Field(min_length=1, max_length=255)
    client_email: str = Field(min_length=1, max_length=255)
    type_request: str = Field(min_length=1, max_length=50)
    asset_value: StrictInt = Field(ge=0)
