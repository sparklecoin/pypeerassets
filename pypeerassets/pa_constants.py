'''various protocol constants'''

from collections import namedtuple
from decimal import Decimal

from pypeerassets.exceptions import UnsupportedNetwork


PAParams = namedtuple('PAParams', [
    'network_name',
    'network_shortname',
    'P2TH_wif',
    'P2TH_addr',
    'test_P2TH_wif',
    'test_P2TH_addr',
    'P2TH_fee',
])

params = (

    ## PPC mainnet
    PAParams("peercoin", "ppc", "U624wXL6iT7XZ9qeHsrtPGEiU78V1YxDfwq75Mymd61Ch56w47KE",
             "PAprodbYvZqf4vjhef49aThB9rSZRxXsM6", "UAbxMGQQKmfZCwKXAhUQg3MZNXcnSqG5Z6wAJMLNVUAcyJ5yYxLP",
             "PAtesth4QreCwMzXJjYHBcCVKbC4wjbYKP", Decimal(0.01)),

    ## PPC testnet
    PAParams("peercoin-testnet", "tppc", "cTJVuFKuupqVjaQCFLtsJfG8NyEyHZ3vjCdistzitsD2ZapvwYZH",
             "miHhMLaMWubq4Wx6SdTEqZcUHEGp8RKMZt", "cQToBYwzrB3yHr8h7PchBobM3zbrdGKj2LtXqg7NQLuxsHeKJtRL",
             "mvfR2sSxAfmDaGgPcmdsTwPqzS6R9nM5Bo", Decimal(0.01)),

    ## SPRK mainnet
    PAParams("sparklecoin", "sprk", "VMy79GpUMvfQ7yVhM27brXcPvKxAUNn7oXQJ52NQGzWtPQecEYo8",
             "SatuPf4wo1JxrWFK62q7Jm8ZwYTDvXMT1n", "VQ4Gr39aazkxDy61XA1iMEKSKTgB42rdegtjhfhdfFE6sgAbxgN3",
             "SinPAWasqVVcoEcw7ymSH5PSFNZNZa2mkm", Decimal(0.01)),

    ## SPRK testnet
    PAParams("sparklecoin-testnet", "tsprk", "ejdajVvWCRinwbdnJsbcVrjukAAnhnb6CBaCrg31iu2Ljh4pVsCY",
             "tHeAnCNaQarB92WpCAHC8kRs79FhJvcjgA", "ejoPqiMAC7mbcLDH9iXM9Aqg2pj46pQ6rQNxCw3zx3DmuLLoTYQ1",
             "tTbbxyd6o9qTsUoYChay6aYtzVpreAiGHV", Decimal(0.01))
)


def param_query(name: str) -> PAParams:
    '''Find the PAParams for a network by its long or short name. Raises
    UnsupportedNetwork if no PAParams is found.
    '''

    for pa_params in params:
        if name in (pa_params.network_name, pa_params.network_shortname,):
            return pa_params

    raise UnsupportedNetwork
