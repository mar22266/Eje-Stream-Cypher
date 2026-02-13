# se improta la funcion de generar keystream del prngBasico
from prngBasico import generarKeystream


# funcion para hacer xor entre dos bytes
def xorBytes(a: bytes, b: bytes) -> bytes:
    if len(a) != len(b):
        raise ValueError("longitudes distintas")
    return bytes(x ^ y for x, y in zip(a, b))


# funciones para cifrar y descifrar con xor entre el mensaje y el keystream generado
def cifrar(mensaje: str, clave: str) -> bytes:
    mensajeBytes = mensaje.encode("utf-8")
    keystream = generarKeystream(clave, len(mensajeBytes))
    return xorBytes(mensajeBytes, keystream)


# funcion para descifrar usando xor entre ciphertext y keystream
def descifrar(ciphertext: bytes, clave: str) -> str:
    keystream = generarKeystream(clave, len(ciphertext))
    mensajeBytes = xorBytes(ciphertext, keystream)
    return mensajeBytes.decode("utf-8", errors="strict")
