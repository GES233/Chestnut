from typing import List, Any, Dict
from multidict import CIMultiDict  # type: ignore


def parseheaders(
    headers: CIMultiDict[str] | Dict[str, str]
) -> List[Dict[str, str | int]]:
    language_ = headers.get("Accept-Language")
    if not language_:
        language_ = ["en;q=0.8", "*;q=0.5"]
    else:
        language_ = language_.split(",")
        # Example:
        # ['zh-CN', 'zh;q=0.9', 'en;q=0.8', 'en-GB;q=0.7', 'en-US;q=0.6', 'zh-TW;q=0.5']
    language = []
    for lang_item in language_:
        if ";q=" in lang_item:
            lang_id, weight = lang_item.split(";q=")
        else:
            lang_id, weight = lang_item, "1.0"
        language.append(dict(lang=lang_id, weight=float(weight)))
    # language example:
    # [
    # {'lang': 'zh-CN', 'weight': 1.0},
    # {'lang': 'zh', 'weight': 0.9},
    # {'lang': 'en', 'weight': 0.8},
    # {'lang': 'en-GB', 'weight': 0.7},
    # {'lang': 'en-US', 'weight': 0.6},
    # {'lang': 'zh-TW', 'weight': 0.5}]
    return language
