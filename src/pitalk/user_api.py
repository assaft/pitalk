from __future__ import annotations

import base64
import os
from pathlib import Path

import rsa
from pydantic import BaseModel, Base64Bytes
from rsa import PrivateKey


class FriendCard(BaseModel):
    user_name: str
    full_name: str
    public_key: bytes
    announce_data: Base64Bytes

    def export(self, path: Path):
        with open(path / f"{self.user_name}.json", "wt") as f:
            f.write(self.model_dump_json(indent=4))


class User:

    PITALK_USER_PATH = Path("/home/.pitalk/")

    def __init__(self, user_name: str | None = None):
        if not user_name:
            assert len(users := os.listdir(self.PITALK_USER_PATH)) == 1
            user_name = users[0]
        self.user_name = user_name
        user_path = self.PITALK_USER_PATH / user_name
        keys_path = user_path / "keys"
        card_path = user_path / "card"
        friends_path = user_path / "friends"

        # load the friend card
        with open(card_path / f"{user_name}.json", "r") as f:
            self.friend_card = FriendCard.model_validate_json(f.read())

        # load the private key
        with open(keys_path / "rsa.key", "rb") as f:
            self.private_key = PrivateKey.load_pkcs1(f.read())

        # load the friends list
        self.friend_list = []
        for f in os.listdir(friends_path):
            with open(friends_path / f, "rt") as fp:
                self.friend_list.append(FriendCard.model_validate_json(fp.read()))

    @classmethod
    def create_user(cls, user_name: str, full_name: str, announce_path: Path):
        user_path = cls.PITALK_USER_PATH / user_name
        keys_path = user_path / "keys"
        card_path = user_path / "card"

        os.makedirs(cls.PITALK_USER_PATH, exist_ok=True)
        os.makedirs(user_path, exist_ok=False)
        os.makedirs(keys_path)
        os.makedirs(card_path)

        # create and save keys
        public_key, private_key = rsa.newkeys(512)
        with open(keys_path / "rsa.key", "wb") as f1, \
             open(keys_path / "rsa_public.key", "wb") as f2:
            f1.write(private_key.save_pkcs1())
            f2.write(public_key.save_pkcs1())

        # load the announcement sound file
        with open(announce_path, "rb") as f:
            announce_data = f.read()
            announce_data = base64.b64encode(announce_data)

        # create and save a friend card
        friend_card = FriendCard(user_name=user_name,
                                 full_name=full_name,
                                 public_key=public_key.save_pkcs1(),
                                 announce_data=announce_data)
        friend_card.export(card_path)

    def add_friend(self, friend_card: FriendCard):
        assert friend_card.user_name not in [f.user_name for f in self.friend_list]
        friend_card.export(self.PITALK_USER_PATH / self.user_name / "friends")
        self.friend_list.append(friend_card)

    def get_friend_card(self):
        return self.friend_card

    @classmethod
    def make_friends(cls, user_name1: str, user_name2: str):
        user1 = User(user_name1)
        user2 = User(user_name2)
        user1.add_friend(user2.friend_card)
        user2.add_friend(user1.friend_card)
