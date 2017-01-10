
'''miscellaneous utilities.'''

import binascii
import pypeerassets.constants

def testnet_or_mainnet(node):
    '''check if local node is configured to testnet or mainnet'''

    if node.getinfo()["testnet"] is True:
        return "testnet"
    else:
        return "mainnet"

def load_p2th_privkeys_into_node(node):
    '''load production p2th privkey into local node'''

    if testnet_or_mainnet(node) is "testnet":
        try:
            node.importprivkey(testnet_PAPROD, "PAPROD")
            assert testnet_PAPROD_addr in node.getaddressesbyaccount("PAPROD")
        except Exception:
            return {"error": "Loading P2TH privkey failed."}
    else:
        try:
            node.importprivkey(mainnet_PAPROD, "PAPROD")
            assert mainnet_PAPROD_addr in node.getaddressesbyaccount("PAPROD")
        except Exception:
            return {"error": "Loading P2TH privkey failed."}

def load_test_p2th_privkeys_into_node(node):
    '''load test p2th privkeys into local node'''

    if testnet_or_mainnet(node) is "testnet":
        try:
            node.importprivkey(testnet_PATEST, "PATEST")
            assert mainnet_PATEST_addr in node.getaddressesbyaccount("PATEST")
        except Exception:
            return {"error": "Loading P2TH privkey failed."}

    else:
        try:
            node.importprivkey(mainnet_PATEST, "PATEST")
            assert mainnet_PAPROD_addr in node.getaddressesbyaccount("PATEST")
        except Exception:
            return {"error": "Loading P2TH privkey failed."}

def find_deck_spawns(node, prod_or_test):
    '''find deck spawn transactions via local node, it requiers that Deck spawn P2TH were imported in local node.'''

    if prod_or_test == "prod":
        decks = [i["txid"] for i in node.listtransactions("PAPROD")]
    else:
        decks = [i["txid"] for i in node.listtransactions("PATEST")]

    return decks

def read_tx_opreturn(node, txid):
    '''Decode OP_RETURN message from <txid>'''

    vouts = node.getrawtransaction(txid, 1)['vout']

    for vout in vouts:
        asm = vout['scriptPubKey']['asm']
        n = asm.find('OP_RETURN')
        if n == -1:
            continue
        else:
            # add 10 because 'OP_RETURN ' is 10 characters
            n += 10
            data = asm[n:]
            n = data.find(' ')
            #make sure that we don't include trailing opcodes
            if n == -1:
                return binascii.unhexlify(data)
            else:
                return binascii.unhexlify(data[:n])
    return {'error': 'OP_RETURN not found'}
