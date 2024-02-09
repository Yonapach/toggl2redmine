import asyncio

import aiohttp

from config import redmine_config, toggl_config
from redmine import Redmine
from toggl import Toggl


async def main():
    async with aiohttp.ClientSession() as session:
        toggl = Toggl(config=toggl_config, session=session)
        redmine = Redmine(config=redmine_config, session=session)

        entries = await toggl.entries
        await redmine.create_time_entries(entries)


if __name__ == "__main__":
    asyncio.run(main())
