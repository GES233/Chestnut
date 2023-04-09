from ..link import APP_LINK


class AppConfig:
    """AppConfig with an `APP_` prefix default."""

    name: str
    """Application's name."""
    introduction: str
    """Introduction of your app."""
    description: str | None
    """FULL introduction of app."""
    website: str | None
    """Link for app."""
    installed: bool
    """Boolean. It will be `True` if app is installed."""
    use_https: bool
    """ Return `True` if app use HTTPS(HTTPS related and TLS always in instance).
        
        Set `False` if use Ngnix.
    """
    lang: str
    """App's language."""
    build: bool
    """ Compile front-end or not.
    
        - If `build` is True => delete `public/webapp` if exist and execute `npm run build` in command.
          - solve -> install node
        - If `build` is False => Check `public/webapp` existed:
          - if exist => execute next step;
          - if not exist => Try to execute `npm run build` in command and sent a warning.
          - solve -> contact to developer
    """

    __slots__ = (
        "name",
        "installed",
        "use_https",
        "introduction",
        "description",
        "lang",
        "build",
        "website",
        # "__dict__",
    )

    def __init__(
        self,
        name: str,
        introduction: str,
        installed: bool,
    ) -> None:
        """If you want to disable instance, don't forget to set here."""
        self.name = name
        self.introduction = introduction
        self.installed = installed
        self.use_https = False
        self.description = None
        self.lang = "cmn-Hans"
        self.build = True
        self.website = APP_LINK

    def push(self, upper: bool = True, app_prefix: str = "APP_") -> dict:
        cfg = {}

        for item in self.__slots__:
            cfg[app_prefix + item.upper() if upper else item] = object.__getattribute__(
                self, item
            )

        return cfg

    def load(self, config_dict: dict) -> None:
        for item in config_dict:
            self.__setattr__(item, config_dict[item])
