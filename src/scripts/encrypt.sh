# Щифрует stdin в stdout через openssl

KEY="$1"

openssl pkeyutl -encrypt -pubin -inkey ${KEY} -in data.txt -out data.enc
