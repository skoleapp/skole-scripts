from pathlib import Path

from bs4 import BeautifulSoup

from importer.templates import COURSE, SUBJECT, SUBJECT_TRANSLATION

COURSES_HTML = Path(__file__).resolve(strict=True).parent.parent.parent / "generated/tuas-courses.html"
COURSES_YAML = Path(__file__).resolve(strict=True).parent.parent.parent / "generated/tuas-courses.yaml"
SUBJECTS_YAML = Path(__file__).resolve(strict=True).parent.parent.parent / "generated/tuas-subjects.yaml"

# There are so few different units (=subjects), so haven't bothered to fetch the
# translated data, but instead just manually translated them.
#
# Even though the TUAS koulutushaku service would also offer translated names for the
# courses, we also don't want to bother with that, since for our own sanity our courses
# only have the name specified in one language.
subject_translation_map = {
    "Tekniikka ja liiketoiminta": {
        "en": "Engineering and Business", "sv": "Teknik och affärsverksamhet",
    },
    "Terveys ja hyvinvointi": {
        "en": "Health and Well-being", "sv": "Hälsa och välmående",
    },
    "Taideakatemia": {
        "en": "Arts Academy", "sv": "Konstakademi",
    },
    "Yhteiset palvelut": {
        "en": "Corporate Services", "sv": "Gemensamma tjänster",
    }
}

def main():
    with open(COURSES_HTML) as f:
        # Manually edited the file to contain exactly one HTML document per line.
        courses_html = f.readlines()

    subject_translations = []
    subjects = []
    subject_id = 249  # Existing fixtures end in 248.

    courses = []
    course_id = 7100  # Existing fixtures end in 7021, but need to leave some leeway for user generated ones.

    subject_name_to_id = {}
    used_courses = set()

    for course_html in courses_html:
        soup = BeautifulSoup(course_html, features="html5lib")
        # Checked manually that all courses have the name and code specified,
        # the unit (=subject) is missing from a few though.
        name = soup.find("div", attrs={"id": "name", "class": "value"}).string
        code = soup.find("div", attrs={"id": "code", "class": "value"}).string
        code = code.split("-")[0]  # the -1234 after the code basically just identifies the instance.
        subject = getattr(soup.find("div", attrs={"id": "unit", "class": "value"}), "string", None)

        if subject and subject not in subject_name_to_id:
            subject_translations.append(
                SUBJECT_TRANSLATION.format(
                    id1=subject_id * 3 - 2,
                    id2=subject_id * 3 - 1,
                    id3=subject_id * 3,
                    subject_id=subject_id,
                    name_en=subject_translation_map[subject]["en"],
                    name_fi=subject,
                    name_sv=subject_translation_map[subject]["sv"],
                )
            )
            subjects.append(
                SUBJECT.format(
                    id=subject_id,
                )
            )
            subject_name_to_id[subject] = subject_id
            subject_id += 1

        if not (code, subject) in used_courses:
            courses.append(
                COURSE.format(
                    id=course_id,
                    name=name,
                    code=code,
                    subjects=[subject_name_to_id[subject]] if subject else [],
                )
            )
            used_courses.add((code, subject))
            course_id += 1

    with open(SUBJECTS_YAML, "w") as f:
        f.writelines(subject_translations)
        f.write("\n")
        f.writelines(subjects)

    with open(COURSES_YAML, "w") as f:
        f.writelines(courses)


if __name__ == "__main__":
    main()
