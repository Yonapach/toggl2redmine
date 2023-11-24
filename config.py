from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    toggl_api_key: str
    redmine_api_key: str
    redmine_activity_id: int
    redmine_url: HttpUrl
    days_offset: int = 0


settings = Settings()
