#!/usr/bin/python
#
# Generate one-time password and copy to the clipboard.
# Requires gpg2 & gpg-agent.
#
# .otp.conf:
# blah = OEIRJWOEFHWLEFKNLDFJSDLFKJSDLFEI2340234FDDFSFLL2340F
# evil = LASDJLSDJFso98965SALDFJDSLFJSLDFJS02930SDFLSFNSDLFSD
#
# encrypt it:
# gpg --encrypt --armor --output .otp.conf.asc -r <your-gpg-user-id-name> .otp.conf


import os
import sys
import gnupg
import pyotp
import pyperclip


def usage():
    sys.stderr.write("Usage: %s <otpkey>\n" % sys.argv[0])
    sys.exit(1)

def main():
    if len(sys.argv) != 2:
        usage()

    home_dir = os.environ['HOME']
    conf_file = '.otp.conf.asc'
    path = os.path.join(home_dir, conf_file)
    param = sys.argv[1]

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

            if otpkey == param:
                totp = pyotp.TOTP(otpval)
                totpn = totp.now()
                pyperclip.copy(totpn)
                print(totpn)
                sys.exit(0)

        sys.stderr.write("Can't find %s in %s!\n" % (param, conf_file))
        sys.exit(1)

if __name__ == '__main__':
    main()
