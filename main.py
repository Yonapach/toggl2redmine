import asyncio

import aiohttp

from config import redmine_config, toggl_settings
from redmine import Redmine
from toggl import Toggl


async def main():
    async with aiohttp.ClientSession() as session:
        toggl = Toggl(config=toggl_settings, session=session)
        redmine = Redmine(config=redmine_config, session=session)

        entries = await toggl.entries
        await redmine.add_costs(entries)


if __name__ == "__main__":
    asyncio.run(main())
