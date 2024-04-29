from enum import Enum
from enum import unique


@unique
class SubCmd(Enum):
    run = "run"
    remote = "remote"
    playbook = "playbook"
    pmsctl = "pmsctl"
    csvctl = "csvctl"
    startapp = "startapp"
    git = "git"
