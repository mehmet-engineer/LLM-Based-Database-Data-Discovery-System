from pydantic_settings import BaseSettings, SettingsConfigDict

# create a settings class as a subclass of BaseSettings to load env variables
class Settings(BaseSettings):
    # System DB
    SYSTEM_DB_USER: str
    SYSTEM_DB_PASSWORD: str
    SYSTEM_DB_NAME: str
    SYSTEM_DB_HOST: str
    SYSTEM_DB_PORT: str

    # Auth
    AUTH_USERNAME: str
    AUTH_PASSWORD: str

    # LLM
    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# instantiate the settings class to load the environment variables
settings = Settings()