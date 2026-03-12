import os
import sys
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

ClavePrivadaPassphrase = "lab04uvg"


# cifra con RSA usando OAEP
def cifrar_con_rsa(mensaje: bytes, public_key_pem: bytes) -> bytes:
    if not isinstance(mensaje, bytes):
        raise TypeError("mensaje debe ser bytes")
    if not isinstance(public_key_pem, bytes):
        raise TypeError("public_key_pem debe ser bytes")

    LlavePublica = RSA.import_key(public_key_pem)
    CifradorRsa = PKCS1_OAEP.new(LlavePublica)
    return CifradorRsa.encrypt(mensaje)


# descifra con RSA usando OAEP
def descifrar_con_rsa(cifrado: bytes, private_key_pem: bytes) -> bytes:
    if not isinstance(cifrado, bytes):
        raise TypeError("cifrado debe ser bytes")
    if not isinstance(private_key_pem, bytes):
        raise TypeError("private_key_pem debe ser bytes")

    LlavePrivada = RSA.import_key(private_key_pem, passphrase=ClavePrivadaPassphrase)
    DescifradorRsa = PKCS1_OAEP.new(LlavePrivada)
    return DescifradorRsa.decrypt(cifrado)


# cargar claves generadas en el ejercicio anterior
if __name__ == "__main__":
    with open("public_key.pem", "rb") as ArchivoPublico:
        pub = ArchivoPublico.read()
    with open("private_key.pem", "rb") as ArchivoPrivado:
        priv = ArchivoPrivado.read()

    mensaje_original = b"El mensaje sera la clave secreta de AES"
    cifrado = cifrar_con_rsa(mensaje_original, pub)
    descifrado = descifrar_con_rsa(cifrado, priv)

    print(f"Original  : {mensaje_original}")
    print(f"Cifrado   : {cifrado.hex()[:64]}...")
    print(f"Descifrado: {descifrado}")

    # lo que hace OAEP es usar aleatoriedad interna y por eso cambia el resultado
    c1 = cifrar_con_rsa(mensaje_original, pub)
    c2 = cifrar_con_rsa(mensaje_original, pub)
    print(f"\nc1 == c2: {c1 == c2}")
    print(f"c1: {c1.hex()[:64]}...")
    print(f"c2: {c2.hex()[:64]}...")
