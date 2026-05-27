from pydantic import BaseModel, Field

class CreateClientRequestSchema(BaseModel):
    client_name: str = Field(min_length=1, max_length=100)
    client_email: str = Field(min_length=1, max_length=100)
    type_request: str = Field(min_length=1, max_length=50)
    asset_value: int = Field(ge=0)

