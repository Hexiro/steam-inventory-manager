from dataclasses import dataclass
from enum import Enum
from typing import Optional, TypedDict

import requests

from . import config

PRICES = requests.get("https://csgobackpack.net/api/GetItemsList/v2/").json()["items_list"]

# for config.py

ConfigurationAccount = TypedDict(
    "ConfigurationAccount",
    {"username": str, "password": str, "shared-secret": str, "identity-secret": str, "priorities": Optional[list[str]]},
)

ConfigurationOptions = TypedDict(
    "ConfigurationOptions",
    {
        "min-price": float,
        "auto-accept-trades": bool,
        "always-trade-graffities": bool,
        "always-trade-stickers": bool,
        "always-trade-agents": bool,
        "always-trade-containers": bool,
        "always-trade-collectibles": bool,
        "always-trade-patches": bool,
    },
)


class SessionData(TypedDict):
    session_id: str
    steam_id64: int
    steam_login_secure: str


# for steam stuff


@dataclass
class TradeConfirmation:
    id: str
    data_conf_id: int
    data_key: str
    trade_id: int


class ItemExterior(Enum):
    FACTORY_NEW = "Factory New"
    MINIMAL_WEAR = "Minimal Wear"
    FIELD_TESTED = "Field-Tested"
    WELL_WORN = "Well-Worn"
    BATTLE_SCARRED = "Battle-Scarred"


class ItemType(Enum):
    # weapon types
    KNIFE = "Knife"
    GLOVES = "Gloves"
    PISTOL = "Pistol"
    RIFLE = "Rifle"
    SNIPER_RIFLE = "Sniper Rifle"
    SHOTGUN = "Shotgun"
    SMG = "SMG"
    MACHINEGUN = "Machinegun"
    # other
    GRAFFITI = "Graffiti"
    STICKER = "Sticker"
    AGENT = "Agent"
    CONTAINER = "Container"
    COLLECTIBLE = "Collectible"
    PATCH = "Patch"


@dataclass
class Item:
    # details about the item itself
    name: str
    # details about the item regarding to your inventory
    # most of these could be strings or integers, so im going off of what steam requires for their trading api
    appid: int
    contextid: str
    amount: int
    assetid: int
    # not required
    exterior: Optional[ItemExterior] = None
    type: Optional[ItemType] = None

    @property
    def is_weapon(self):
        # do gloves count as a weapon? probably not. but are they a *weapon* skin? yes
        return self.type in {
            ItemType.KNIFE,
            ItemType.GLOVES,
            ItemType.PISTOL,
            ItemType.RIFLE,
            ItemType.SNIPER_RIFLE,
            ItemType.SHOTGUN,
            ItemType.SMG,
            ItemType.MACHINEGUN,
        }

    @property
    def market_name(self):
        return f"{self.name} ({self.exterior.value})" if self.exterior else self.name

    @property
    def trade_asset(self):
        """Contains all the details needed to trade an item"""
        return {"appid": self.appid, "contextid": self.contextid, "amount": self.amount, "assetid": self.assetid}

    @property
    def price(self) -> float:
        if self.market_name not in PRICES:
            return -1
        item = PRICES[self.market_name]
        if "price" not in item:
            return -1
        # imo median is better then an average because of extreme undercuts
        # and super high prices skewing the average
        queue = ("30_days", "all_time", "7_days", "24_hours")
        for key in queue:
            if key in item["price"]:
                return item["price"][key]["median"]
        return -1

    @property
    def should_be_traded(self):
        if config.options["always-trade-graffities"] and self.type == ItemType.GRAFFITI:
            return True
        if config.options["always-trade-stickers"] and self.type == ItemType.STICKER:
            return True
        if config.options["always-trade-agents"] and self.type == ItemType.AGENT:
            return True
        if config.options["always-trade-containers"] and self.type == ItemType.CONTAINER:
            return True
        if config.options["always-trade-collectibles"] and self.type == ItemType.COLLECTIBLE:
            return True
        if config.options["always-trade-patches"] and self.type == ItemType.PATCH:
            return True
        # if the item doesn't have a price, it's likely just a pricing issue and shouldn't be traded.
        return self.price < config.options["min-price"] and self.price != -1
