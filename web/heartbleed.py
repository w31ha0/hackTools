import sys, base64, gmpy
from pyasn1.codec.der import encoder
from pyasn1.type.univ import *

def main ():
        n = int ("00d52ec41c43bb2f40ec74ff09bfab6d96b87e77cb88928fbfca12be4ac441e2ef2d0679f5a9010caeaadd3ba9c82b1c26d51ff91aeca6c319cec15a7ec2f9460f9db6df1a1df39db262fa3f258a4b41ef192030e9b64b717c06dcd0aec4a5edd82cfb057423e58f7885f1a784cbf44c2a8a75e26f34844edf27ef953df55986e6d0066b7d4a83f52f09bc0cce106761bf5db09024e4670b113132ec2df6edcf46d02664585aa50fe642125953ee6512bfb00b86c0e39e5abe4d0e468b0b4169910cbd98ce1165e5148a97d530d646de1a4d05e529bc9593adb7d803471d26b0a0ed90986f2f2ffa73c7a94797b849247f30ca0ca27c8208d1b51233387cc7b801", 16)
        keysize = n.bit_length() / 16
        with open (sys.argv[1], "rb") as f:
                chunk = f.read (16384)
                while chunk:
                        for offset in xrange (0, len (chunk) - keysize):
                                p = long (''.join (["%02x" % ord (chunk[x]) for x in xrange (offset + keysize - 1, offset - 1, -1)]).strip(), 16)
                                if gmpy.is_prime (p) and p != n and n % p == 0:
                                        e = 65537
                                        q = n / p
                                        phi = (p - 1) * (q - 1)
                                        d = gmpy.invert (e, phi)
                                        dp = d % (p - 1)
                                        dq = d % (q - 1)
                                        qinv = gmpy.invert (q, p)
                                        seq = Sequence()
                                        for x in [0, n, e, d, p, q, dp, dq, qinv]:
                                                seq.setComponentByPosition (len (seq), Integer (x))
                                        print "\n\n-----BEGIN RSA PRIVATE KEY-----\n%s-----END RSA PRIVATE KEY-----\n\n" % base64.encodestring(encoder.encode (seq))
                                        sys.exit (0)
                        chunk = f.read (16384)
                print "private key not found :("

if __name__ == '__main__':
        main()