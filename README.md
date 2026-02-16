# Eje-Stream-Cypher

## descripcion del proyecto

este proyecto implementa un stream cipher basico en python utilizando un generador pseudoaleatorio deterministico a partir de una clave.

el sistema funciona en tres partes principales:

- generacion de un keystream deterministico a partir de un seed
- cifrado de un mensaje aplicando xor entre el texto plano y el keystream
- descifrado aplicando nuevamente xor para recuperar el mensaje original

el objetivo es entender el funcionamiento interno de un stream cipher, su comportamiento deterministico y sus implicaciones de seguridad.

---

## instrucciones de instalacion y uso

### requisitos

- python 3.x
- no se requieren librerias externas

### ejecutar el programa principal

desde la carpeta raiz del proyecto:

```bash
python main.py
```

ejecutar pruebas unitarias

```bash
python -m unittest -q
```

## ejemplos de ejecucion

a continuacion se muestran 3 ejemplos reales de ejecucion del programa `main.py`:

```
mensaje: hola me llamo andre
clave: clave1
cipher hex: ed44924730f8f2e1fdd39625bf3c130549ffc8
cipher base64: 7USSRzD48uH905YlvzwTBUn/yA==
descifrado: hola me llamo andre
----------------------------------------
mensaje: me gusta jugar futbol
clave: realmadrid
cipher hex: 93742b0832a1f0cffb75590e203c82f6260dfcbc03
cipher base64: k3QrCDKh8M/7dVkOIDyC9iYN/LwD
descifrado: me gusta jugar futbol
----------------------------------------
mensaje: cifrando este mensaje
clave: cifrados26
cipher hex: 324b1c39af6b6095ef9628914cd4989977445c85b8
cipher base64: MkscOa9rYJXvliiRTNSYmXdEXIW4
descifrado: cifrando este mensaje
----------------------------------------
```

### 2.1 Variacion de la clave

**pregunta:**  
¿que sucede cuando cambia la clave utilizada para generar el keystream?

**respuesta:**

Cuando cambia la clave, cambia completamente el keystream generado.  
Como el cifrado se basa en aplicar xor entre el mensaje y el keystream, el cambio en la clave produce un ciphertext diferente, incluso si el mensaje es el mismo.

- misma clave + mismo mensaje = mismo ciphertext
- clave distinta + mismo mensaje = ciphertext distinto

---

#### Ejemplo practico ejecutado

```powershell
2.1 variacion de la clave
mensaje: hola me gusta comer
clave a: claveA
cipher a (hex): dc6445f326060bfd4cd753a0dc0f73489229ba
clave b: claveB
cipher b (hex): 909c6f5fd08028195406fdd4f63dc04c91b0bf
son diferentes: True
descifrado con clave a: hola me gusta comer
descifrado con clave b: hola me gusta comer
descifrado con clave equivocada fallo: 'utf-8' codec can't decode byte 0x97 in position 1: invalid start byte
```

### 2.2 Reutilizacion del keystream

**pregunta 1:**  
¿que riesgos de seguridad existen si reutiliza el mismo keystream para cifrar dos mensajes diferentes?

**respuesta:**

si se utiliza la misma clave para cifrar dos mensajes distintos, se reutiliza el mismo keystream, esto genera una vulnerabilidad.

si se tiene:
c1 y c2 = ciphers
p1 y p2 = plain texts
ks = keystream

c1 = p1 xor ks  
c2 = p2 xor ks

un atacante puede calcular:

c1 xor c2 = p1 xor p2

El keystream se elimina completamente y el atacante obtiene informacion sobre la relacion entre los mensajes originales.
Esto permite recuperar partes del mensaje si uno de los textos es conocido.

---

**pregunta 2:**  
¿que informacion puede extraer un atacante que intercepte ambos textos cifrados?

**respuesta:**

El atacante puede calcular el xor entre ambos ciphertext y obtener el xor entre los mensajes originales.  
aunque no vea directamente los textos, obtiene su relacion byte a byte.

si se conoce uno de los mensajes se puede recuperar el otro completamente.

---

#### ejemplo practico ejecutado

```powershell
2.2 reutilizacion del keystream
clave: password1
mensaje 1: hola me llamo andre
mensaje 2: pera la comio sofia
cipher 1 (hex): 95fe23b42da2348c18c261323bde0430496c62
cipher 2 (hex): 8df43db42da3308c17c16d363bde16314b7766
c1 xor c2 (hex): 180a1e00000104000f030c0400001201021b04
p1 xor p2 (hex): 180a1e00000104000f030c0400001201021b04
coinciden: True
```

### 2.3 longitud del keystream

**pregunta:**  
¿como afecta la longitud del keystream a la seguridad del cifrado? considere tanto keystreams mas cortos como mas largos que el mensaje.

**respuesta:**

la longitud del keystream influye directamente en la seguridad del cifrado. Si el keystream se repite o introduce patrones, el sistema se vuleve menos eficaz.
Se analizaron tres casos distintos.

caso 1: keystream igual al mensaje
el keystream tiene exactamente la misma longitud que el mensaje.

caso 2: keystream mas corto y repetido
al repetirse el keystream para cubrir el mensaje completo, se crea una estructura periodica.
esto reduce la seguridad porque aparecen patrones que pueden ser vulnerables mediante analisis de frecuencia.

caso 3: keystream mas largo y truncado
generar un keystream mas largo y truncarlo evita repeticion interna.
el resultado es equivalente al caso 1 si se usan los mismos primeros bytes. Pero la seguridad depende de no reutilizar.

---

#### ejemplo practico ejecutado

