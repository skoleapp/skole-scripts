import asyncio
import signal
import sys
from pathlib import Path

import aiohttp
import pypeln

URL = "https://koulutushaku.turkuamk.fi/result.php?id={id}"

COURSES_HTML = Path(__file__).resolve(strict=True).parent.parent.parent / "generated/tuas-courses.html"
MIN = 1
MAX = 30_000
WORKERS = 100

urls = (URL.format(id=i) for i in range(MIN, MAX))


async def main():

    def save(*args, **kwargs):
        with open(COURSES_HTML, "w") as f:
            for line in processed:
                f.write(f"{line}")
        print(f"Successfully loaded {len(processed)} courses, encountered {len(errors)} HTTP errors.")
        joined = "\n".join(errors)
        print(f"Errors were:\n{joined}")
        sys.exit(0)

    signal.signal(signal.SIGINT, save)

    try:
        with open(COURSES_HTML, "r") as f:
            processed = f.readlines()
    except FileNotFoundError:
        processed = []
    errors = []

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=0)) as session:

        async def fetch(url):
            async with session.get(url) as res:
                length = res.headers.get('Content-Length')
                status = res.status
                msg = f"id: {url: <55} - status code: {status} - length {length}"
                print(msg)
                if status == 200:
                    if length != "1604":
                        processed.append(await res.text())
                else:
                    errors.append(msg)

        await pypeln.task.each(fetch, urls, workers=WORKERS)

    save()


if __name__ == "__main__":
    asyncio.run(main())
