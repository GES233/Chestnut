# TODO: Change this into a RequredItem/PrerequisiteItem.
import subprocess

from .path import WEB_DIR_PATH
from ....helpers.config.app import AppConfig


def getbuildstatus(config: AppConfig) -> bool:
    return config.build


def checknodeenv() -> bool:
    try:
        subprocess.run("node -v")
    except subprocess.SubprocessError:
        return False
    else:
        return True


def buildwebapp() -> None:
    subprocess.run(f"cd {WEB_DIR_PATH} && npm run build", shell=True)


def webapp(config: AppConfig) -> None:
    if not getbuildstatus(config):
        public_exist = WEB_DIR_PATH.touch()
        if not public_exist:
            node_env = checknodeenv()
            if not node_env:
                ...
            else:
                buildwebapp()
    else:
        if WEB_DIR_PATH.exists():
            import shutil

            shutil.rmtree(WEB_DIR_PATH)

        buildwebapp()
