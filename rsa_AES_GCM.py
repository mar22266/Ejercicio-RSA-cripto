import os
import sys
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

from generar_claves import generar_par_claves


ClavePrivadaPassphrase = "lab04uvg"
EncabezadoPaquete = b"RSA1"
VersionPaquete = 1


# se cifra un documento con AES-GCM y se cifra la clave de AES con RSA-OAEP, luego se empaqueta todo en un formato
def encrypt_document(document: bytes, recipient_public_key_pem: bytes) -> bytes:
    if not isinstance(document, bytes):
        raise TypeError("document debe ser bytes")
    if not isinstance(recipient_public_key_pem, bytes):
        raise TypeError("recipient_public_key_pem debe ser bytes")

    LlaveAes = os.urandom(32)
    CifradorAes = AES.new(LlaveAes, AES.MODE_GCM)
    CifradoDocumento, TagAutenticacion = CifradorAes.encrypt_and_digest(document)
    LlavePublica = RSA.import_key(recipient_public_key_pem)
    CifradorRsa = PKCS1_OAEP.new(LlavePublica)
    LlaveAesCifrada = CifradorRsa.encrypt(LlaveAes)
    LongitudLlaveRsa = len(LlaveAesCifrada).to_bytes(2, "big")
    LongitudNonce = len(CifradorAes.nonce).to_bytes(1, "big")
    LongitudTag = len(TagAutenticacion).to_bytes(1, "big")
    LongitudCiphertext = len(CifradoDocumento).to_bytes(8, "big")

    # ayuda de gpt para crear un formato de paquete simple con encabezado, version, longitudes y datos
    Paquete = b"".join(
        [
            EncabezadoPaquete,
            VersionPaquete.to_bytes(1, "big"),
            LongitudLlaveRsa,
            LongitudNonce,
            LongitudTag,
            LongitudCiphertext,
            LlaveAesCifrada,
            CifradorAes.nonce,
            TagAutenticacion,
            CifradoDocumento,
        ]
    )

    return Paquete


# decfra el documento a partir del paquete extrayendo la clave de AES cifrada descifrandola con RSA
def decrypt_document(pkg: bytes, recipient_private_key_pem: bytes) -> bytes:
    if not isinstance(pkg, bytes):
        raise TypeError("pkg debe ser bytes")
    if not isinstance(recipient_private_key_pem, bytes):
        raise TypeError("recipient_private_key_pem debe ser bytes")
    if len(pkg) < 17:
        raise ValueError("Paquete demasiado corto")
    if pkg[:4] != EncabezadoPaquete:
        raise ValueError("Encabezado invalido")
    if pkg[4] != VersionPaquete:
        raise ValueError("Version de paquete no soportada")

    LongitudLlaveRsa = int.from_bytes(pkg[5:7], "big")
    LongitudNonce = pkg[7]
    LongitudTag = pkg[8]
    LongitudCiphertext = int.from_bytes(pkg[9:17], "big")
    PosicionActual = 17
    TamanoEsperado = (
        17 + LongitudLlaveRsa + LongitudNonce + LongitudTag + LongitudCiphertext
    )
    if len(pkg) != TamanoEsperado:
        raise ValueError("Tamano de paquete inconsistente")

    LlaveAesCifrada = pkg[PosicionActual : PosicionActual + LongitudLlaveRsa]
    PosicionActual += LongitudLlaveRsa
    Nonce = pkg[PosicionActual : PosicionActual + LongitudNonce]
    PosicionActual += LongitudNonce
    TagAutenticacion = pkg[PosicionActual : PosicionActual + LongitudTag]
    PosicionActual += LongitudTag
    CifradoDocumento = pkg[PosicionActual : PosicionActual + LongitudCiphertext]
    LlavePrivada = RSA.import_key(
        recipient_private_key_pem, passphrase=ClavePrivadaPassphrase
    )
    DescifradorRsa = PKCS1_OAEP.new(LlavePrivada)
    LlaveAes = DescifradorRsa.decrypt(LlaveAesCifrada)
    DescifradorAes = AES.new(LlaveAes, AES.MODE_GCM, nonce=Nonce)
    Documento = DescifradorAes.decrypt_and_verify(CifradoDocumento, TagAutenticacion)
    return Documento


# Prueba de cifrado y descifrado de un documento
if __name__ == "__main__":
    generar_par_claves(3072)

    with open("public_key.pem", "rb") as ArchivoPublico:
        pub = ArchivoPublico.read()
    with open("private_key.pem", "rb") as ArchivoPrivado:
        priv = ArchivoPrivado.read()

    # Genera un cifrado de un texto
    doc = b"Contrato de confidencialidad No. 2025-GT-001"
    pkg = encrypt_document(doc, pub)
    resultado = decrypt_document(pkg, priv)
    print(f"Documento original  : {doc}")
    print(f"Paquete cifrado     : {len(pkg)} bytes")
    print(f"Documento recuperado: {resultado}")

    # Prueba con archivo de 1 MB para simular un documento real
    doc_grande = os.urandom(1024 * 1024)
    pkg2 = encrypt_document(doc_grande, pub)
    assert decrypt_document(pkg2, priv) == doc_grande
    print("Archivo 1 MB: OK")
