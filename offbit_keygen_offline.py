#!/usr/bin/env python
# -*- coding: cp1252 -*-
import random
import os
import time
import hashlib
import pybitcointools as pbt

import mnemonic

PARTS = 2  # fixed
WORDS = 24  # fixed
DASHLEN = 90  # must NOT be calculated to fit as it could give away length of the other part

##with open("icelist.txt") as f:
##    wordList = f.read().split("\n")

wordList = mnemonic.words

print "len(wordList):", len(wordList)

########################################################################################

print "Enter some random characters and press <enter>."
rawEntropy = raw_input()

print "Enter a title for this paper wallet and press <enter>."
title = raw_input().strip()
print "working...\n\n"

# generate passPhrase
entropy = rawEntropy
entropy += os.urandom(32) + str(random.randrange(2**256)) + str(int(time.time())**7)  # from Vitalik
entropyHash = hashlib.sha256(entropy).hexdigest()
words = mnemonic.mn_encode(entropyHash)
if len(words) != WORDS:
    raise Exception("Encode error.")
passPhrase = " ".join(words)

seed = mnemonic.mn_decode(passPhrase.split(" "))
rootPrivKey = pbt.electrum_privkey(seed, 0, 0)
rootAddress = pbt.electrum_address(seed, 0, 0)
mpk = pbt.electrum_mpk(seed)

# output
parts = [" ".join(words[:WORDS / 2]), " ".join(words[WORDS / 2:])]

for i, p in enumerate(parts):
    part = " ".join(p)
    for c in range(2):
        print "\n" + "-" * DASHLEN + "\n"
        if title:
            print title
        print "Electrum 1.x seed part %d of %d" % (i + 1, PARTS), "  copy", "AB"[c]
        if i == 0:
            print "rootAddress:", rootAddress
            #print "mpk:", mpk
        print p
print "\n" + "-" * DASHLEN + "\n"


if 1:
    print "\n\n"
    print "Press <enter> to show verification data. <ctrl-c> to exit."
    raw_input()
    print "Only for verification against address above (do not print / do destroy):"
    print "privKey:", pbt.bin_to_b58check(rootPrivKey.decode("hex"), 0x80)  # WIF wallet import format
    print "electrum seed:", passPhrase


