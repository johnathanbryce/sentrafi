from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()


def hash_password(plain_pword: str) -> str:
    hashed_password = password_hash.hash(plain_pword)
    print(f"HASHED PWORD: {hashed_password}")
    return hashed_password


def verify_password(plain_pword: str, hashed: str) -> bool:
    is_valid_pword = password_hash.verify(plain_pword, hashed)

    if is_valid_pword:
        print("VALID PASSWORD")
        return True
    else:
        print("INVALID PASSWORD")
        return False
