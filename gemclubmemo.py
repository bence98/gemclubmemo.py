from enum import IntEnum, IntFlag
#from smartcard.System import readers
from smartcard.CardType import ATRCardType
from smartcard.CardRequest import CardRequest
from smartcard.Exceptions import NoCardException

GCM_CLASS=0x80 # not really used by card

GCM_INS_READ=0xbe
GCM_INS_WRITE=0xde
GCM_INS_VERIFY=0x20

"""
Used for specifying which CSC you want to present in a `verify` operation
"""
class VerifyTarget(IntEnum):
	"""
	Present Card Secret Code 0
	"""
	CSC0=0x07
	"""
	Present Card Secret Code 1
	"""
	CSC1=0x39
	"""
	Present Card Secret Code 2
	"""
	CSC2=0x3b
	"""
	In Issuer mode: Enter User mode emulation. Presented value is ignored.
	"""
	EMUL=0x3a

"""
Pre-defined constants for GemClub Memo's memory map
"""
class Address(IntEnum):
	"""
	Manufacturer Area
	"""
	MANUFACTURER=0x00
	"""
	Base address of Issuer Area
	"""
	ISSUER_BASE=0x01
	"""
	Access Control Area and Protected Area 1
	"""
	ACA_PROT=0x05
	"""
	Card Secret Code 0
	"""
	CSC0=0x06
	"""
	Card Secret Code 0 Ratification Counter
	"""
	CSC0_RCNT=0x07
	"""
	Card Transaction Counter 1
	"""
	CTC1=0x08
	"""
	Card Transaction Counter 1 Backup
	"""
	CTC1_B=0x09
	"""
	Card Transaction Counter 1 Flags
	"""
	CTC1_F=0x0a
	"""
	Balance 1 Flags
	"""
	BAL1_F=0x0b
	"""
	Balance 1 high word. Must be updated before writing BAL1L
	"""
	BAL1H=0x0c
	"""
	Balance 1 high word Backup
	"""
	BAL1H_B=0x0d
	"""
	Balance 1 low word. Must be updated after writing BAL1H
	"""
	BAL1L=0x0e
	"""
	Balance 1 low word Backup
	"""
	BAL1L_B=0x0f
	"""
	Base address of User Area 1
	"""
	USER1_BASE=0x10
	"""
	Card Transaction Counter 2
	"""
	CTC2=0x20
	"""
	Card Transaction Counter 2 Backup
	"""
	CTC2_B=0x21
	"""
	Card Transaction Counter 2 Flags
	"""
	CTC2_F=0x22
	"""
	Balance 2 Flags
	"""
	BAL2_F=0x23
	"""
	Balance 2 high word. Must be updated before writing BAL2L
	"""
	BAL2H=0x24
	"""
	Balance 2 high word Backup
	"""
	BAL2H_B=0x25
	"""
	Balance 2 low word. Must be updated after writing BAL2H
	"""
	BAL2L=0x26
	"""
	Balance 2 low word Backup
	"""
	BAL2L_B=0x27
	"""
	Base address of User Area 2
	"""
	USER2_BASE=0x28
	"""
	Card Secret Code 1
	"""
	CSC1=0x38
	"""
	Card Secret Code 1 Ratification Counter
	"""
	CSC1_RCNT=0x39
	"""
	Card Secret Code 2
	"""
	CSC2=0x3a
	"""
	Card Secret Code 2 Ratification Counter
	"""
	CSC2_RCNT=0x3b
	"""
	Base address of Protected Area 2
	"""
	PROT_BASE=0x3c
	"""
	Last word in card. Addresses higher than this will yield an IndexError
	"""
	_CARD_END=0x3f

"""
Operating mode of the card
"""
class Mode(IntEnum):
	"""
	Issuer mode: card can be personalized with CSC0
	"""
	ISSUER=1
	"""
	User mode: many fields are read-only and/or automatically managed
	"""
	USER=2

"""
Access conditions of the card
"""
class AccessConditions(IntFlag):
	"""
	Protect CTC1 and Balance 1 by CSC1.
	Normally 1, i.e. reading CTC1 and Balance 1 needs CSC1.
	If 0, they can always be read.
	"""
	PROT_BAL1 = 0x80,
	"""
	Disallow updating of Balance 1 by CSC1
	Normally 0, i.e. the field can be updated using CSC1.
	If 0, it is read-only.
	"""
	LOCK_BAL1 = 0x40,
	"""
	Protect User Area 1 by CSC1.
	Normally 1, i.e. reading User Area 1 needs CSC1.
	If 0, it can always be read.
	"""
	PROT_USR1 = 0x20,
	"""
	Disallow updating of User Area 1 by CSC1
	Normally 0, i.e. the field can be updated using CSC1.
	If 0, it is read-only.
	"""
	LOCK_USR1 = 0x10,
	"""
	Protect CTC2 and Balance 2 by CSC2.
	Normally 1, i.e. reading CTC2 and Balance 2 needs CSC2.
	If 0, they can always be read.
	"""
	PROT_BAL2 = 0x08,
	"""
	Disallow updating of Balance 2 by CSC2
	Normally 0, i.e. the field can be updated using CSC2.
	If 0, it is read-only.
	"""
	LOCK_BAL2 = 0x04,
	"""
	Protect User Area 2 by CSC2.
	Normally 1, i.e. reading User Area 2 needs CSC2.
	If 0, it can always be read.
	"""
	PROT_USR2 = 0x02,
	"""
	Disallow updating of User Area 2 by CSC2
	Normally 0, i.e. the field can be updated using CSC2.
	If 0, it is read-only.
	"""
	LOCK_USR2 = 0x01

