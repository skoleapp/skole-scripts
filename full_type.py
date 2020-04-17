import json
from typing import Any, Dict, List, Optional

JsonDict = Dict[str, Any]


def fields(max_depth: int, depth: int = 0) -> str:
    if depth == max_depth:
        return ""
    return (
        f"""
        fields {{
            name
            type {{
                name
                {fields(max_depth, depth + 1)}
                {of_type(max_depth, depth + 1)}
            }}
        }}
        """
    )

def of_type(max_depth: int, depth: int = 0) -> str:
    if depth == max_depth:
        return ""
    return (
        f"""
        ofType {{
            name
            {fields(max_depth, depth + 1)}
            {of_type(max_depth, depth + 1)}
        }}
        """
    )



def full_type(max_depth: int) -> str:
    return (
        f"""
        fragment FullType on __Type {{
            name
            {fields(max_depth)}
            {of_type(max_depth)}
        }}

        query introspectionFullType($name: String!) {{
            __type(name: $name) {{
                ...FullType
            }}
        }}
        """
    )


def remove_empty_elements(d):
    """recursively remove empty lists, empty dicts, or None elements from a dictionary"""

    def empty(x, key=None):
        return x is None or x == {} or x == [] or (key == "name" and isinstance(x, str) and x[0].isupper())


    if isinstance(d, list):
        return [v for v in (remove_empty_elements(v) for v in d) if not empty(v)]
    elif isinstance(d, dict):
        return {k: v for k, v in ((k, remove_empty_elements(v)) for k, v in d.items()) if not empty(v, k)}
    else:
        return d


def flatten_of_types(d):

    def is_of_type(value):
        return isinstance(value, dict) and len(value) == 1 and "ofType" in value

    if isinstance(d, list):
        return [v for v in (flatten_of_types(v) for v in d)]
    elif isinstance(d, dict):
        return {k: (next(iter(v.values())) if is_of_type(v) else v) for k, v in ((k, flatten_of_types(v)) for k, v in d.items())}
    else:
        return d


def main() -> None:
    query = full_type(2)
    with open("full_type.graphql", "w") as f:
        f.write(query)
    with open("result.json") as f:
        result = json.load(f)["data"]["__type"]

    # with open("result.json") as f:
    #     result = json.load(f)["data"]["__type"]

    # result = remove_empty_elements(result)
    # result = flatten_of_types(result)


    # with open("filtered.json", "w") as f:
    #     json.dump(result, f, indent=2)



if __name__ == "__main__":
    main()
