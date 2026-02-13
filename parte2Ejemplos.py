# importan archivo
from streamCipher import *
from prngBasico import generarKeystream


# eje 2.1 ejemplo
def inciso21VariacionClave() -> None:
    mensaje = "hola me gusta comer"
    claveA = "claveA"
    claveB = "claveB"
    cipherA = cifrar(mensaje, claveA)
    cipherB = cifrar(mensaje, claveB)

    print("2.1 variacion de la clave")
    print("mensaje:", mensaje)
    print("clave a:", claveA)
    print("cipher a (hex):", cipherA.hex())
    print("clave b:", claveB)
    print("cipher b (hex):", cipherB.hex())
    print("son diferentes:", cipherA != cipherB)

    # verificacion rapida de que cada clave recupera el mensaje correctamente
    planoA = descifrar(cipherA, claveA)
    planoB = descifrar(cipherB, claveB)
    print("descifrado con clave a:", planoA)
    print("descifrado con clave b:", planoB)

    # descifrar con clave equivocada no recupera el mensaje
    try:
        planoIncorrecto = descifrar(cipherA, claveB)
        print("descifrado con clave equivocada:", planoIncorrecto)
    except Exception as e:
        print("descifrado con clave equivocada fallo:", str(e))


# eje 2.2 ejemplo
def inciso22ReutilizacionKeystream() -> None:
    clave = "password1"

    # misma longitud para poder hacer xor entre ambos ciphertext
    mensaje1 = "hola me llamo andre"
    mensaje2 = "pera la comio sofia"
    cipher1 = cifrar(mensaje1, clave)
    cipher2 = cifrar(mensaje2, clave)

    # a la hora de interceptar ambos ciphertext puede hacer c1 xor c2
    cipher1XorCipher2 = xorBytes(cipher1, cipher2)

    # esto es lo mismo que plain text 1 xor plain text 2 porque el keystream se cancela
    tPlano1XortPlano2 = xorBytes(mensaje1.encode("utf-8"), mensaje2.encode("utf-8"))

    print("2.2 reutilizacion del keystream")
    print("clave:", clave)
    print("mensaje 1:", mensaje1)
    print("mensaje 2:", mensaje2)
    print("cipher 1 (hex):", cipher1.hex())
    print("cipher 2 (hex):", cipher2.hex())
    print("c1 xor c2 (hex):", cipher1XorCipher2.hex())
    print("p1 xor p2 (hex):", tPlano1XortPlano2.hex())
    print("coinciden:", cipher1XorCipher2 == tPlano1XortPlano2)


# eje 2.3 ejemplo
def inciso23LongitudKeystream() -> None:
    clave = "estaesunaprueba"
    mensaje = "me gusta ver futbol los domingos"
    mensajeBytes = mensaje.encode("utf-8")

    print("2.3 longitud del keystream")
    print("clave:", clave)
    print("mensaje:", mensaje)
    print("longitud mensaje (bytes):", len(mensajeBytes))

    # keystream del mismo tamano que el mensaje
    ksIgual = generarKeystream(clave, len(mensajeBytes))
    cipherIgual = xorBytes(mensajeBytes, ksIgual)

    print("\ncaso 1 keystream igual al mensaje")
    print("longitud keystream:", len(ksIgual))
    print("cipher (hex):", cipherIgual.hex())
    print("por lo queno hay repeticion interna del keystream")

    # keystream mas corto que el mensaje y repetido para cubrirlo
    ksCorto = generarKeystream(clave, 8)
    ksRepetido = (ksCorto * ((len(mensajeBytes) // len(ksCorto)) + 1))[
        : len(mensajeBytes)
    ]
    cipherRepetido = xorBytes(mensajeBytes, ksRepetido)

    print("\ncaso 2 keystream corto y repetido")
    print("longitud keystream corto:", len(ksCorto))
    print("keystream repetido (hex):", ksRepetido.hex())
    print("cipher (hex):", cipherRepetido.hex())
    print("por lo tanto la repeticion da patrones y no es seguro")

    # keystream mas largo que el mensaje pero se corta al tamano necesario
    ksLargo = generarKeystream(clave, len(mensajeBytes) + 16)
    ksTruncado = ksLargo[: len(mensajeBytes)]
    cipherTruncado = xorBytes(mensajeBytes, ksTruncado)

    print("\ncaso 3 keystream largo y cortado")
    print("longitud keystream largo:", len(ksLargo))
    print("longitud keystream truncado:", len(ksTruncado))
    print("cipher (hex):", cipherTruncado.hex())
    print("evita la repeticion pero igual no es tan seguro")


# entrada llamda de ejemplols
if __name__ == "__main__":
    print("-" * 40 + "\n")
    inciso21VariacionClave()
    print("-" * 40 + "\n")
    inciso22ReutilizacionKeystream()
    print("-" * 40 + "\n")
    inciso23LongitudKeystream()
    print("-" * 40 + "\n")
