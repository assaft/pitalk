import json
import os
from pathlib import Path
from uuid import uuid4
import shutil
import subprocess

# from pitalk.user_api import FriendCard
# from pitalk.user_api import User


class DropBoxAPI:

    PITALK_PATH = Path(os.environ["PITALK_HOME"])
    DROPBOX_PATH = Path(os.environ["DROPBOX_HOME"])
    DROPBOX_UPLOADER_PATH = Path(os.environ["DROPBOX_UPLOADER_HOME"])

    DROPBOX_USERS_DIR = Path("users")

    DROPBOX_USERS_LOCAL = DROPBOX_PATH / DROPBOX_USERS_DIR
    DROPBOX_USERS_REMOTE = DROPBOX_USERS_DIR

    DROPBOX_JOBS_LOCAL = DROPBOX_PATH / "jobs"

    DROPBOX_UPLOADER_SCRIPT = DROPBOX_UPLOADER_PATH / "dropbox_uploader.sh"

    # ADD_FRIEND_JOB = DROPBOX_JOBS / "add_friend"

    @staticmethod
    def is_connected() -> bool:
        pass

    def create_users(self):
        print("before create users")
        result = subprocess.run([self.DROPBOX_UPLOADER_SCRIPT,
                                 'mkdir', self.DROPBOX_USERS_DIR], 
                                 cwd=self.PITALK_PATH, stdout=subprocess.PIPE)
        print("after create users")
        print(result.stdout.decode('utf-8'))
  

    def upload_user(self, card_path: Path, user_name: str):
        print("before upload")
        source_path = card_path
        target_path = self.DROPBOX_USERS_DIR / user_name
        result = subprocess.run([self.DROPBOX_UPLOADER_SCRIPT,
                                 'upload', source_path, target_path], 
                                cwd=self.PITALK_PATH, 
                                stdout=subprocess.PIPE)
        print("after upload")
        print(result.stdout.decode('utf-8'))

    def download_user(self, user_name:str) -> Path:
        print("before download")
        source_path = self.DROPBOX_USERS_DIR / user_name
        target_path = self.DROPBOX_PATH / self.DROPBOX_USERS_DIR / user_name
        result = subprocess.run([self.DROPBOX_UPLOADER_SCRIPT,
                                 'download', source_path, target_path], 
                                 cwd=self.PITALK_PATH, stdout=subprocess.PIPE)
        print("after download")
        print(result.stdout.decode('utf-8'))
        return target_path

    def create_user(self, user_name: str):
        job_id = uuid4()
        job_file = self.DROPBOX_JOBS / f"{job_id}.json"
        job_desc = {
            "task": "create_user",
            "user_name": user_name
        }
        with open(job_file, "w") as f:
            json.dump(job_desc, f, indent=4)

    # def add_friend(self, recipient: str, friend_card: FriendCard):
    #     friends_path = self.DROPBOX_JOBS / recipient / "friends"
    #     friend_card.export(friends_path)

    # def send_message(self, recipient: str, file_path: Path):
    #     messages_path = self.DROPBOX_JOBS / recipient / "messages"
    #     shutil.copyfile(file_path, messages_path)

    # def read_users(self):
    #     result = subprocess.run(['./dropbox-uploader.sh', 'download', 'users'],
    #                             cwd='~', 
    #                             stdout=subprocess.PIPE)
    #     print(result.stdout.decode('utf-8'))
