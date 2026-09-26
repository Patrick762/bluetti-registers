The Bluetooth protocol is mostly based on [bluetti_mqtt](https://github.com/warhammerkid/bluetti_mqtt) from [@warhammerkid](https://github.com/warhammerkid) who started with Reverse Engineering the proprietary protocol for Bluetti Powerstations.
After Bluetti added encryption to the protocol for some devices, [@nhurman](https://github.com/nhurman) Reverse Engineered their encryption and made it available on [GitHub](https://github.com/nhurman/bluetti_mqtt/blob/main/bluetti_mqtt/bluetooth/encryption.py).

Based on the information from both, we now know the following:
- The protocol is based on [Modbus-RTU](https://wikipedia.org/wiki/Modbus#Modbus_RTU).
- The encryption is based on [AES](https://wikipedia.org/wiki/Advanced_Encryption_Standard) using [ECDH](https://wikipedia.org/wiki/Elliptic-curve_Diffie-Hellman) for key exchange.
- Keys for the encrypted communication with the powerstations
- There are at least 2 versions of the protocol
