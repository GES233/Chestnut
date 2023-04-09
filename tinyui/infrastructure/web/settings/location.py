"""Locate config."""


CONFIG_LOCATION = dict(
    app_config="APP",  # type: AppConfig
    sse_message="MESSAGE",  # type: DepsConfig
    database="database".upper(),  # type: DepsConfig
    security="security".upper(),  # type: DepsConfig
)
"""Config location related to Sanic Config."""


REQUEST_CONTEXT_LOCATION = dict(
    app_config="app_config",
    page_config="page_config",
)
