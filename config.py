from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    toggl_api_key: str
    round_costs: bool = False
    days_offset: int = 0


class RedmineConfig(BaseSettings):
    api_key: str
    activity_id: int
    url: HttpUrl

    class Config:
        env_prefix = "redmine_"


settings = Settings()
redmine_config = RedmineConfig()
