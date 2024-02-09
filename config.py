from datetime import datetime, date, timedelta

from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    days_offset: int = 0

    @property
    def day(self) -> date:
        return datetime.now().date() - timedelta(days=base_config.days_offset)


class TogglConfig(BaseSettings):
    api_key: str
    url: HttpUrl = HttpUrl("https://api.track.toggl.com/api/v9/me")

    class Config:
        env_prefix = "toggl_"


class RedmineConfig(BaseSettings):
    api_key: str
    activity_id: int
    user_id: int
    url: HttpUrl
    round_costs: bool = False
    default_comment: str = "Выполнение требований задачи"

    class Config:
        env_prefix = "redmine_"


base_config = Config()
toggl_config = TogglConfig()
redmine_config = RedmineConfig()
