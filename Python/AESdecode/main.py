import base64
import hashlib
from Crypto.Cipher import AES

ct = base64.b64decode("AAQz1rUDqp849MRxu0tqGRGvPcLzVG24xa5zbYxpwVHH6Z2p95xPPzNhMIRMcaTPvijE71RQU1X3cQhtnXdRScA6UBiLWNs9vMul2gldnMTpT92sDYHl+hKBGy2dR22Un7ElToipSqeqRrwhEK8T9ROMChrBw8i7JOICpOYoVhqDB72BH2RG\/PqjRqsKittES5BVhTTY9cs+zQI0rM+FQA62bVCL57P3RD+E+aWJJLjUvoXBqct6Jc5W7li9mk9udgn9rPKkCbXSCvwIxcWS5C1kw4uSO7y0IlovaTWLAIw5nY0l4REjbC1wPWrtxDWLlr8J+\/sQdDF+P61VHz6yiC+w56QLDjVwz4kBl3r3uP\/VZ7kUuLwWHSHnbmmXv31f")
iv = bytes.fromhex("feae762ac889376169708872d9676319")
salt = bytes.fromhex("9b2328e8a4ee2717")

# In your case, the pass phrase is NOT a hex-encoded byte array.
#  It is directly used as bytes.
pass_phrase = b"f12c8b59265dc1e898135211cc30be49"

md = hashlib.md5()
md.update(pass_phrase)
md.update(salt)
cache0 = md.digest()

md = hashlib.md5()
md.update(cache0)
md.update(pass_phrase)
md.update(salt)
cache1 = md.digest()

key = cache0 + cache1

cipher = AES.new(key, AES.MODE_CBC, iv)
result = cipher.decrypt(ct)

unpad = lambda s : s[:-ord(s[len(s)-1:])]


print(unpad(result))
