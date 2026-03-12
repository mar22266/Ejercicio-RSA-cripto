import os
import sys
from Crypto.PublicKey import RSA


ClavePrivadaPassphrase = "lab04uvg"


# generra el par de claves verifcicando que sea mayor a 2048 bits
def generar_par_claves(bits: int = 3072):
    if bits < 2048:
        raise ValueError("RSA requiere al menos 2048 bits")

    ParClaves = RSA.generate(bits)
    ClavePrivadaPem = ParClaves.export_key(
        format="PEM",
        passphrase=ClavePrivadaPassphrase,
        pkcs=8,
        protection="PBKDF2WithHMAC-SHA512AndAES256-CBC",
    )
    ClavePublicaPem = ParClaves.publickey().export_key(format="PEM")

    with open("private_key.pem", "wb") as ArchivoPrivado:
        ArchivoPrivado.write(ClavePrivadaPem)
    with open("public_key.pem", "wb") as ArchivoPublico:
        ArchivoPublico.write(ClavePublicaPem)
    return ClavePrivadaPem, ClavePublicaPem


if __name__ == "__main__":
    generar_par_claves(3072)
    print("Claves generadas: private_key.pem y public_key.pem")
