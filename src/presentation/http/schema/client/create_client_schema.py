from pydantic import AliasChoices, BaseModel, Field, StrictInt

class CreateClientRequestSchema(BaseModel):
    client_name: str = Field(min_length=1,max_length=255,validation_alias=AliasChoices("client_name", "cliente_nome"))
    client_email: str = Field(min_length=1,max_length=255,validation_alias=AliasChoices("client_email", "cliente_email"))
    type_request: str = Field(min_length=1,max_length=50,validation_alias=AliasChoices("type_request", "tipo_solicitacao"),)
    asset_value: StrictInt = Field(ge=0,validation_alias=AliasChoices("asset_value", "valor_patrimonio"))
