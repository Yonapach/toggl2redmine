from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class TogglConfig(BaseSettings):
    api_key: str
    url: HttpUrl = HttpUrl("https://api.track.toggl.com/api/v9/me")
    days_offset: int = 0

    class Config:
        env_prefix = "toggl_"


class RedmineConfig(BaseSettings):
    api_key: str
    activity_id: int
    url: HttpUrl
    round_costs: bool = False
    default_comment: str = "Выполнение требований задачи"

    class Config:
        env_prefix = "redmine_"


toggl_settings = TogglConfig()
redmine_config = RedmineConfig()
