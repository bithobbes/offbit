offbit v0.001 2014 hobbes / bitcointalk

Basic Bitcoin offline storage and TXs. Helps with hodling. Tor protected retrieval/broadcasting via blockchain.info.

https://github.com/bithobbes/offbit

Alpha software. Nothing guaranteed. Maximum recommendend amount: see version number. 

https://www.gnu.org/copyleft/gpl.html

Files
offbit_keygen_offline.py - generate (mnemonic) privkeys
offbit_mktx1_online.py - start transaction (also broadcast)
offbit_mktx2_offline.py - sign transaction

How to use
Generate (mnemoic) privkeys via offline keygen, load them and keep them safe (bring one half to the bank). Then:
0.) Optional: Start Tor Browser to set up a Tor socket to be used by offbit.
1.) Use mktx1 to create a transaction.
2.) Save offbit data to a USB stick (text file).
3.) Move the stick into an old offline computer, booted from a Linux Live CD (knoppix.org). Needs Python but no WiFi, no bluetooth.
4.) Start mktx2 and feed it the data (currently a manual process).
5.) Remove the USB stick so that there is no persistent data (no USB stick, no harddrive, no SD card)
6.) Verify the TX, enter your privkey and sign.
7.) Transport the signed transaction to the online computer via QR code (designated reader, synced clipboard or manually)
8.) Broadcast the signed transaction by finishing mktx1
You will be guided through the steps.

Step 7.) works completely automatic with Windows/ClipSync & Android/ZXBarcodeScanner.

QR Code Scanner
Use only open source Zebra Crossing Barcode Scanner as the other scanners sniff your data (hurting your privacy).
Helpful options:
* inverted image scan (negative)
* copy to clipboard (automatically on scan)

Clipboard syncing
* Windows & Android: ClipSync (data stays within you local WiFi)
     hint: will only sync when clipboard content has changed (will not sync on the second scan when scanning twice)
* Linux & Android: ?
* Mac & iOS: ???

Limitations
* Only small TXs will fit into the QR code.

Todo
* add manual random data for tx generation
* encrypt offbit transport data
* check if TX to publish matches original TX
* find open source clipboard local sharing software

Based on
https://github.com/vbuterin/pybitcointools (thanks vitalik!)
https://github.com/unapiedra/pyqrnative
https://github.com/spesmilo/electrum (mnemonic.py)

