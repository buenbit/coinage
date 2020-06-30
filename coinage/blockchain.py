from coinage.validators.bech32 import Bech32Validator
from coinage.validators.base58check import Base58CheckValidator
from coinage.validators.sha3 import Sha3Validator
from coinage.validators.cashaddr import CashAddrValidator


class BlockchainNetwork:
    def validators(self):
        return []

    def validate(self, address):
        last_error = Exception(f'There are no validators for {self}')
        for validator in self.validators():
            try:
                return validator.validate(address)
            except FailedChecksumValidation:
                raise
            except FailedValidation as error:
                last_error = error
        raise last_error

    def is_main_net(self, net_name):
        return False


class BitcoinBlockchain(BlockchainNetwork):
    MAIN_NET = 'main'
    TEST_NET = 'test'
    UNKNOWN_NET = 'unknown'
    
    def net_name_from_human_readable_part(self, hrp):
        return {
            'bc': self.MAIN_NET,
            'tb': self.TEST_NET,
        }.get(hrp, self.UNKNOWN_NET)

    def net_name_from_version_bytes(self, version_bytes):
        return {
            0x00: self.MAIN_NET,
            0x05: self.MAIN_NET,
            0x6f: self.TEST_NET,
            0xc4: self.TEST_NET,
        }.get(version_bytes, self.UNKNOWN_NET)

    def is_main_net(self, net_name):
        return net_name == self.MAIN_NET

    def validators(self):
        return [Bech32Validator(), Base58CheckValidator()]


class BitcoinCashBlockchain(BitcoinBlockchain):
    REGTEST_NET = 'regtest'

    def net_name_from_human_readable_part(self, hrp):
        return {
            'bitcoincash': self.MAIN_NET,
            'bchtest': self.TEST_NET,
            'bchreg': self.REGTEST_NET,
        }.get(hrp, self.UNKNOWN_NET)

    def validators(self):
        return [CashAddrValidator(), Base58CheckValidator()]


class EthereumBlockchain():
    ALL_NETS = 'all'

    def net_name(self, **kwargs):
        return self.ALL_NETS

    def is_main_net(self, net_name):
        return net_name == self.ALL_NETS

    def validators(self):
        return [Sha3Validator()]
