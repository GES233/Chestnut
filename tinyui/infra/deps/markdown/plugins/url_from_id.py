""" tinyui.infrastructrue.deps.markdown.plugins.url_from_id

    Generate url from web-id.
"""
from mistune.markdown import Markdown
from mistune.util import escape_url


# ==== Some other site example ====
# Markdown: [[av10492]]
# ==> <a href="https://www.bilibili.com/video/av10492">av10492</a>

SITE_PATTERN = r"\[\[" "{}" r"\]\]"

ACFUN_SITE_PATTERN = SITE_PATTERN.format(r"ac[\d]+?")
BILI_AV_SITE_PATTERN = SITE_PATTERN.format(r"av[\d]+?")
BILI_BV_SITE_PATTERN = SITE_PATTERN.format(r"BV[\w]+?")

acfun_video = lambda vid: '<a href="https://www.acfun.cn/{0}">{0}</a>'.format(
    vid.strip("[").strip("]")
)
bili_video = lambda vid: '<a href="https://www.bilibili.com/video/{0}">{0}</a>'.format(
    vid.strip("[").strip("]")
)
# youtube_video = lambda vid: '<a href="https://youtu.be/watch?={}">{0}</a>'.format(vid.strip("[").strip("]"))

purse_acfun_url = lambda inline, m, state: ("site_acfun_url", m.group(0))
purse_bili_av_url = lambda inline, m, state: ("site_bili_av_url", m.group(0))
purse_bili_bv_url = lambda inline, m, state: ("site_bili_bv_url", m.group(0))


def url_from_id(md: Markdown):
    md.inline.register("site_bili_av_url", BILI_AV_SITE_PATTERN, bili_video)
