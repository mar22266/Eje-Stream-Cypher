# importacion de la lib de base65 y la funcion de cifrar y descifrar del streamCipher
import base64
from streamCipher import cifrar, descifrar


# funcion para convertir bytes a hex
def aHex(data: bytes) -> str:
    return data.hex()


# convierte bytes a base64
def aBase64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


# funcion de demo del programa para mostrar el mensaje, la clave, el cipher en hex y base64, y el mensaje descifrado
def demo(mensaje: str, clave: str) -> None:
    tCipher = cifrar(mensaje, clave)
    tPlano = descifrar(tCipher, clave)

    # alerta de error
    if tPlano != mensaje:
        raise AssertionError("el decifrado no coincide con el mensaje original")

    print("mensaje:", mensaje)
    print("clave:", clave)
    print("cipher hex:", aHex(tCipher))
    print("cipher base64:", aBase64(tCipher))
    print("descifrado:", tPlano)
    print("-" * 40)


# entrada principal con ejemplos
if __name__ == "__main__":
    demo("hola me llamo andre", "clave1")
    demo("me gusta jugar futbol", "realmadrid")
    demo("cifrando este mensaje", "cifrados26")
