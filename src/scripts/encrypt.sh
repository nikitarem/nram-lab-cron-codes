# Щифрует stdin в stdout через openssl

KEY1="$1"
KEY2="$2"

openssl enc -aes-256-cbc -salt -pbkdf2 -pass "pass:${KEY1}:${KEY2}"