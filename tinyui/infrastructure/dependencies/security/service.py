import ecdsa
from pathlib import Path
from typing import Any, Dict, Iterable

from ...helpers.config import DepsConfig


def _config_validation(config: DepsConfig, assert_items: Iterable[str]) -> None:
    assert config.name in ["crypt", "encrypt", "crypto", "security"]

    for item in assert_items:
        assert item in config.values


def cryptfromconfig(config: DepsConfig) -> Dict[str, Any]:
    _config_validation(config, ["secret_key", "ecc_pubkey", "ecc_prikey"])

    crypto_dict = {
        "secret_key": None,
        "ecc": {"public": None, "private": None},
    }

    crypto_dict["secret_key"] = config.secret_key
    crypto_dict["ecc"]["public"] = ecdsa.VerifyingKey.from_pem(
        Path(config.ecc_pubkey).read_text()
    )
    crypto_dict["ecc"]["private"] = ecdsa.SigningKey.from_pem(
        Path(config.ecc_prikey).read_text()
    )

    return crypto_dict
