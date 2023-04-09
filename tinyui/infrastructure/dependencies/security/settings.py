import os
from pathlib import Path
from typing import Tuple

try:
    import ecdsa  # type: ignore

    security_enable = True
except (ModuleNotFoundError, ImportError):
    security_enable = False

from ...helpers.config import DepsConfig


security_dev = DepsConfig(
    "security",
    security_enable,
    {
        "secret_key": "ViqV0Nx1U6HksReMYyIcb4azdqA1gQA9ejeH9kcAMHw=",
        "ecc_prikey": Path(Path(__file__).parent / "eckey.pem"),
        "ecc_pubkey": Path(Path(__file__).parent / "ecpubkey.pem"),
    },
)


security_test = DepsConfig(
    "security",
    security_enable,
    {
        "secret_key": "8eU8o5uGAq1on3f5S6f1R/TXDpc2JEP5QppeKoRiCes=",
        "ecc_prikey": Path(Path(__file__).parent / "eckey.pem"),
        "ecc_pubkey": Path(Path(__file__).parent / "ecpubkey.pem"),
    },
)


security_prod = DepsConfig(
    "security",
    security_enable,
    {
        "secret_key": "YT3Y4CEQHL0xHXAdbO4l5bAFOEdliJhDR+MjAHUWluQ=",
        "ecc_prikey": None,
        "ecc_pubkey": None,
    },
)


def generatekeyfile(path: Path) -> Tuple[Path, Path]:
    sk = ecdsa.SigningKey.generate(ecdsa.NIST256p)

    eckey = sk.to_pem()
    sk_path = Path(path / "eckey.pem")
    if not sk_path.exists():
        sk_path.touch()
        sk_path.write_bytes(eckey)

    vk: ecdsa.VerifyingKey = sk.verifying_key  # type: ignore
    ecpubkey = vk.to_pem()
    pk_path = Path(path / "ecpubkey.pem")
    if not pk_path.exists():
        pk_path.touch()
        pk_path.write_bytes(ecpubkey)

    return (sk_path, pk_path)


def set_security_inst_setting(path: Path) -> DepsConfig:
    if not security_enable:
        return DepsConfig("security")

    # Secret key
    secret_key = os.popen("openssl rand -base64 32").readline().strip("\n")

    # Paths
    sk, pk = generatekeyfile(path)

    return DepsConfig(
        "security",
        True,
        {
            "secret_key": secret_key,
            "ecc_prikey": sk,
            "ecc_pubkey": pk,
        },
    )
