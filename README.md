# Ejercicio - RSA, OAEP

## Descripcion

Lo que se hace en el ejercicio es usar RSA en un caso real. Incluye la generacion de claves, el cifrado y descifrado con RSA-OAEP, y tambien el uso de cifrado hibrido, donde RSA protege una clave AES y AES-GCM se encarga de cifrar el documento de forma mas rapida y segura.

** Se sube el archivo de la llave privada para demostrar el fin del ejercicio, tomando en cuenta que es una mala practica y no debe de subirse en la practica real**

## Requisitos previos

- Windows con Python instalado y accesible desde terminal.
- `pip` disponible.
- Libreria `pycryptodome`.

## Instalacion

1. Abrir una terminal en la ruta del proyecto:

```powershell
cd C:\Users\andre\EJERCICIO-RSA\Ejercicio-RSA-cripto
```

2. Instalar la dependencia pedida por el laboratorio:

```powershell
python -m pip install pycryptodome
```

## Estructura de archivos

- `generar_claves.py`: genera el par de claves RSA en formato PEM.
- `rsa_OAEP.py`: hace cifrado y descifrado directo con RSA y OAEP.
- `rsa_AES_GCM.py`: implementa el cifrado hibrido con RSA-OAEP + AES-256-GCM.
- `README.md`: documentacion del laboratorio.
- `private_key.pem`: clave privada protegida con passphrase `lab04uvg`.
- `public_key.pem`: clave publica del receptor.

## ejecucion paso a paso

1. Generar las llaves RSA:

```powershell
python generar_claves.py
```

Esto genera:

- `private_key.pem` protegida con la passphrase `lab04uvg`
- `public_key.pem`

2. Probar el cifrado y descifrado directo con RSA-OAEP:

```powershell
python rsa_OAEP.py
```

3. Probar el cifrado hibrido con documento corto y documento de 1 MB:

```powershell
python rsa_AES_GCM.py
```

## Ejemplos de ejecucion

### `python generar_claves.py`

```text
Claves generadas: private_key.pem y public_key.pem
```

### `python rsa_OAEP.py`

```text
Original  : b'El mensaje sera la clave secreta de AES'
Cifrado   : 591159c7ce25036ab2f89fd9addd6d856231895c1c5b925a8b984e7e3c872592...
Descifrado: b'El mensaje sera la clave secreta de AES'

c1 == c2: False
c1: c5a3f79d75f56452c85b2de2413950b6c27bc6975d4131a3667c2465d777b96e...
c2: 505975231fea8923e5c51c1db2e179172fa79f99caa9c9715c4ec92e67bf67cf...
```

### `python rsa_AES_GCM.py`

```text
Documento original  : b'Contrato de confidencialidad No. 2025-GT-001'
Paquete cifrado     : 477 bytes
Documento recuperado: b'Contrato de confidencialidad No. 2025-GT-001'
Archivo 1 MB: OK
```

## Respuestas a las preguntas

### Pregunta 1

¿Explique por que no cifrar el documento directamente con RSA?

No conviene cifrar el documento completo directamente con RSA por varias razones. La primera es que RSA es mucho mas lento que un cifrado simetrico, asi que para archivos medianos o grandes seria ineficiente y se necesitaria mucho costo computacional. La segunda es que RSA solo puede cifrar bloques pequeños, con OAEP el mensaje debe ser bastante menor que el tamano de la clave, y lo que llega a pasar es que un documento real no quepa de forma natural en una sola operacion de RSA.

Por eso el enfoque correcto es usar cifrado hibrido. RSA se usa para proteger una clave AES aleatoria, y AES-GCM se usa para cifrar el documento real. Asi el sistema, puede manejar archivos grandes y ademas conserva confidencialidad y su integridad.

### Pregunta 2

¿Qué información contiene un archivo .pem? Abre public_key.pem con un editor de texto y describe su estructura.

Un archivo `.pem` contiene datos criptograficos codificados en Base64 y rodeados por cabeceras de texto legibles. En este laboratorio, `public_key.pem` guarda la clave publica RSA exportada en formato PEM.

Al abrir `public_key.pem` se observa esta estructura:

- Una linea inicial: `-----BEGIN PUBLIC KEY-----`
- Varias lineas con texto Base64
- Una linea final: `-----END PUBLIC KEY-----`

El archivo generado en el lab quedo con esa forma exacta. El contenido del centro no es texto comun, sino la representacion codificada de la clave publica. Ese bloque tiene la info necesaria para reconstruir la clave, como el modulo y el exponente publico, pero empaquetados en una estructura binaria estandar y luego convertidos a Base64 para poder guardarlos como texto.

Tambien se nota una diferencia con la clave privada porque en `private_key.pem` aparece `-----BEGIN ENCRYPTED PRIVATE KEY-----`, lo cual indica que la clave privada si quedo protegida con la passphrase `lab04uvg`, tal como pedia el laboratorio.

### Pregunta 3

¿Porqué cifrar el mismo mensaje dos veces produce resultados distintos? Demuéstrenlo y expliquen que propiedad de OAEP lo cause

La demostracion esta en la salida del script `rsa_OAEP.py`, donde se hacen dos cifrados del mismo mensaje:

```text
c1 == c2: False
```

Eso confirma que el mensaje original era exactamente el mismo, pero los dos cifrados fueron distintos. La razon es que OAEP no es un padding determinista. Cada vez que cifra, incorpora aleatoriedad interna por medio de una semilla aleatoria. Esa semilla cambia el bloque final que entra a RSA, asi que el resultado cifrado tambien cambia.

## Referencias

- Buchanan, W. J. (2022, abril 18). So how does padding work in RSA? Basically, PKCS#v1.5 is bad, OAEP is good. Medium. https://medium.com/asecuritysite-when-bob-met-alice/so-how-does-padding-work-in-rsa-6b34a123ca1f

- DataSunrise, Inc. (2026). Archivos PEM: Importancia de los datos criptográficos. DataSunrise. https://www.datasunrise.com/es/centro-de-conocimiento/archivos-pem/

- mee. (2023, febrero 12). Can someone please explain RSA-OAEP in plain English mathematically? Cryptography Stack Exchange. https://crypto.stackexchange.com/questions/104191/can-someone-please-explain-rsa-oaep-in-plain-english-mathematically

- Ojha, S. (2025, junio 13). Secure your Flutter apps with AES-GCM and RSA encryption (hybrid encryption guide). Medium. https://medium.com/@ojhasahil9/secure-your-flutter-app-with-aes-gcm-and-rsa-encryption-hybrid-encryption-guide-0293d899b4d0

- OpenAI. (2036). ChatGPT OpenAI