```powershell
2.3 longitud del keystream
clave: estaesunaprueba
mensaje: me gusta ver futbol los domingos
longitud mensaje (bytes): 32

caso 1 keystream igual al mensaje
longitud keystream: 32
cipher (hex): 7227f2fb512be96e1b8a89bc5a14707de1c18190fae21553bea448ab0e3efcbe
por lo que no hay repeticion interna del keystream

caso 2 keystream corto y repetido
longitud keystream corto: 8
keystream repetido (hex): 1f42d29c24589d0f1f42d29c24589d0f1f42d29c24589d0f1f42d29c24589d0f
cipher (hex): 7227f2fb512be96e3f34b7ee043ee87b7d2dbebc4837ee2f7b2dbff54a3ff27c
por lo tanto la repeticion da patrones y no es seguro

caso 3 keystream largo y cortado
longitud keystream largo: 48
longitud keystream truncado: 32
cipher (hex): 7227f2fb512be96e1b8a89bc5a14707de1c18190fae21553bea448ab0e3efcbe
evita la repeticion pero igual no es tan seguro
```

### 2.4 Consideraciones practicas

**pregunta:**  
¿que consideraciones debe tener al generar un keystream en un entorno de produccion real? mencione al menos 3 aspectos criticos.

**respuesta:**

En un entorno real de produccion no es suficiente generar un keystream. se deben considerar varios aspectos criticos para garantizar seguridad real.

---

#### aspectos

**1 usar un generador criptograficamente seguro**  
no se deben utilizar generadores simples como lcg. Se deben usar algoritmos estandar y auditados como chacha20 o aes en modo ctr.

**2 usar un nonce por mensaje**  
Aunque la clave sea la misma, el keystream no debe repetirse. Se debe incluir un nonce unico para cada mensaje, evitando reutilizacion del keystream.

**3 incluir autenticacion e integridad**  
xor solo cifra, pero no protege contra cosas maliciosas. Por eso see debe utilizar cifrado autenticado como aes gcm o chacha20.

**4 proteger adecuadamente las claves**  
Las claves no deben almacenarse en texto plano ni exponerse en logs. Debe de haber gestion segura de secretos y rotacion de claves.

---

## Parte 4: Reflexión Técnica (Opcional - 10 puntos extra)

### 4.1 Limitaciones de PRNG Simples

**Reflexione sobre las limitaciones de los generadores pseudoaleatorios simples en aplicaciones criptográficas reales. Considere:**

- Predictibilidad
- Periodicidad
- Calidad estadística del keystream

**Respuesta:**

Los generadores pseudoaleatorios simples son utiles para fines academicos o simulaciones, pero no son adecuados para aplicaciones criptograficas reales. Uno de los principales problemas es la predictibilidad. Muchos PRNG basicos se basan en formulas matematicas faciles de analizar. Si alguien llega y observa suficientes valores generados, puede deducir el estado interno del sistema y anticipar los siguientes numeros. Ademas, estos generadores suelen tener un ciclo limitado, lo que significa que la secuencia eventualmente se repite. Cuando el keystream se repite, aparecen patrones en el cifrado que pueden ser explotados mediante analisis con estadisticas. Tambien tienen limitaciones en su calidad estadistica, ya que pueden contener correlaciones internas o distribuciones poco uniformes, lo que vuelve mas facil su analisis.

### 4.2 Comparación con Stream Ciphers Modernos

**Investigue cómo algoritmos modernos como ChaCha20 o AES-CTR generan keystreams y compare con su implementación:**

---

**¿que mejoras de seguridad ofrecen?**

los algoritmos modernos como chacha20 y aes-ctr ofrecen mejoras importantes frente a un prng simple.  
entre ellas estan estan:

- resistencia frente a la prediccion del estado interno
- periodos extremadamente largos
- mejor calidad estadistica del keystream
- validacion y analisis criptografico durante anos por la comunidad academica

A diferencia de la implementacion de este ejercicio, estos algoritmos fueron disenados especificamente para entornos reales y para resistir ataques avanzados.

---

**¿que tecnicas usan para evitar las vulnerabilidades de prng basicos?**

para evitar problemas como la predictibilidad y la aparicion de patrones, utilizan:

- operaciones no lineales como sumas modulares y rotaciones
- funciones criptograficas robustas auditadas publicamente
- mezcla intensiva de bits para evitar correlaciones internas
- uso obligatorio de nonce o contador unico por mensaje

estas tecnicas hacen que el keystream no sea matematicamente predecible, incluso si un atacante observa multiples bloques generados.

---

**¿como manejan la inicializacion y el estado interno?**

tanto chacha20 como aes-ctr combinan:

- una clave secreta
- un nonce o vector de inicializacion unico
- un contador interno

En aes-ctr, el keystream se produce cifrando un contador incremental con aes.  
En chacha20, se genera el keystream aplicando rondas de operaciones aritmeticas y rotaciones sobre una estructura interna que incluye clave, nonce y contador.

Esto asegura que, aunque se use la misma clave cada mensaje tenga un keystream distinto si el nonce cambia, evitando reutilizacion y vulnerabilidades como las demostradas en este ejercicio.

---

### referencias

ayuda de chatgpt para su fromato y planteacion

- bernstein, d. j. (2008). _chacha, a variant of salsa20_. https://cr.yp.to/chacha/chacha-20080128.pdf

- national institute of standards and technology. (2001). _advanced encryption standard aes fips pub 197_. https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.197.pdf

- national institute of standards and technology. (2001). _recommendation for block cipher modes of operation nist sp 800-38a_. https://nvlpubs.nist.gov/nistpubs/legacy/sp/ nistspecialpublication800-38a.pdf

- nir, y., & langley, a. (2018). _chacha20 and poly1305 for ietf protocols rfc 8439_. internet engineering task force. https://www.rfc-editor.org/rfc/rfc8439
