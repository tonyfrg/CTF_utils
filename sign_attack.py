import hashlib
import math
from Crypto.Util.number import bytes_to_long, long_to_bytes
from base64 import b64encode

# Données publiques du challenge
n = int("00b149477e0d169106ece603b3d1fb0d3b2e85381b974e5b69d06642382a7c96c254ff315cf8971b25e83d2b8df433bf857c16c82ed4607f2fc24365c3e6c5a05dd57381c68bb8915e33694f5bae1a9302815e5592e64970e037596fa3588cf7f9a0562c15ad5289708379dc94306ca30b4cb1f27583e5c398fd3e2ea2edc052e98aad2f20c4b8441c512eb448008cc3418d559e36b3bd0dd4dd85810d506367538e2d005965564a0181a5bc5d7f325781ffe007832f21bb913f2c94f4204f6c258e87ee3ee9e0b17ff3c1eae53195bccc2b369642b103001d81b424fded7cc87a08e4c61a49c97aacf3d086b07293e8fc1433e6299e0a6336cc6daad5d28675cdd98cebdccc0e6b7b39873aca56cac5f7bdb5a1efc8c2b080073f63607ae0bbd31dd4a392db08b3672d7b7c3337933286b1d7b9e9801060504aa6efd408a6362b0daf97c36f676677db6e8c33c58996514f38f5565a79", 16)
e = 3

# Préparer un message
message = "a"

# Calculer le hash SHA-256 du message
message_hash = hashlib.sha256(message.encode()).digest()

# Préfixe ASN.1 pour SHA-256
prefix_sha256 = bytes.fromhex("3031300d060960864801650304020105000420")

# Créer le bloc à signer (préfixe + hash)
to_sign = prefix_sha256 + message_hash

# Ajouter un remplissage 0xff pour obtenir la bonne taille (2736 bits = 342 octets)
block = b"\x00\x01" + b"\xff" * (342 - len(to_sign) - 3) + b"\x00" + to_sign

# Convertir le bloc en entier
block_int = bytes_to_long(block)
print(block_int)

# Calculer la racine cubique du bloc pour obtenir la signature
signature_int = 1081947199765842424529591879509026010150599323721976877318063532086628152436172512203606540057921920808293160946190599534351047801861499980289103827892100253508375928829962412377562148201321351276593628996016513851695161943555198441141036848674890703850575013678567420592128

# Convertir la signature en base64 pour l'envoyer au serveur
signature_bytes = long_to_bytes(signature_int)
signature_b64 = b64encode(signature_bytes).decode()

print("Signature (Base64) : ", signature_b64)
