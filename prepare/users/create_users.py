from pathlib import Path

from pitalk.user_api import User

announce_path = Path("prepare") / "users" / "announcements"

nelly_t = User.create_user(
    short_name="nelly_t", full_name="Nelly Toledo",
    announce_path=announce_path / "nelly_t.wav")

zoey_t = User.create_user(
    short_name="zoey_t", full_name="Zoey Toledo",
    announce_path=announce_path / "zoey_t.wav")

alma_by = User.create_user(
    short_name="alma_by", full_name="Alma Basson-Yovel",
    announce_path=announce_path / "alma_by.wav")

gili_b = User.create_user(
    short_name="gili_b", full_name="Gili Basson",
    announce_path=announce_path / "gili_b.wav")

User.make_friends("nelly_t", "zoey_t")
User.make_friends("nelly_t", "alma_by")
User.make_friends("zoey_t", "gili_b")
