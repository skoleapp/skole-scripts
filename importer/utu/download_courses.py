import json
import os
import signal
import sys

import requests

URL = "https://opas.peppi.utu.fi/api/course/{id}"
COURSES_JSON = os.path.join(os.path.dirname(__file__) + "/generated/utu-courses.json")
MIN = 880
MAX = 25000


def main():
    success_count = 0
    error_count = 0

    def save(*args, **kwargs):
        with open(COURSES_JSON, "w") as f:
            json.dump(processed, f, indent=2)
        print(f"Successfully loaded {success_count} courses, encountered {error_count} HTTP errors.")
        sys.exit(0)

    signal.signal(signal.SIGINT, save)

    try:
        with open(COURSES_JSON, "r") as f:
            processed = json.load(f)
    except FileNotFoundError:
        processed = []

    for i in range(MIN, MAX):
        res = requests.get(URL.format(id=i))
        print(f"id: {i} - status code: {res.status_code}")
        if res.status_code == 200:
            processed.append(res.json())
            success_count += 1
        else:
            error_count += 1

    save()


if __name__ == "__main__":
    main()
