# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = info_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Day:
    id: int
    traffic_needed: bool
    alarm_time: Optional[str] = None
    traffic_time: Optional[str] = None
    traffic_length: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Day':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        traffic_needed = from_bool(obj.get("traffic_needed"))
        alarm_time = from_union([from_none, from_str], obj.get("alarm_time"))
        traffic_time = from_union([from_none, from_str], obj.get("traffic_time"))
        traffic_length = from_union([from_int, from_none], obj.get("traffic_length"))
        return Day(id, traffic_needed, alarm_time, traffic_time, traffic_length)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["traffic_needed"] = from_bool(self.traffic_needed)
        result["alarm_time"] = from_union([from_none, from_str], self.alarm_time)
        result["traffic_time"] = from_union([from_none, from_str], self.traffic_time)
        result["traffic_length"] = from_union([from_int, from_none], self.traffic_length)
        return result


@dataclass
class Days:
    day: List[Day]

    @staticmethod
    def from_dict(obj: Any) -> 'Days':
        assert isinstance(obj, dict)
        day = from_list(Day.from_dict, obj.get("day"))
        return Days(day)

    def to_dict(self) -> dict:
        result: dict = {}
        result["day"] = from_list(lambda x: to_class(Day, x), self.day)
        return result


@dataclass
class Info:
    days: Days

    @staticmethod
    def from_dict(obj: Any) -> 'Info':
        assert isinstance(obj, dict)
        days = Days.from_dict(obj.get("days"))
        return Info(days)

    def to_dict(self) -> dict:
        result: dict = {}
        result["days"] = to_class(Days, self.days)
        return result


def info_from_dict(s: Any) -> Info:
    return Info.from_dict(s)


def info_to_dict(x: Info) -> Any:
    return to_class(Info, x)
