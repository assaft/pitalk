import os
import re

from pitalk import user_api


def main():
    regex_patten = r"^[a-zA-Z0-9_]*$"
    usernane_regex = re.compile(regex_patten)

    user_name = input("Enter the user name (e.g. john_smith): ")

    if not usernane_regex.match(user_name):
        print(f"User name does not match the regex {regex_patten}")
        exit(1)

    full_name = input("Enter the full name (e.g. John Smith): ")

    announce_path = input("Enter the path to the announcement file: ")

    if not os.path.exists(announce_path):
        print(f"File not found: {announce_path}")
        exit(1)

    if not announce_path.endswith(".wav"):
        print(f"File is not a .wav file: {announce_path}")
        exit(1)
        
    print("Creating user...")

    user = user_api.create_user(
        user_name=user_name, full_name=full_name,
        announce_path=announce_path)


if __name__ == '__main__':
    main()
