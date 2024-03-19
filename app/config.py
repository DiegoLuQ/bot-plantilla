from pathlib import Path
from dotenv import load_dotenv
from os import environ



env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path)


class Settings:
    token = environ.get('token_access')
    wsp_url = environ.get('WSP_URL')
    wsp_token = environ.get('TOKEN_WSP')


settings = Settings()