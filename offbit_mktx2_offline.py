#!/usr/bin/env python

import base
import pybitcointools as pbt
import printqr
import json
import mnemonic

while 1:
    try:
        while 1:
            try:
                print "\n\n\n"
                print "Enter offbit data:"
                data = ""
                while 1:
                    data += raw_input()
                    if data[-1] == "!":
                        data = data[:-1]
                        break
                data = json.loads(data)
                break
            except ValueError:
                print "Decode error (carriage returns are not allowed)"
                continue

        availableBalance = base.check_unspent(data["u"])

        # build tx
        outs = [{'value' : availableBalance - sum(data["amounts"]), 'address' : data["source"]}]  # change
        if outs[0]["value"] == 0:
            outs = []
        for i, t in enumerate(data["targets"]):
            outs.append({'value' : data["amounts"][i], 'address' : data["targets"][i]})

        rtx = pbt.mktx(data["u"], outs)  # serialized tx
        dtx = pbt.deserialize(rtx)

        base.display_dtx(dtx, data)

        print "Check balance and targets. Remove your data source (USB-stick)."
        print "Press <enter> to proceed, <ctrl-c> to cancel."
        raw_input()
        print

        print "Enter private key or (double) Electrum seed:"
        priv = raw_input().strip()
        if " " in priv:
            seed = mnemonic.mn_decode(priv.split(" "))
            priv = pbt.electrum_privkey(seed, 0, 0)  # root key
        source = pbt.privkey_to_address(priv)
        if source != data["source"]:
            print "Address from privkey:", source
            raise Exception ("Privkey does not match source address.")
        print


        # sign tx
        for i in range(len(dtx["ins"])):
            rtx = pbt.sign(rtx, i, priv)

        print "signed serialized tx:"
        print
        rtx58 = pbt.changebase(rtx, 16, 58)
        print rtx58
        printqr.print_tx(rtx58)

        print
        print "Restart your computer to clear memory."
        raw_input()
    except:
        import traceback
        traceback.print_exc()
        print
        print "Starting over...."

