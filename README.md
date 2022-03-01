# gemclubmemo.py
Python library for Gemplus GemClub Memo cards

## The card
Gemplus GemClub Memo (GCM) is a 1k EEPROM-based storage card with a smart card interface. It has a somewhat complex access control and transactional scheme.
The card is divided into 4-byte (32 bit) words, and its memory map can be found in the 1998 datasheet of the product.
The GCM has two main areas for storing data: Balance 1 / User Area 1 and Balance 2 / User Area 2, both being independently protected by a Card Secret Code (CSC, similar in function to a PIN).
On top, it has a few areas under the control of the Issuer and its partners (who know the "master PIN", CSC0).

The card is mainly used as a club card, notably by [SuperShop](https://www.supershop.hu/).

## Requirements
* Python 3
* [pyscard 2.0.2](https://pyscard.sourceforge.io) (needs [PCSC Lite](https://pcsclite.apdu.fr/))
* a PC/SC compatible contacted smartcard reader
* a Gemplus GemClub Memo card

## Usage
`gemclubmemo.py` is meant to be imported as a module:
```Python
import gemclubmemo
```
The code is fairly well-documented (use Python's `help()` function in the interactive shell).
The main class is `GemClubMemoCard`: it represents a GemClub Memo card. Plug in the card and create a reference to it:
```Python
c=gemclubmemo.GemClubMemoCard()              
c.connect()
```
After that, check out the object's functions, it should be fairly easy to get around 😃
