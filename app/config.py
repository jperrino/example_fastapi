from pydantic import BaseSettings


# pydantic allows retrieving environment variables from OS
# and check the variable type,
# also it does not matter if the variable is in lower case or capital
# default values can be given, but we are going to use a .env file to store
# the environment variables values
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_username: str
    database_password: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = '.env'


settings = Settings()

# print(settings.database_password)

