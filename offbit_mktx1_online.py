#!/usr/bin/env python

try:
    import base
    import torsetup
    import pybitcointools as pbt
    import time
    import json
    import Tkinter as tk
    root = tk.Tk()
    root.withdraw()

    ########################################################################################

    print "About to query inputs from blockchain.info"
    print "Enter address to spend from:"
    print "(Normal address or Electrum root address.)"
    source = raw_input()
    print

    u = pbt.unspent(source)
    availableBalance = base.check_unspent(u)

    targets = []
    amounts = []
    while 1:
        print "Enter target address:"
        targets.append(raw_input())
        if targets[-1] == "":
            targets.pop(-1)
            if len(targets) == 0:
                continue
            break
        print

        print "Enter amount to spend in Bitcoin:"
        print "(maximum: " + str(float(availableBalance - sum(amounts)) / base.SpBTC) + ")"
        amount = raw_input()
        if not amount:
            amount = "0.0001"
        amount = int(float(amount) * base.SpBTC)
        amounts.append(amount)
        if sum(amounts) > availableBalance:
            raise Exception("Spend amount higher than available balance.")
        print

        print "Add another target address or press <enter> to continue."

    data = {"u" : u, "source" : source, "targets" : targets, "amounts" : amounts}

    print "Offbit data:"
    print "(Transport safely to offline system. Keep the '!' at the end.)"
    print
    print json.dumps(data) + "!"
    print

    root.update()
    root.clipboard_clear()
    print "Waiting for signed tx in clipboard (no carriage returns allowed)."
    print "Press <ctrl-c> to cancel."
    cb = ""
    while 1:
        try:

            try:
                root.update()
                sigRtx = root.clipboard_get()
                if sigRtx == cb:
                    time.sleep(0.5)
                    continue
                cb = sigRtx
                print cb
            except tk.TclError:
                time.sleep(0.5)
                continue
            sigRtx = pbt.changebase(sigRtx.strip(), 58, 16)
            if len(sigRtx) % 2:
                sigRtx = "0" + sigRtx
            sigDtx = {}
            try:
                sigDtx = pbt.deserialize(sigRtx)
            except:
                pass
            if sigDtx["ins"][0]["script"]:
                break
        except (IndexError, KeyError):
            pass
        else:
            raise
        time.sleep(0.5)

    base.display_dtx(sigDtx, data)
    sigRtx = pbt.serialize(sigDtx)

    print "About to publish tx"
    print "Press <enter> to proceed, <ctrl-c> to cancel."
    raw_input()
    print

    print pbt.pushtx(sigRtx)

except:
    import traceback
    traceback.print_exc()
print "Good bye - <enter>"
raw_input()