"""
Default values used by GemPlus when manufacturing cards
"""
class Defaults:
	"""
	Default Manufacturer Area string
	"""
	MFA = b'\xaa\xff\xff\xff'
	"""
	Default CSC0
	"""
	CSC0=b'\xaa'*4
	"""
	Default CSC1
	"""
	CSC1=b'\x11'*4
	"""
	Default CSC2
	"""
	CSC2=b'\x22'*4
	"""
	Invalid value for CSC's
	"""
	INV_CSC1=b'\0'*4
	"""
	Invalid value for CSC's
	"""
	INV_CSC2=b'\x80'+b'\0'*3
	"""
	Invalid value for CSC's
	"""
	INV_CSC3=b'\x7f'+b'\xff'*3
	"""
	Invalid value for CSC's
	"""
	INV_CSC4=b'\xff'*4

"""
CardType to pass to CardRequest() for finding GemClub Memo cards
"""
GCMCardType=ATRCardType([0x3b, 0x02, 0x53, 0x01], [0xff, 0xff, 0xff, 0x00])

def _checkSW(sw1, sw2, data):
	if sw1 == 0x69 and sw2 == 0x82:
		raise PermissionError("Security not satisfied.")
	if sw1 == 0x6b and sw2 == 0x00:
		raise IndexError("Invalid P2 parameter.")
	if sw1 == 0x65 and sw2 == 0x81:
		raise ValueError("Memory error: unknown flag, unknown mode or CTC reached maximum allowed value.")
	if sw1 == 0x67 and sw2 == 0x00:
		raise IndexError("Invalid length of expected data.")
	if sw1 == 0x65 and sw2 == 0x81:
		raise ValueError("Unknown mode.")
	if sw1 == 0x6d and sw2 == 0x00:
		raise ValueError("Invalid instruction byte (INS).")
	if sw1 == 0x63 and sw2 == 0x00:
		raise ValueError("Invalid secret code or forbidden value")
	if sw1 == 0x90 and sw2 == 00:
		return data
	raise Exception("Unexpected SW response! {:02x} {:02x}".format(sw1, sw2))

def _parseRC(rcWord):
	rcNibble=rcWord[3]>>4
	if rcNibble == 0x0:
		return 0
	if rcNibble == 0x8:
		return 1
	if rcNibble == 0xc:
		return 2
	if rcNibble == 0xe:
		return 3
	if rcNibble == 0xf:
		return -1 # card now blocked
	raise Exception("Invalid Ratification Counter value!")

def readGCM(con, off):
	apdu=[GCM_CLASS, GCM_INS_READ, 0x00, off, 0x04]
	resp, sw1, sw2 = con.transmit(apdu)
	return _checkSW(sw1, sw2, resp)

def writeGCM(con, off, data):
	apdu=[GCM_CLASS, GCM_INS_WRITE, 0x00, off, len(data)] + data
	resp, sw1, sw2 = con.transmit(apdu)
	return _checkSW(sw1, sw2, True)

def verifyGCM(con, target, data):
	apdu=[GCM_CLASS, GCM_INS_VERIFY, 0x00, target, len(data)] + data
	resp, sw1, sw2 = con.transmit(apdu)
	return _checkSW(sw1, sw2, True)

class GemClubMemoCard:
	def __init__(self, con=None, timeout=10):
		if con is None:
			req = CardRequest(timeout=timeout, cardType=GCMCardType)
			svc = req.waitforcard()
			con = svc.connection
		self._con = con

	"""
	Connect to the card and read its Manufacturer Area
	"""
	def connect(self):
		self._con.connect()
		self.mfa=self.readWordRaw(Address.MANUFACTURER)

	"""
	Disconnect from the card
	"""
	def disconnect(self):
		self._con.disconnect()

	"""
	Get Issuer Area data (usually card serial number)
	"""
	def getIssuerSN(self):
		issuer0=readGCM(self._con, Address.ISSUER_BASE)
		issuer1=readGCM(self._con, Address.ISSUER_BASE+1)
		issuer2=readGCM(self._con, Address.ISSUER_BASE+2)
		issuer3=readGCM(self._con, Address.ISSUER_BASE+3)
		return bytes(issuer0+issuer1+issuer2+issuer3)

	"""
	Get card operating mode
	"""
	def getMode(self):
		issuer3=readGCM(self._con, Address.ISSUER_BASE+3)
		return Mode(issuer3[3]>>6)

	"""
	Get card access conditions
	"""
	def getAccessConditions(self):
		aca=readGCM(self._con, Address.ACA_PROT)
		return AccessConditions(aca[3])

	"""
	Get a ratification counter's value
	"""
	def getRatificationCounter(self, addr):
		rcnt=readGCM(self._con, addr)
		return _parseRC(rcnt)

	"""
	Read a word from the card
	"""
	def readWord(self, addr):
		return int.from_bytes(self.readWordRaw(addr), 'big')

	"""
	Read a word from the card (as bytes)
	"""
	def readWordRaw(self, addr):
		word=readGCM(self._con, addr)
		return bytes(word)

	def writeWord(self, addr, word):
		if word is int:
			word=word.to_bytes(4, 'big') # TODO endianness
		return writeGCM(self._con, addr, list(word))

	"""
	Perform a verify operation for unlocking areas with CSC's
	"""
	def verify(self, target, code):
		if code is int:
			code=(int(digit) for digit in str(code))
		return verifyGCM(self._con, target, list(code))
