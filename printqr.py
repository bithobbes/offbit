#!/usr/bin/env python
import pyqrnative as qrlib

# http://www.utf8-chartable.de/unicode-utf8-table.pl?start=9600&number=128

sp = " "  # space
uh = u"\u2580"  # upper half
lh = u"\u2584"  # lower half
fb = u"\u2588"  # full block

def print_qr_array(QRarray):
    row = []
    print sp * len(QRarray[0])
    QRarray.append([False for i in range(len(QRarray[0]))])
    for i, y in enumerate(QRarray):
        if i % 2 == 0:
            for x in y:
                row.append(x)
            s = " "
        else:
            for x in y:
                if row.pop(0):
                    if x == 1:
                        s += fb
                    else:
                        s += uh
                else:
                    if x == 1:
                        s += lh
                    else:
                        s += sp
            print s
    print sp * len(QRarray)

def print_tx(tx):
    for i in range(1,20):
        try:
            qr = qrlib.QRCode(i, 0)
            qr.addData(tx)
            qr.make()
            break
        except qrlib.CodeOverflowException:
            if i < 20:
                continue
            else:
                raise Exception("Too much data for QR Code")
    Q = qr.export_modules()
    print_qr_array(Q)

##def print_sig(sig):
##    qr = qrlib.QRCode(9, 0)
##    qr.addData(sig)
##    qr.make()
##    Q = qr.export_modules()
##    print_qr_array(Q)

if __name__ == "__main__":
    print_tx("tasdfasdfadsasdfdasest")
