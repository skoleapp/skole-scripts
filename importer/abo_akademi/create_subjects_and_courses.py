import json
import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import yaml

from importer.templates import COURSE, SUBJECT, SUBJECT_TRANSLATION

COURSES_JSON = Path(__file__).resolve(strict=True).parent.parent.parent / "generated/abo-akademi-courses.json"
COURSES_YAML = Path(__file__).resolve(strict=True).parent.parent.parent / "generated/abo-akademi-courses.yaml"
SUBJECTS_YAML = Path(__file__).resolve(strict=True).parent.parent.parent / "generated/abo-akademi-subjects.yaml"

INITIAL_SUBJECTS = Path(__file__).resolve(strict=True).parent.parent.parent / "generated/initial-subjects.yaml"


def main() -> None:
    def get_subject_names(subject_dict: dict[str, str], key: str) -> Iterable[str]:
        for name in subject_dict[key].split(","):
            if "/" in name:
                # Some languages can be in the form 'marketing / international marketing'.
                name = name.split("/")[1]
            name = name.strip()
            if name:
                name = name[0].upper() + name[1:]
            yield name

    def get_course_name(course_json: dict[str, Any]) -> str:
        name = course_json["name"]["valueEn"]  # The English name is always the authoritative one we want to use.
        return name

    with open(COURSES_JSON) as f:
        courses_json = json.load(f)

    course_code_to_id = {}

    try:
        with open(INITIAL_SUBJECTS, "r") as f:
            models = yaml.safe_load(f)
            subject_name_to_id = {
                model["fields"]["name"].lower(): model["fields"]["master"]
                for model in models if model["fields"].get("language_code") == "en"
            }
    except FileNotFoundError:
        subject_name_to_id = {}

    subject_translations = []
    subjects = []
    subject_id = 253  # Existing fixtures end in 252.

    courses = []
    course_id = 8400  # Existing fixtures end in 8635, but need to leave some leeway for user generated ones.

    for course_json in courses_json:
        subject_dict = course_json["contentList"][12]["content"]

        if any(subject_dict.values()):
            # If the course doesn't have any subjects set, it's probably some trash data that we do not want.
            subject_names_en = get_subject_names(subject_dict, "valueEn")
            subject_names_fi = get_subject_names(subject_dict, "valueFi")
            subject_names_sv = get_subject_names(subject_dict, "valueSv")

            subjects_of_course = []
            for name_en, name_fi, name_sv in zip(subject_names_en, subject_names_fi, subject_names_sv):
                if name_en.lower() not in subject_name_to_id:
                    subject_translations.append(
                        SUBJECT_TRANSLATION.format(
                            id1=subject_id * 3 - 2,
                            id2=subject_id * 3 - 1,
                            id3=subject_id * 3,
                            subject_id=subject_id,
                            name_en=name_en,
                            name_fi=name_fi,
                            name_sv=name_sv,
                        )
                    )
                    subjects.append(
                        SUBJECT.format(
                            id=subject_id,
                        )
                    )
                    subject_name_to_id[name_en.lower()] = subject_id
                    subject_id += 1

                subjects_of_course.append(subject_name_to_id[name_en.lower()])

            if course_json["code"] not in course_code_to_id:
                courses.append(
                    COURSE.format(
                        id=course_id,
                        name=get_course_name(course_json),
                        code=course_json["code"],
                        subjects=sorted(subjects_of_course),
                    )
                )
                course_id += 1

    with open(SUBJECTS_YAML, "w") as f:
        f.writelines(subject_translations)
        f.write("\n")
        f.writelines(subjects)

    with open(COURSES_YAML, "w") as f:
        f.writelines(courses)


if __name__ == "__main__":
    main()
