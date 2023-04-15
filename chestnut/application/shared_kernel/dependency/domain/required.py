import sys
from enum import Enum

from ....core.domain.value_object import ValueObject


class RequiredState(tuple, Enum, ValueObject):
    REQUIRED = ("Required",)
    REQUIRED_WHEN_INSTALL = ("Required", "Install")
    """Required when installation."""
    REQUIRED_WHEN_DEVELOP = ("Required", "Develop")
    """Required in development."""
    REQUIRED_BUT_NOT_UNIQUE = ("Required", "Type")
    """Requred, but only with type."""
    OPTIONAL = ("Optional",)
    OPTIONAL_APPEARANCE = ("Optional", "Appearance")
    OPTIONAL_PERFORMANCE = ("Optional", "Performance")
    OPTIONAL_FOR_DEVELOP = ("Optional", "Develop")
    """Optional to facilitate development."""
    OPTIONAL_IN_OTHER = ("Optional", "Other")
    USELESS = ("Useless",)

    def targetrequired(self) -> bool:
        return (
            self.value == RequiredState.REQUIRED
            or self.value == RequiredState.REQUIRED_WHEN_INSTALL
            or self.value == RequiredState.REQUIRED_WHEN_DEVELOP
            or self.value == RequiredState.REQUIRED_BUT_NOT_UNIQUE
        )

    def targetoptional(self) -> bool:
        return (
            self.value == RequiredState.OPTIONAL
            or self.value == RequiredState.OPTIONAL_APPEARANCE
            or self.value == RequiredState.OPTIONAL_PERFORMANCE
            or self.value == RequiredState.OPTIONAL_IN_OTHER
        )

    def targetuseless(self) -> bool:
        return self.value == RequiredState.USELESS


class InstallationOption(str, Enum):
    AutomaticInstallation = "AUTOMATIC"
    MannualInstallation = "MANNUAL"
