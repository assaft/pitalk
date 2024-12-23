import json
from pathlib import Path
from uuid import uuid4
import shutil
import subprocess

from pitalk.user_api import FriendCard
from pitalk.user_api import User


class DropBoxAPI:

    DROPBOX_PATH = Path("dropbox")

    DROPBOX_USERS = DROPBOX_PATH / "users"
    DROPBOX_JOBS = DROPBOX_PATH / "jobs"

    # ADD_FRIEND_JOB = DROPBOX_JOBS / "add_friend"

    @staticmethod
    def is_connected() -> bool:
        pass

    def create_user(self, user_name: str):
        job_id = uuid4()
        job_file = self.DROPBOX_JOBS / f"{job_id}.json"
        job_desc = {
            "task": "create_user",
            "user_name": user_name
        }
        with open(job_file, "w") as f:
            json.dump(job_desc, f, indent=4)

    def add_friend(self, recipient: str, friend_card: FriendCard):
        friends_path = self.DROPBOX_JOBS / recipient / "friends"
        friend_card.export(friends_path)

    def send_message(self, recipient: str, file_path: Path):
        messages_path = self.DROPBOX_JOBS / recipient / "messages"
        shutil.copyfile(file_path, messages_path)

    def read_users(self):
