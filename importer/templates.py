# `school: 3` is Åbo Akademi
COURSE = """\
- model: skole.Course
  pk: {id}
  fields:
    name: "{name}"
    codes: ["{code}"]
    subjects: {subjects}
    school: 3
    user: null
    modified: "2021-01-15 12:00:00.000000+00:00"
    created: "2021-01-15 12:00:00.000000+00:00"
"""

SUBJECT = """\
- model: skole.Subject
  pk: {id}
  fields: {{}}
"""

SUBJECT_TRANSLATION = """\
- model: skole.SubjectTranslation
  pk: {id1}
  fields:
    language_code: en
    name: {name_en}
    master: {subject_id}
- model: skole.SubjectTranslation
  pk: {id2}
  fields:
    language_code: fi
    name: {name_fi}
    master: {subject_id}
- model: skole.SubjectTranslation
  pk: {id3}
  fields:
    language_code: sv
    name: {name_sv}
    master: {subject_id}
"""
