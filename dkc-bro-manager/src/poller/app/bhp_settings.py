from pydantic_settings import BaseSettings, SettingsConfigDict


class SharedSettings(BaseSettings):
    manager_url: str
    bhp_endpoint: str


class RwsBhpSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='RWS_')

    org_code: str
    bhp_username: str
    bhp_token: str


class IctuBhpSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='ICTU_')

    org_code: str
    bhp_username: str
    bhp_token: str

# Add settings for additional organization here, example:
#
# class ProvincieHollandSettings(BaseSettings):
#     model_config = SettingsConfigDict(env_prefix='PROVINCIE_HOLLAND_')
#
#     org_code: str
#     bhp_endpoint: str
#     bhp_username: str
#     bhp_token: str
