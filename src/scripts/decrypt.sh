# Дешифрует архив

KEY1="$1"
KEY2="$2"
INPUT="$3"

openssl enc -aes-256-cbc -d -pbkdf2 -pass "pass:${KEY1}:${KEY2}" -in "$INPUT" | tar xzf -
