# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = motion_sensor_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast
from datetime import datetime
import dateutil.parser


T = TypeVar("T")


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Capabilities:
    certified: bool
    primary: bool

    @staticmethod
    def from_dict(obj: Any) -> 'Capabilities':
        assert isinstance(obj, dict)
        certified = from_bool(obj.get("certified"))
        primary = from_bool(obj.get("primary"))
        return Capabilities(certified, primary)

    def to_dict(self) -> dict:
        result: dict = {}
        result["certified"] = from_bool(self.certified)
        result["primary"] = from_bool(self.primary)
        return result


@dataclass
class Config:
    on: bool
    battery: int
    reachable: bool
    alert: str
    sensitivity: int
    sensitivitymax: int
    ledindication: bool
    usertest: bool
    pending: List[Any]

    @staticmethod
    def from_dict(obj: Any) -> 'Config':
        assert isinstance(obj, dict)
        on = from_bool(obj.get("on"))
        battery = from_int(obj.get("battery"))
        reachable = from_bool(obj.get("reachable"))
        alert = from_str(obj.get("alert"))
        sensitivity = from_int(obj.get("sensitivity"))
        sensitivitymax = from_int(obj.get("sensitivitymax"))
        ledindication = from_bool(obj.get("ledindication"))
        usertest = from_bool(obj.get("usertest"))
        pending = from_list(lambda x: x, obj.get("pending"))
        return Config(on, battery, reachable, alert, sensitivity, sensitivitymax, ledindication, usertest, pending)

    def to_dict(self) -> dict:
        result: dict = {}
        result["on"] = from_bool(self.on)
        result["battery"] = from_int(self.battery)
        result["reachable"] = from_bool(self.reachable)
        result["alert"] = from_str(self.alert)
        result["sensitivity"] = from_int(self.sensitivity)
        result["sensitivitymax"] = from_int(self.sensitivitymax)
        result["ledindication"] = from_bool(self.ledindication)
        result["usertest"] = from_bool(self.usertest)
        result["pending"] = from_list(lambda x: x, self.pending)
        return result


@dataclass
class State:
    presence: bool
    lastupdated: datetime

    @staticmethod
    def from_dict(obj: Any) -> 'State':
        assert isinstance(obj, dict)
        presence = from_bool(obj.get("presence"))
        lastupdated = from_datetime(obj.get("lastupdated"))
        return State(presence, lastupdated)

    def to_dict(self) -> dict:
        result: dict = {}
        result["presence"] = from_bool(self.presence)
        result["lastupdated"] = self.lastupdated.isoformat()
        return result


@dataclass
class Swupdate:
    state: str
    lastinstall: datetime

    @staticmethod
    def from_dict(obj: Any) -> 'Swupdate':
        assert isinstance(obj, dict)
        state = from_str(obj.get("state"))
        lastinstall = from_datetime(obj.get("lastinstall"))
        return Swupdate(state, lastinstall)

    def to_dict(self) -> dict:
        result: dict = {}
        result["state"] = from_str(self.state)
        result["lastinstall"] = self.lastinstall.isoformat()
        return result


@dataclass
class MotionSensor:
    state: State
    swupdate: Swupdate
    config: Config
    name: str
    type: str
    modelid: str
    manufacturername: str
    productname: str
    swversion: str
    uniqueid: str
    capabilities: Capabilities

    @staticmethod
    def from_dict(obj: Any) -> 'MotionSensor':
        assert isinstance(obj, dict)
        state = State.from_dict(obj.get("state"))
        swupdate = Swupdate.from_dict(obj.get("swupdate"))
        config = Config.from_dict(obj.get("config"))
        name = from_str(obj.get("name"))
        type = from_str(obj.get("type"))
        modelid = from_str(obj.get("modelid"))
        manufacturername = from_str(obj.get("manufacturername"))
        productname = from_str(obj.get("productname"))
        swversion = from_str(obj.get("swversion"))
        uniqueid = from_str(obj.get("uniqueid"))
        capabilities = Capabilities.from_dict(obj.get("capabilities"))
        return MotionSensor(state, swupdate, config, name, type, modelid, manufacturername, productname, swversion, uniqueid, capabilities)

    def to_dict(self) -> dict:
        result: dict = {}
        result["state"] = to_class(State, self.state)
        result["swupdate"] = to_class(Swupdate, self.swupdate)
        result["config"] = to_class(Config, self.config)
        result["name"] = from_str(self.name)
        result["type"] = from_str(self.type)
        result["modelid"] = from_str(self.modelid)
        result["manufacturername"] = from_str(self.manufacturername)
        result["productname"] = from_str(self.productname)
        result["swversion"] = from_str(self.swversion)
        result["uniqueid"] = from_str(self.uniqueid)
        result["capabilities"] = to_class(Capabilities, self.capabilities)
        return result


def motion_sensor_from_dict(s: Any) -> MotionSensor:
    return MotionSensor.from_dict(s)


def motion_sensor_to_dict(x: MotionSensor) -> Any:
    return to_class(MotionSensor, x)
