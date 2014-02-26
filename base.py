#!/usr/bin/env python
import pybitcointools as pbt

PARTS = 2  # fixed
WORDS = 24  # fixed
DASHLEN = 90  # must NOT be calculated to fit as it could give away length of the other part

FEEBTC = 0.0001  # Enter in BTC
SpBTC = int(1e8)
FEE = int(FEEBTC * SpBTC)

MAXFEEBTC = 0.001  # Enter in BTC
MAXFEE = int(MAXFEEBTC * SpBTC)

TORPORT = 9150

def sum_values(dictList):
    return sum([x["value"] for x in dictList])

def check_unspent(u):
    balance = sum_values(u)
    print "Number of previous outputs:", len(u)
    print "balance:", 1.0 * balance / SpBTC
    availableBalance = balance - FEE
    print "availableBalance:", float(availableBalance) / SpBTC, "(balance - fee)"
    print
    return availableBalance

def display_dtx(dtx, data):
    print "tx summary:"
    for o in dtx["outs"]:
        address = pbt.script_to_address(o["script"])
        isSource = "(change)" if address == data["source"] else ""
        print "Sending %fBTC to %s %s" % (float(o["value"]) / SpBTC, address, isSource)

    #print "has signature(s):",
    #print bool(dtx["ins"][0]["script"])

    balance = sum_values(data["u"])
    fee = (balance - sum_values(dtx["outs"]))
    print "fee:", 1.0 * fee / SpBTC
    if fee > MAXFEE * SpBTC:
        raise Exception("Fee seems too high.")
    if fee != FEE:
        print "Warning: Unexpected fee height!"
        print "Press <enter> to proceed anyway or <ctrl-c> to cancel."
        raw_input()
    print

