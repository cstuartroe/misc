from OpenSSL import crypto
import base64
import codecs

encodings = {'ascii':'Jefe','utf-8':'Jefe','hex':'4a656665','base64':'SmVmZQ==\n'}

def tobytes(s,encoding='utf-8'):
    if encoding == 'utf-8':
        return codecs.encode(s,encoding='utf-8')
    elif encoding == 'ascii':
        return codecs.encode(s,encoding='ascii')
    elif encoding == 'hex':
        return codecs.decode(bytes(s,encoding='ascii'),encoding='hex')
    elif encoding == 'base64':
        return codecs.decode(bytes(s,encoding='ascii'),encoding='base64')
    else:
        raise TypeError('Not a valid encoding scheme.')

for encoding in encodings:
    assert(tobytes(encodings[encoding],encoding) == b'Jefe')

##message = bytes('key', 'utf-8')
##secret = bytes('The quick brown fox jumps over the lazy dog', 'utf-8')
##
##hash = hmac.new(secret, message, hashlib.sha256)
##
### to lowercase hexits
##hexdig = hash.hexdigest()
##
### to base64
##b64dig = base64.b64encode(hash.digest())
