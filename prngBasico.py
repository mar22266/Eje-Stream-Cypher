# imprtacion librerria de hashing
import hashlib


# funcion para crear un estado inicial a partir de una semilla
def crearEstadoInicial(seed: str) -> int:
    digest = hashlib.sha256(seed.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") & 0xFFFFFFFF


# funcion para generar el siguiente numero pseudoaleatorio a partir del estado actual
# hex de 32 bits elegido para el laboratrio
# LCG X(n+1) = (a * X_n + c) mod 2^32 por eso se hace esa func
# c debe ser impar y dentro de 32 bits, a debe dejar residuo 1 al dividirse entre 4
def siguienteU32(estadoActual: int) -> int:
    return (1234565 * estadoActual + 1000000003) & 0xFFFFFFFF


# generadora de bytes pseudoaleatorios a partir de una semilla y una longitud deseada
def generarBytes(seed: str, longitud: int) -> bytes:
    estado = crearEstadoInicial(seed)
    salida = bytearray()
    while len(salida) < longitud:
        estado = siguienteU32(estado)
        salida.extend(estado.to_bytes(4, "big"))
    return bytes(salida[:longitud])


# funcion principal para generar un keystream pseudoaleatorio a partir de una semilla y una longitud
def generarKeystream(seed: str, longitud: int) -> bytes:
    if longitud < 0:
        raise ValueError("longitud invalida")
    return generarBytes(seed, longitud)
