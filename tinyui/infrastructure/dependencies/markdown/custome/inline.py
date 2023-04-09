import re
from typing import Any, Tuple

from mistune.core import InlineState
from mistune.inline_parser import InlineParser
from mistune.helpers import parse_link, parse_link_label, parse_link_text
from mistune.util import unikey


class DocDiffLangParser(InlineParser):
    """Inline Parser with different language."""

    def parse_link(self, m: re.Match, state: InlineState) -> int | None:
        # 2 things:
        # - Link to markdown => Link to route
        # - Detect different language
        pos = m.end()

        marker = m.group(0)
        is_image = marker[0] == "!"
        if is_image and state.in_image:
            state.append_token({"type": "text", "raw": marker})
            return pos
        elif not is_image and state.in_link:
            state.append_token({"type": "text", "raw": marker})
            return pos

        text: None | Any = None
        label, end_pos = parse_link_label(state.src, pos)
        if label is None:
            text, end_pos = parse_link_text(state.src, pos)
        if (text and label) or end_pos is None:  # For type annotation.
            return
        # end_pos: (int, int)

        if text is None:
            text = label

        if end_pos >= len(state.src) and label is None:
            return

        rules = ["codespan", "prec_auto_link", "prec_inline_html"]
        prec_pos = self.precedence_scan(m, state, end_pos, rules)
        if prec_pos:
            return prec_pos

        if end_pos < len(state.src):
            c = state.src[end_pos]
            if c == "(":
                # standard link [text](<url> "title")
                attrs, pos2 = parse_link(state.src, end_pos + 1)
                if pos2:
                    token = self.__parse_link_token(is_image, text, attrs, state)  # type: ignore
                    state.append_token(token)
                    return pos2

            elif c == "[":
                # standard ref link [text][label]
                label2, pos2 = parse_link_label(state.src, end_pos + 1)
                if pos2:
                    end_pos = pos2
                    if label2:
                        label = label2

        if label is None:
            return

        ref_links = state.env["ref_links"]
        key = unikey(label)
        env = ref_links.get(key)
        if env:
            attrs = {"url": env["url"], "title": env.get("title")}
            token = self.__parse_link_token(is_image, text, attrs, state)  # type: ignore
            token["ref"] = key
            token["label"] = label
            state.append_token(token)
            return end_pos

    def __parse_link_token(
        self, is_image: bool, text: str, attrs: dict, state: InlineState
    ):
        new_state = state.copy()
        new_state.src = text
        if is_image:
            new_state.in_image = True
            token = {
                "type": "image",
                "children": self.render(new_state),
                "attrs": attrs,
            }
        else:
            # TODO: Add link endswith ".md".
            new_state.in_link = True
            token = {
                "type": "link",
                "children": self.render(new_state),
                "attrs": attrs,
            }
        return token
