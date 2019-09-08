# -*- coding: utf-8 -*-
from passlib.hash import bcrypt


def encrypt_pass(pwd: str) -> str:
    hashed_pwd = bcrypt.using(rounds=13).hash(pwd)
    return hashed_pwd


def verify_pass(pwd: str, crypt_pwd: str) -> bool:
    result = bcrypt.verify(pwd, crypt_pwd)
    return result


# def main():
#     password = "toast"
#     hashed_pwd = encrypt_pass(password)
#     print(hashed_pwd)
#     check_pwd = verify_pass(password, hashed_pwd)
#     print(check_pwd)
#     bad_pwd = "Toast"
#     check_pwd = verify_pass(bad_pwd, hashed_pwd)
#     print(check_pwd)


# if __name__ == "__main__":
#     main()
