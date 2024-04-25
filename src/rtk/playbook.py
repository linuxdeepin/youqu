from src.read_toml import read_toml
from setting import conf
from src.rtk.remote_runner import RemoteRunner
from src.rtk.local_runner import LocalRunner


class PlayBook():

    def __init__(self):
        ts = read_toml(f"{conf.ROOT_DIR}/playbook.toml")

        conf_repos = ts.get("repositories")
        # for conf_repo in conf_repos:
        #     self.url = conf_repo.get("url")
        #     self.branch_or_tag = conf_repo.get("branch_or_tag")
        #     self.depth = conf_repo.get("depth")
        #     self.path_to = conf_repo.get("path_to")
        #     self.user = conf_repo.get("user")
        #     self.password = conf_repo.get("password")

        conf_play = ts.get("play")
        self.execution_mode = conf_play.get("execution_mode")
        if self.execution_mode not in ["run", "remote"]:
            raise ValueError
        self.clients = conf_play.get("clients")
        self.slaves = conf_play.get("slaves")
        self.keywords = conf_play.get("keywords")
        self.tags = conf_play.get("tags")
        self.pms_case_file_path = conf_play.get("pms_case_file_path")

    def playbook(self):
        if self.execution_mode == "remote":
            runner = RemoteRunner()
        else:
            runner = LocalRunner()