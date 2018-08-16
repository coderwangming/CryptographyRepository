# This program proves that the keyspace of the affine cipher is limited
# to len(SYMBOLS) ^ 2.
#keyA有95种可能 keyB有95中可能
#能够使用的keyA有75个，故Affine Cipher有75*95=7125个可用的key
from lib import affineCipher, cryptomath

message = 'Make things as simple as possible, but not simpler.'
count = 0
for keyA in range(2, 100):
    key = keyA * len(affineCipher.SYMBOLS) + 1

    if cryptomath.gcd(keyA, len(affineCipher.SYMBOLS)) == 1:
        count = count + 1
        print(keyA, affineCipher.encryptMessage(key, message))

print (count)