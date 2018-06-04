from pypeerassets.networks import net_query
from pypeerassets.base58 import b58encode, b58decode
from hashlib import sha256, new
from binascii import unhexlify, hexlify
from os import urandom
from btcpy.structs.crypto import PublicKey, PrivateKey
from btcpy.structs.transaction import MutableTransaction, TxOut
from btcpy.structs.sig import P2pkhSolver
from btcpy.setup import setup


class Kutil:

    def __init__(self, network: str, privkey: PrivateKey=None, from_bytes: bytes=None,
                 from_string: str=None, from_wif: str=None) -> None:
        '''
           High level helper class for handling public key cryptography.

           : privkey - use PrivateKey class from btcpy library
           : from_wif - <WIF> import private key from your wallet in WIF format
           : from_bytes - import private key in binary format
           : network - specify network [ppc, tppc, btc]
           : from_string - specify seed (string) to make the privkey from
           '''

        self.network = network

        try:
            if self.network.startswith('t'):
                setup('testnet')
            else:
                setup('mainnet')
        except ValueError:
            pass

        if privkey is not None:
            self._private_key = PrivateKey(privkey)

        if from_string is not None:
            self._private_key = PrivateKey(sha256(from_string.encode()).digest())

        if from_wif is not None:
            #Convert WIF into bytearray - btcpy cannot be used
            #Due to missing PPC prefixes
            wifFromPriv = self.wif_to_privkey(from_wif)
            self._private_key = wifFromPriv['privkey']
            
        if not privkey:
            if from_string == from_wif is None:  # generate a new privkey
                self._private_key = PrivateKey(bytearray(urandom(32)))

        #Hexlify the bytearray _private_key
        self.privkey = self._private_key.hexlify()
        #Get publickey from btcpy 
        self._public_key = PublicKey.from_priv(self._private_key)
        #Set pubkey to the hexlified output of above
        self.pubkey = self._public_key.hexlify()
        self.load_network_parameters(network)

    def load_network_parameters(self, network: str) -> None:
        '''loads network parameters and sets class variables'''

        for field, var in zip(net_query(network)._fields, net_query(network)):
            setattr(self, field, var)

    def wif_to_privkey(self, wif: str) -> dict:
        '''import WIF'''

        if not 51 <= len(wif) <= 52:
            return 'Invalid WIF length'

        b58_wif = b58decode(wif)
        return {'privkey': b58_wif[1:33], 'net_prefix': hexlify(b58_wif[0:1])}

    @property
    def address(self) -> str:
        '''generate an address from pubkey'''

        return str(self._public_key.to_address())

    @property
    def wif(self) -> str:
        '''convert raw private key to WIF'''

        return self._private_key.to_wif()

    def sign_transaction(self, txin: TxOut,
                         tx: MutableTransaction) -> MutableTransaction:
        '''sign the parent txn outputs P2PKH'''
        #Pass PrivateKey object from btcpy
        solver = P2pkhSolver(PrivateKey(self._private_key))
        return tx.spend([txin], [solver])
