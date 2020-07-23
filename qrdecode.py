#!/usr/bin/env python3

import sys

from PIL import Image
from pyzbar.pyzbar import decode

def usage():
    sys.stderr.write("Usage: %s QR_image_to_decode.png\n" % sys.argv[0])
    sys.exit(1)

if len(sys.argv) != 2:
    usage()
else:
    image = sys.argv[1]

def main():
    try:
        data = decode(Image.open(image))
        content = str(data[0][0], "utf-8")
    except Exception as ex:
        sys.stderr.write("Can't decode QR image: %s\n" % ex)
        sys.exit(1)
    else:
        print(content)

if __name__ == '__main__':
    main()
