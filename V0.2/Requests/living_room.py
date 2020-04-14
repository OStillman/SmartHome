# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = living_room_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import List, Any, TypeVar, Callable, Type, cast


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


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Action:
    on: bool
    bri: int
    hue: int
    sat: int
    effect: str
    xy: List[float]
    ct: int
    alert: str
    colormode: str

    @staticmethod
    def from_dict(obj: Any) -> 'Action':
        assert isinstance(obj, dict)
        on = from_bool(obj.get("on"))
        bri = from_int(obj.get("bri"))
        hue = from_int(obj.get("hue"))
        sat = from_int(obj.get("sat"))
        effect = from_str(obj.get("effect"))
        xy = from_list(from_float, obj.get("xy"))
        ct = from_int(obj.get("ct"))
        alert = from_str(obj.get("alert"))
        colormode = from_str(obj.get("colormode"))
        return Action(on, bri, hue, sat, effect, xy, ct, alert, colormode)

    def to_dict(self) -> dict:
        result: dict = {}
        result["on"] = from_bool(self.on)
        result["bri"] = from_int(self.bri)
        result["hue"] = from_int(self.hue)
        result["sat"] = from_int(self.sat)
        result["effect"] = from_str(self.effect)
        result["xy"] = from_list(to_float, self.xy)
        result["ct"] = from_int(self.ct)
        result["alert"] = from_str(self.alert)
        result["colormode"] = from_str(self.colormode)
        return result


@dataclass
class State:
    all_on: bool
    any_on: bool

    @staticmethod
    def from_dict(obj: Any) -> 'State':
        assert isinstance(obj, dict)
        all_on = from_bool(obj.get("all_on"))
        any_on = from_bool(obj.get("any_on"))
        return State(all_on, any_on)

    def to_dict(self) -> dict:
        result: dict = {}
        result["all_on"] = from_bool(self.all_on)
        result["any_on"] = from_bool(self.any_on)
        return result


@dataclass
class LivingRoom:
    name: str
    lights: List[int]
    sensors: List[Any]
    type: str
    state: State
    recycle: bool
    living_room_class: str
    action: Action

    @staticmethod
    def from_dict(obj: Any) -> 'LivingRoom':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        lights = from_list(lambda x: int(from_str(x)), obj.get("lights"))
        sensors = from_list(lambda x: x, obj.get("sensors"))
        type = from_str(obj.get("type"))
        state = State.from_dict(obj.get("state"))
        recycle = from_bool(obj.get("recycle"))
        living_room_class = from_str(obj.get("class"))
        action = Action.from_dict(obj.get("action"))
        return LivingRoom(name, lights, sensors, type, state, recycle, living_room_class, action)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["lights"] = from_list(lambda x: from_str((lambda x: str(x))(x)), self.lights)
        result["sensors"] = from_list(lambda x: x, self.sensors)
        result["type"] = from_str(self.type)
        result["state"] = to_class(State, self.state)
        result["recycle"] = from_bool(self.recycle)
        result["class"] = from_str(self.living_room_class)
        result["action"] = to_class(Action, self.action)
        return result


def living_room_from_dict(s: Any) -> LivingRoom:
    return LivingRoom.from_dict(s)


def living_room_to_dict(x: LivingRoom) -> Any:
    return to_class(LivingRoom, x)
