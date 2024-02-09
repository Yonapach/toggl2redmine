from base64 import b64encode
from collections import defaultdict
from datetime import timedelta, date
from typing import TYPE_CHECKING

from config import base_config

if TYPE_CHECKING:
    from aiohttp import ClientSession
    from config import TogglConfig


class Toggl:
    def __init__(self, config: "TogglConfig", session: "ClientSession"):
        self.config = config
        self.session = session

    async def _get_entries(self, day: date) -> dict:
        url = f"{self.config.url}/time_entries"
        params = {"start_date": str(day), "end_date": str(day + timedelta(days=1))}

        async with self.session.get(url, headers=self.headers, params=params) as response:
            return await response.json()

    async def _get_projects(self) -> dict:
        url = f"{self.config.url}/projects"
        async with self.session.get(url, headers=self.headers) as response:
            return await response.json()

    @property
    async def entries(self) -> dict[str, dict[int, dict[str, int]]]:
        projects = await self.projects
        entries = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

        for entry in await self._get_entries(base_config.day):
            if entry["stop"] is None:
                raise Exception("There are running time entries")

            d_end = entry["stop"][:10]
            duration = entry["duration"]
            project_id = entry["project_id"]
            description = entry["description"]
            task_id = int(projects[project_id])  # lazy validating

            entries[d_end][task_id][description] += duration

        return entries

    @property
    async def projects(self) -> dict[int, str]:
        response = await self._get_projects()
        return {row["id"]: row["name"] for row in response}

    @property
    def headers(self) -> dict[str, str]:
        token = b64encode(f"{self.config.api_key}:api_token".encode()).decode("ascii")
        return {"content-type": "application/json", "Authorization": f"Basic {token}"}
