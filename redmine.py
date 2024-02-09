import asyncio
from collections.abc import Iterable
import datetime
from typing import TYPE_CHECKING

import math
from pydantic import BaseModel
from tabulate import tabulate

if TYPE_CHECKING:
    from aiohttp import ClientSession
    from config import RedmineConfig


class RedmineIssue(BaseModel):
    id: int


class RedmineTimeEntry(BaseModel):
    comments: str
    hours: float
    issue: RedmineIssue
    spent_on: datetime.date


class Redmine:
    def __init__(self, config: "RedmineConfig", session: "ClientSession"):
        self.config = config
        self.session = session

    async def add_costs(self, data: dict[str, dict[int, dict[str, int]]]) -> None:
    async def create_time_entries(self, data: dict[str, dict[int, dict[str, int]]]) -> None:
        tasks = [
            asyncio.create_task(
                self._create_time_entry(
                    task_id=task_id,
                    hours=self._secs_to_hours(secs),
                    spent_on=spent_on,
                    comments=comment or self.config.default_comment,
                )
            )
            for spent_on, tasks in data.items()
            for task_id, comments in tasks.items()
            for comment, secs in comments.items()
        ]
        responses = await asyncio.gather(*tasks)
        self._print_report(responses)

    async def _create_time_entry(self, task_id: int, hours: float, spent_on: str, comments: str) -> RedmineTimeEntry:
        json = {
            "time_entry": {
                "issue_id": task_id,
                "hours": hours,
                "activity_id": self.config.activity_id,
                "spent_on": spent_on,
                "comments": comments.strip().capitalize(),
            }
        }
        async with self.session.post(
            f"{self.config.url}/time_entries.json", headers=self.headers, json=json
        ) as response:
            response = await response.json()
            return RedmineTimeEntry.model_validate(response["time_entry"])

    def _secs_to_hours(self, secs: int) -> float:
        hours = secs / 60 / 60

        if self.config.round_costs:
            hours = math.ceil(hours * 10) / 10
        else:
            hours = round(hours, 2)

        return hours

    @staticmethod
    def _print_report(time_entries: Iterable[RedmineTimeEntry]) -> None:
        table = (
            (entry.issue.id, entry.comments, entry.hours, entry.spent_on)
            for entry in sorted(time_entries, key=lambda x: (x.spent_on, x.hours), reverse=True)
        )
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
