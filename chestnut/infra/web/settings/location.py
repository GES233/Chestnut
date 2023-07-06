"""Locate config."""


CONFIG_LOCATION = dict(
    app_config="APP",  # AppConfig
    sse_message="MESSAGE",  # DepsConfig
    database="database".upper(),  # DepsConfig
    security="security".upper(),  # DepsConfig
)  # type: ignore
"""
Config location related to Sanic Config.

e.g.
```python
app.config.update({CONFIG_LOCATION["app_config"]: app_config})
```
"""


REQUEST_CONTEXT_LOCATION = dict(
    app_config="app_config",
    page_config="page_config",
)
