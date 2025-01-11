import os
from dotenv import load_dotenv

load_dotenv()

class Settings: 
    # JWT 
    SECRET_KEY:str = os.getenv("SECRET_KEY")      
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES:int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    REFRESH_TOKEN_EXPIRE_DAYS:int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
    
    if not SECRET_KEY or not ALGORITHM:
        raise ValueError("Environment variables SECRET_KEY and ALGORITHM must be set!")


    # db
    db_user:str = os.getenv("DB_USER")
    db_password: str = os.getenv("DB_PASSWORD")
    db_host: str = os.getenv("DB_HOST")
    db_port: int = int(os.getenv("DB_PORT"))
    db_name: str = os.getenv("DB_NAME")
    #HF
    api_key: str = os.getenv("HF_API_KEY")
    
    @property
    def database_url(self) -> str:
        return f"postgres://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
   
settings = Settings()
