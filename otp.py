#!/usr/bin/python

import os
import sys
import getopt
import gnupg
import pyotp
import pyperclip


def usage():
    sys.stderr.write("Usage: %s [-h|--help] [-n|--name <name> | -o|--otp <otp>]\n" % sys.argv[0])

try:
    opts, args = getopt.getopt(sys.argv[1:], 'hn:o:', ['help', 'name=', 'otp='])
except getopt.GetoptError as msg:
    print(msg)
    usage()
    sys.exit(1)

n = o = False

for opt, arg in opts:
    if opt in ('-h', '--help'):
        print("Generate one-time password and copy to the clipboard")
        print("(Requires gpg2 & gpg-agent)")
        print("")
        usage()
        print("")
        print("Options:")
        print(" -h, --help         Print this help screen")
        print(" -n, --name <name>  Generate OTP based on the name from the file")
        print(" -o, --otp <otp>    Generate OTP based on the input")
        print("")
        print("Initial configuration:")
        print("~/.otp.conf:")
        print("test = OEIRJWOEFHWLEFKNLDFJSDLFKJSDLFEI2340234FDDFSFLL2340F")
        print("stage = LASDJLSDJFso98965SALDFJDSLFJSLDFJS02930SDFLSFNSDLFSD")
        print("prod = OIWEROWUER9UFSAFAUSDF9AUFAUDFOAJDSFAIUR32234LKKFADSF")
        print("")
        print("encrypt it, then remote .otp.conf:")
        print("gpg --encrypt --armor --output .otp.conf.asc -r <your-gpg-user-id> .otp.conf")
        sys.exit(1)
    elif opt in ('-n', '--name'):
        n = True
    elif opt in ('-o', '--otp'):
        o = True
    else:
        usage()
        sys.exit(1)

def main():
    if len(sys.argv) == 1 or len(sys.argv) > 3:
        usage()
        sys.exit(1)

    def gen(param):
        totp = pyotp.TOTP(param)
        totpn = totp.now()
        pyperclip.copy(totpn)
        print(totpn)
        sys.exit(0)

    if n:
        home_dir = os.environ['HOME']
        conf_file = '.otp.conf.asc'
        path = os.path.join(home_dir, conf_file)

        gpg = gnupg.GPG(use_agent=True)

        with open(path, 'rb') as fh:
            output = gpg.decrypt_file(fh)

            if output.status != "decryption ok":
                sys.stderr.write("Can't decrypt %s!\n" % conf_file)
                sys.stderr.write(output.stderr)
                sys.exit(1)

            for line in output.data.splitlines():
                lined = line.decode('utf-8') # python3 compatibility
                col = lined.split('=')
                otpkey = col[0].strip()
                otpval = col[1].strip()

                if otpkey == arg:
                    gen(otpval)

            sys.stderr.write("Can't find %s in %s!\n" % (arg, conf_file))
            sys.exit(1)
    elif o:
        gen(arg)

if __name__ == '__main__':
    main()
