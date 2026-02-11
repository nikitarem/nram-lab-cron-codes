# Щифрует stdin в stdout через openssl

KEY_FILE="$1"
FILENAME="$2"

openssl pkeyutl -encrypt -pubin -inkey ${KEY_FILE} -in ${FILENAME} -out ${FILENAME}.enc
