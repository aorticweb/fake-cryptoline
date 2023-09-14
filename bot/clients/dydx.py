from logging import getLogger
from typing import Dict, List

import requests
from requests import Response

from bot.clients import BaseClient
from bot.exceptions import DataSourceInconsistencyException
from bot.models.price import PairPrice
from bot.validate import validate_api_request_status_code

DYDX_V3_BASE_URL = "https://api.dydx.exchange/v3"

# TODO:
# Improve logging
logger = getLogger(__name__)


class DyDx(BaseClient):
    base_url: str

    def __init__(self, base_url=DYDX_V3_BASE_URL):
        self.base_url = base_url

    def _get(self, route: str = "/", params: Dict = None, headers: Dict = None) -> Response:
        resp = requests.get(f"{self.base_url}{route}", params=params, headers=headers)
        validate_api_request_status_code(resp)
        return resp

    def _markets(self):
        return self._get("/markets")

    def _parse_pair_prices(self, resp: Response) -> List[PairPrice]:
        prices = []

        pairs_data = resp.json().get("markets", None)
        if pairs_data is None or not isinstance(pairs_data, dict):
            raise DataSourceInconsistencyException(
                "DYDX client: /markets, missing parent field 'markets'"
            )

        for data in pairs_data.values():
            try:
                prices.append(
                    PairPrice(
                        symbol=data["baseAsset"],
                        price=data["indexPrice"],
                        reference_asset=data["quoteAsset"],
                    )
                )
            except KeyError:
                exc = DataSourceInconsistencyException(
                    "DYDX client: /markets, market pair missing fields", extra=data
                )
                logger.error(exc)
        return prices

    def markets(self) -> List[PairPrice]:
        resp = self._markets()
        prices = self._parse_pair_prices(resp)
        return prices



if __name__ == "__main__":
    from pprint import pprint

    markets_resp = DyDx().markets()
    pprint(markets_resp.json())
