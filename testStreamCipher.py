# import de lib para unit testing
import unittest

# importar funciones a testear
from streamCipher import cifrar, descifrar
from prngBasico import generarKeystream


# clase de test para el streancipher
class TestStreamCipher(unittest.TestCase):
    # verifica mismo texto de entrada y salida
    def testCifraYDescifra(self):
        mensaje = "prubea numero 1"
        clave = "password"
        tCipher = cifrar(mensaje, clave)
        tPlano = descifrar(tCipher, clave)
        self.assertEqual(tPlano, mensaje)

    # la misma entrada con claves distintas no debe producir el mismo cifrado
    def testClavesDistintas(self):
        mensaje = "esta seria la prueba 2 de mi eje"
        tCipher1 = cifrar(mensaje, "pass1")
        tCipher2 = cifrar(mensaje, "passB")
        self.assertNotEqual(tCipher1, tCipher2)

    # misma clave y mismo mensaje deben dar el mismo cifrado
    def testDeterminismo(self):
        mensaje = "este es el eje del determinismo"
        clave = "determinismo"
        tCipher1 = cifrar(mensaje, clave)
        tCipher2 = cifrar(mensaje, clave)
        self.assertEqual(tCipher1, tCipher2)

    # debe funcionar con longitudes distintas incluyendo vacio
    def testVariosMensajes(self):
        clave = "k"
        mensajes = ["a", "123", "mensaje de oracion de prueba", ""]

        for mensaje in mensajes:
            tCipher = cifrar(mensaje, clave)
            tPlano = descifrar(tCipher, clave)
            self.assertEqual(tPlano, mensaje)

    # mismo seed y misma longitud deben dar el mismo keystream
    def testKeystream(self):
        ks1 = generarKeystream("seed", 32)
        ks2 = generarKeystream("seed", 32)
        self.assertEqual(ks1, ks2)


if __name__ == "__main__":
    unittest.main()
