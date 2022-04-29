from sqlalchemy.orm import Session

from db.schema.coins import Coin, CoinTypeEnum
from db.schema.common import Lookup


def new_coin(id: int, symbol: str, name: str, chain_name: str):
    return Coin(id, symbol, name, chain_name, CoinTypeEnum.crypto.id, True)


class CoinEnum(Lookup):
    model = Coin
    value_column = "ETH"

    btc = Coin(1, "BTC", "Bitcoin", "Bitcoin", CoinTypeEnum.crypto.id, True)
    eth = Coin(2, "ETH", "Ether", "Ethereum", CoinTypeEnum.crypto.id, True)
    doge = Coin(3, "DOGE", "DogeCoin", "DogeCoin", CoinTypeEnum.crypto.id, True)
    sol = Coin(4, "SOL", "Sol", "Solana", CoinTypeEnum.crypto.id, True)
    curve = Coin(5, "CRV", "Curve", "Curve", CoinTypeEnum.stable.id, True)
    link = Coin(6, "LINK", "Link", "Chainlink", CoinTypeEnum.stable.id, True)
    cosmos = Coin(7, "ATOM", "Atom", "Cosmos", CoinTypeEnum.crypto.id, True)
    polygon = Coin(8, "MATIC", "Matic", "Polygon", CoinTypeEnum.crypto.id, True)
    avax = Coin(9, "AVAX", "AVAX", "Avalanche", CoinTypeEnum.crypto.id, True)
    aave = Coin(10, "AAVE", "Aave", "Aave", CoinTypeEnum.crypto.id, True)
    fil = Coin(11, "FIL", "Filecoin", "Filecoin", CoinTypeEnum.crypto.id, True)
    ltc = Coin(12, "LTC", "Litecoin", "Litecoin", CoinTypeEnum.crypto.id, True)
    dot = Coin(13, "DOT", "Polkadot", "Polkadot", CoinTypeEnum.crypto.id, True)
    sushi = Coin(14, "SUSHI", "Sushi", "Sushi", CoinTypeEnum.crypto.id, True)
    ada = Coin(15, "ADA", "Cardano", "Cardano", CoinTypeEnum.crypto.id, True)
    zrx = Coin(16, "ZRX", "0x", "0x", CoinTypeEnum.crypto.id, True)
    yfi = Coin(17, "YEARN", "Yearn", "Yearn", CoinTypeEnum.crypto.id, True)
    xmr = Coin(18, "XMR", "Monero", "Monero", CoinTypeEnum.crypto.id, True)
    oneinch = Coin(19, "1INCH", "1Inch", "1Inch", CoinTypeEnum.crypto.id, True)
    algo = Coin(20, "ALGO", "Algo", "Algorand", CoinTypeEnum.crypto.id, True)
    snx = Coin(21, "SNX", "Synthetix", "Synthetix", CoinTypeEnum.crypto.id, True)
    uma = Coin(22, "UMA", "Uma", "Uma", CoinTypeEnum.crypto.id, True)
    maker = Coin(23, "MKR", "Maker", "Maker", CoinTypeEnum.crypto.id, True)
    zec = Coin(24, "ZEC", "Zcash", "Zcash", CoinTypeEnum.crypto.id, True)
    uni = Coin(25, "UNI", "Uniswap", "Uniswap", CoinTypeEnum.crypto.id, True)
    eos = Coin(26, "EOS", "Eos", "Eos", CoinTypeEnum.crypto.id, True)
    comp = Coin(27, "COMP", "Compound", "Compound", CoinTypeEnum.crypto.id, True)
    bch = Coin(28, "BCH", "Bitcoin Cash", "Bitcoin Cash", CoinTypeEnum.crypto.id, True)
    usd = Coin(29, "USD", "US Dollar", "United States", CoinTypeEnum.fiat.id, True)
    euro = Coin(30, "EURO", "Euro", "European Union", CoinTypeEnum.fiat.id, True)
    usdc = Coin(31, "USDC", "USDC", "USDC", CoinTypeEnum.stable.id, True)
    usdt = Coin(31, "USDT", "Tether", "Tether", CoinTypeEnum.stable.id, True)


def sync_lookup(db_session: Session):
    CoinEnum.populate_db(db_session)
