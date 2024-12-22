from __future__ import annotations

import base64
import os
from pathlib import Path

import rsa
from pydantic import BaseModel
from rsa import PrivateKey


class FriendCard(BaseModel):
    short_name: str
    full_name: str
    public_key: bytes
    announce_data: bytes


class User:

    USERS_PATH = Path("users")

    def __init__(self, short_name: str | None = None):
        if not short_name:
            assert len(users := os.listdir(self.USERS_PATH)) == 1
            short_name = users[0]
        self.short_name = short_name
        user_path = self.USERS_PATH / short_name
        keys_path = user_path / "keys"
        friend_card_path = user_path / "friend_card"
        friends_path = user_path / "friends"

        # load the friend card
        with open(friend_card_path / f"{short_name}.json", "r") as f:
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
    def create_user(cls, short_name: str, full_name: str, announce_path: Path):
        user_path = cls.USERS_PATH / short_name
        keys_path = user_path / "keys"
        friend_card_path = user_path / "friend_card"
        friends_path = user_path / "friends"

        os.makedirs(cls.USERS_PATH, exist_ok=True)
        os.makedirs(user_path, exist_ok=False)
        os.makedirs(keys_path)
        os.makedirs(friend_card_path)
        os.makedirs(friends_path)

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
        friend_card = FriendCard(short_name=short_name,
                                 full_name=full_name,
                                 public_key=public_key.save_pkcs1(),
                                 announce_data=announce_data)

        with open(friend_card_path / f"{short_name}.json", "wt") as f:
            f.write(friend_card.model_dump_json(indent=4))

    def add_friend(self, friend_card: FriendCard):
        assert friend_card.short_name not in [f.short_name for f in self.friend_list]
        friends_path = self.USERS_PATH / self.short_name / "friends"
        friend_path = friends_path / f"{friend_card.short_name}.json"
        with open(friend_path, "wt") as f:
            f.write(friend_card.model_dump_json(indent=4))
        self.friend_list.append(friend_card)

    def get_friend_card(self):
        return self.friend_card

    @classmethod
    def make_friends(cls, short_name1: str, short_name2: str):
        user1 = User(short_name1)
        user2 = User(short_name2)
        user1.add_friend(user2.friend_card)
        user2.add_friend(user1.friend_card)
