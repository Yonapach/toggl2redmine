import asyncio
from collections.abc import Iterable
import datetime
from typing import TYPE_CHECKING

from aiohttp import ClientSession
import math
from pydantic import BaseModel
from tabulate import tabulate

if TYPE_CHECKING:
    from config import RedmineConfig


class RedmineIssue(BaseModel):
    id: int


class RedmineTimeEntry(BaseModel):
    comments: str
    hours: float
    issue: RedmineIssue
    spent_on: datetime.date


class RedmineTimeEntryResponse(BaseModel):
    time_entry: RedmineTimeEntry


class Redmine:
    def __init__(self, config: "RedmineConfig", session: ClientSession):
        self.config = config
        self.session = session

    async def add_costs(self, data: dict[str, dict[int, dict[str, int]]]) -> None:
        tasks = [
            asyncio.create_task(self.add_cost(task_id, secs, spent_on, comment))
            for spent_on, details_by_task in data.items()
            for task_id, details in details_by_task.items()
            for comment, secs in details.items()
        ]
        responses = await asyncio.gather(*tasks)
        self._print_report(responses)

    async def add_cost(self, task_id: int, secs: int, spent_on: str, comment: str) -> RedmineTimeEntryResponse:
        json = {
            "time_entry": {
                "issue_id": task_id,
                "hours": self._secs_to_hours(secs),
                "activity_id": self.config.activity_id,
                "spent_on": spent_on,
                "comments": comment,
            }
        }
        async with self.session.post(
            f"{self.config.url}/time_entries.json", headers=self.headers, json=json
        ) as response:
            response = await response.json()
            return RedmineTimeEntryResponse(**response)

    def _secs_to_hours(self, secs: int) -> float:
        hours = secs / 60 / 60

        if self.config.round_costs:
            hours = math.ceil(hours * 20) / 20
        else:
            hours = round(hours, 2)

        return hours

    @staticmethod
    def _print_report(responses: Iterable[RedmineTimeEntryResponse]) -> None:
        entries = sorted(
            (response.time_entry for response in responses),
            key=lambda x: (x.spent_on, x.hours),
            reverse=True,
        )
        table = ((entry.issue.id, entry.comments, entry.hours, entry.spent_on) for entry in entries)
        print(
            tabulate(
                table,
                headers=("task_id", "comment", "hours", "spent_on"),
                tablefmt="rounded_outline",
                numalign="center",
                stralign="center",
                floatfmt=".2f",
            )
        )

    @property
    def headers(self) -> dict[str, str]:
        return {"content-type": "application/json", "X-Redmine-API-Key": self.config.api_key}
