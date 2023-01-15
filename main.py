import asyncio
from base64 import b64encode
from collections import defaultdict
from datetime import datetime, timedelta, date
from pprint import pprint

import aiohttp


TOGGL_API_KEY = ...
REDMINE_API_KEY = ...
REDMINE_ACTIVITY_ID = 9

today = datetime.now().date()


async def get_toggl_entries(session: aiohttp.ClientSession, d_start: date, d_end: date) -> dict:
    url = f"https://api.track.toggl.com/api/v9/me/time_entries"
    token = b64encode(f"{TOGGL_API_KEY}:api_token".encode()).decode("ascii")
    headers = {"content-type": "application/json", "Authorization": f"Basic {token}"}
    params = {"start_date": str(d_start), "end_date": str(d_end)}

    async with session.get(url, headers=headers, params=params) as response:
        return await response.json()


def group_by_task_and_date(data) -> defaultdict[str, defaultdict[int, int]]:
    res = defaultdict(lambda: defaultdict(int))
    for row in data:
        d_end = row["stop"][:10]
        duration = row["duration"]
        task_id = int(row["description"])  # lazy validate

        res[d_end][task_id] += duration

    return res


def secs_to_hours(secs: int) -> float:
    hours = secs / 60 / 60
    hours = round(hours, 2)
    return hours


async def add_costs(session: aiohttp.ClientSession, data) -> list[dict]:
    tasks = []
    for spent_on, time_by_task in data.items():
        for task_id, secs in time_by_task.items():
            tasks.append(asyncio.ensure_future(add_cost(session, task_id, secs, spent_on)))

    return await asyncio.gather(*tasks)


async def add_cost(session: aiohttp.ClientSession, task_id: int, secs: int, spent_on: str) -> dict:
    url = "https://redmine.sbps.ru/time_entries.json"
    headers = {"content-type": "application/json", "X-Redmine-API-Key": REDMINE_API_KEY}
    json = {
        "time_entry": {
            "issue_id": task_id,
            "hours": secs_to_hours(secs),
            "activity_id": REDMINE_ACTIVITY_ID,
            "spent_on": spent_on,
        }
    }
    async with session.post(url, headers=headers, json=json) as response:
        return await response.json()


async def main():
    async with aiohttp.ClientSession() as session:
        toggl_entries = await get_toggl_entries(session, today, today + timedelta(days=1))
        data = group_by_task_and_date(toggl_entries)
        responses = await add_costs(session, data)

        pprint(responses)
        print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
