try:
    import pygments  # type: ignore

    COLORFUL_CODE = True
except ImportError:
    COLORFUL_CODE = False


if not COLORFUL_CODE:

    def rendercode(
        source_code: str, lexer: str | None = None, linestart: int | None = None
    ) -> str:
        """Let code into HTML."""

        return r"<pre><code>" + source_code + r"</code></pre>"

else:
    from pygments import highlight
    from pygments.lexer import Lexer
    from pygments.lexers import get_lexer_by_name, guess_lexer

    from pygments.formatters.html import HtmlFormatter

    # Export function code_render.
    def rendercode(
        source_code: str, lexer: str | None = None, linestart: int | None = None
    ) -> str:
        """Let code into HTML."""

        if lexer:
            lexer_: Lexer = get_lexer_by_name(lexer, stripall=True)
        else:
            lexer_: Lexer = guess_lexer(source_code)

        if not linestart:
            line_args = {}
        else:
            line_args = dict(
                linenos="inline",
                linenostart=linestart,
            )
        formatter = HtmlFormatter(**line_args)  # type: ignore
        # formatter = SvgFormatter(**line_args, norwap=True)

        return highlight(source_code, lexer_, formatter)
