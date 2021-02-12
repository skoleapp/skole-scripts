import asyncio
import json
import signal
import sys
from pathlib import Path
from types import FrameType
from typing import NoReturn, Optional

import aiohttp
import pypeln

URL = "https://studiehandboken.abo.fi/api/course/{id}"
COURSES_JSON = Path(__file__).resolve(strict=True).parent.parent.parent / "generated/abo-akademi-courses.json"
MIN = 1
MAX = 30_000
WORKERS = 100

urls = (URL.format(id=i) for i in range(MIN, MAX))


async def main() -> None:
    def save(signum: Optional[int] = None, frame: Optional[FrameType] = None) -> NoReturn:
        with open(COURSES_JSON, "w") as f:
            json.dump(processed, f, indent=2, ensure_ascii=False)
        print(f"Successfully loaded {len(processed)} courses, encountered {len(errors)} HTTP errors.")
        if errors:
            joined = "\n".join(errors)
            print(f"Errors were:\n{joined}")
        sys.exit(0)

    signal.signal(signal.SIGINT, save)

    try:
        with open(COURSES_JSON, "r") as f:
            processed = json.load(f)
    except FileNotFoundError:
        processed = []
    errors = []

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=0)) as session:

        async def fetch(url):
            async with session.get(url) as res:
                status = res.status
                msg = f"{url: <50} - status code: {status}"
                print(msg)
                if status == 200:
                    processed.append(await res.json())
                else:
                    errors.append(msg)

        await pypeln.task.each(fetch, urls, workers=WORKERS)

    save()


if __name__ == "__main__":
    asyncio.run(main())
