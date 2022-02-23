'''
usage: macOS_bin2app.py [-h] [-b BIN] [-p PNG] [-n NAME]

optional arguments:
  -h, --help  show this help message and exit
  -b BIN      Binary file path
  -p PNG      PNG image path
  -n NAME     Output APP name
'''

import argparse
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', dest='bin', help='Binary file path')
    parser.add_argument('-p', dest='png', help='PNG image path')
    parser.add_argument('-n', dest='name', help='Output APP name')
    args = parser.parse_args()
    if (args.bin is None) + (args.png is None)+(args.name is None) > 0:
        exit(parser.print_help())
    bin = args.bin
    png = args.png
    name = args.name
    sips(png, bin, name)
    touchPlist(name)
    os.system("mv tmp %s.app" % name)


def sips(png, bin, name):
    command = ("\
    mkdir tmp.iconset\n\
    sips -z 16 16 %s --out tmp.iconset/icon_16x16.png\n\
    sips -z 32 32 %s --out tmp.iconset/icon_32x32.png\n\
    sips -z 128 128 %s --out tmp.iconset/icon_128x128.png\n\
    sips -z 256 256 %s --out tmp.iconset/icon_256x256.png\n\
    iconutil -c icns tmp.iconset -o icon.icns\n\
    rm -rf tmp.iconset/ \n\
    mkdir tmp\n\
    mkdir tmp/Contents\n\
    mkdir tmp/Contents/MacOS\n\
    mkdir tmp/Contents/Resources\n\
    mv icon.icns tmp/Contents/Resources\n\
    cp %s tmp/Contents/MacOS/%s\n\
    " % (png, png, png, png, bin, name))
    os.system(command)


def touchPlist(name):
    plist = ('''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>%s</string>
    <key>CFBundleIconFile</key>
    <string>icon.icns</string>
    <key>CFBundleIdentifier</key>
    <string>com.example.whatever</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSUIElement</key>
    <true/>
</dict>
</plist>
    ''' % name)
    f = open("tmp/Contents/Info.plist", 'w')
    f.write(plist)


if __name__ == '__main__':
    main()

