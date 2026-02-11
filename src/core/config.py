from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    OPENAI_API_KEY: SecretStr
    
    DB_NAME: str = "bot_memory.db"
    
    AI_MODEL: str = "gpt-4o-mini" 

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings()