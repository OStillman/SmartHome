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
#     result = traffic_from_dict(json.loads(json_string))

from dataclasses import dataclass
from datetime import datetime
from typing import List, Any, TypeVar, Callable, Type, cast
from enum import Enum
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


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


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


@dataclass
class MetaInfo:
    timestamp: datetime
    map_version: str
    module_version: str
    interface_version: str
    available_map_version: List[str]

    @staticmethod
    def from_dict(obj: Any) -> 'MetaInfo':
        assert isinstance(obj, dict)
        timestamp = from_datetime(obj.get("timestamp"))
        map_version = from_str(obj.get("mapVersion"))
        module_version = from_str(obj.get("moduleVersion"))
        interface_version = from_str(obj.get("interfaceVersion"))
        available_map_version = from_list(from_str, obj.get("availableMapVersion"))
        return MetaInfo(timestamp, map_version, module_version, interface_version, available_map_version)

    def to_dict(self) -> dict:
        result: dict = {}
        result["timestamp"] = self.timestamp.isoformat()
        result["mapVersion"] = from_str(self.map_version)
        result["moduleVersion"] = from_str(self.module_version)
        result["interfaceVersion"] = from_str(self.interface_version)
        result["availableMapVersion"] = from_list(from_str, self.available_map_version)
        return result


@dataclass
class Position:
    latitude: float
    longitude: float

    @staticmethod
    def from_dict(obj: Any) -> 'Position':
        assert isinstance(obj, dict)
        latitude = from_float(obj.get("latitude"))
        longitude = from_float(obj.get("longitude"))
        return Position(latitude, longitude)

    def to_dict(self) -> dict:
        result: dict = {}
        result["latitude"] = to_float(self.latitude)
        result["longitude"] = to_float(self.longitude)
        return result


@dataclass
class Waypoint:
    link_id: int
    mapped_position: Position
    original_position: Position
    type: str
    spot: float
    side_of_street: str
    mapped_road_name: str
    label: str
    shape_index: int
    source: str

    @staticmethod
    def from_dict(obj: Any) -> 'Waypoint':
        assert isinstance(obj, dict)
        link_id = int(from_str(obj.get("linkId")))
        mapped_position = Position.from_dict(obj.get("mappedPosition"))
        original_position = Position.from_dict(obj.get("originalPosition"))
        type = from_str(obj.get("type"))
        spot = from_float(obj.get("spot"))
        side_of_street = from_str(obj.get("sideOfStreet"))
        mapped_road_name = from_str(obj.get("mappedRoadName"))
        label = from_str(obj.get("label"))
        shape_index = from_int(obj.get("shapeIndex"))
        source = from_str(obj.get("source"))
        return Waypoint(link_id, mapped_position, original_position, type, spot, side_of_street, mapped_road_name, label, shape_index, source)

    def to_dict(self) -> dict:
        result: dict = {}
        result["linkId"] = from_str(str(self.link_id))
        result["mappedPosition"] = to_class(Position, self.mapped_position)
        result["originalPosition"] = to_class(Position, self.original_position)
        result["type"] = from_str(self.type)
        result["spot"] = to_float(self.spot)
        result["sideOfStreet"] = from_str(self.side_of_street)
        result["mappedRoadName"] = from_str(self.mapped_road_name)
        result["label"] = from_str(self.label)
        result["shapeIndex"] = from_int(self.shape_index)
        result["source"] = from_str(self.source)
        return result


class TypeEnum(Enum):
    PRIVATE_TRANSPORT_MANEUVER_TYPE = "PrivateTransportManeuverType"


@dataclass
class Maneuver:
    position: Position
    instruction: str
    travel_time: int
    length: int
    id: str
    type: TypeEnum

    @staticmethod
    def from_dict(obj: Any) -> 'Maneuver':
        assert isinstance(obj, dict)
        position = Position.from_dict(obj.get("position"))
        instruction = from_str(obj.get("instruction"))
        travel_time = from_int(obj.get("travelTime"))
        length = from_int(obj.get("length"))
        id = from_str(obj.get("id"))
        type = TypeEnum(obj.get("_type"))
        return Maneuver(position, instruction, travel_time, length, id, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["position"] = to_class(Position, self.position)
        result["instruction"] = from_str(self.instruction)
        result["travelTime"] = from_int(self.travel_time)
        result["length"] = from_int(self.length)
        result["id"] = from_str(self.id)
        result["_type"] = to_enum(TypeEnum, self.type)
        return result


@dataclass
class Leg:
    start: Waypoint
    end: Waypoint
    length: int
    travel_time: int
    maneuver: List[Maneuver]

    @staticmethod
    def from_dict(obj: Any) -> 'Leg':
        assert isinstance(obj, dict)
        start = Waypoint.from_dict(obj.get("start"))
        end = Waypoint.from_dict(obj.get("end"))
        length = from_int(obj.get("length"))
        travel_time = from_int(obj.get("travelTime"))
        maneuver = from_list(Maneuver.from_dict, obj.get("maneuver"))
        return Leg(start, end, length, travel_time, maneuver)

    def to_dict(self) -> dict:
        result: dict = {}
        result["start"] = to_class(Waypoint, self.start)
        result["end"] = to_class(Waypoint, self.end)
        result["length"] = from_int(self.length)
        result["travelTime"] = from_int(self.travel_time)
        result["maneuver"] = from_list(lambda x: to_class(Maneuver, x), self.maneuver)
        return result


@dataclass
class Mode:
    type: str
    transport_modes: List[str]
    traffic_mode: str
    feature: List[Any]

    @staticmethod
    def from_dict(obj: Any) -> 'Mode':
        assert isinstance(obj, dict)
        type = from_str(obj.get("type"))
        transport_modes = from_list(from_str, obj.get("transportModes"))
        traffic_mode = from_str(obj.get("trafficMode"))
        feature = from_list(lambda x: x, obj.get("feature"))
        return Mode(type, transport_modes, traffic_mode, feature)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_str(self.type)
        result["transportModes"] = from_list(from_str, self.transport_modes)
        result["trafficMode"] = from_str(self.traffic_mode)
        result["feature"] = from_list(lambda x: x, self.feature)
        return result


@dataclass
class Summary:
    distance: int
    traffic_time: int
    base_time: int
    flags: List[str]
    text: str
    travel_time: int
    type: str

    @staticmethod
    def from_dict(obj: Any) -> 'Summary':
        assert isinstance(obj, dict)
        distance = from_int(obj.get("distance"))
        traffic_time = from_int(obj.get("trafficTime"))
        base_time = from_int(obj.get("baseTime"))
        flags = from_list(from_str, obj.get("flags"))
        text = from_str(obj.get("text"))
        travel_time = from_int(obj.get("travelTime"))
        type = from_str(obj.get("_type"))
        return Summary(distance, traffic_time, base_time, flags, text, travel_time, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["distance"] = from_int(self.distance)
        result["trafficTime"] = from_int(self.traffic_time)
        result["baseTime"] = from_int(self.base_time)
        result["flags"] = from_list(from_str, self.flags)
        result["text"] = from_str(self.text)
        result["travelTime"] = from_int(self.travel_time)
        result["_type"] = from_str(self.type)
        return result


@dataclass
class Route:
    waypoint: List[Waypoint]
    mode: Mode
    leg: List[Leg]
    summary: Summary

    @staticmethod
    def from_dict(obj: Any) -> 'Route':
        assert isinstance(obj, dict)
        waypoint = from_list(Waypoint.from_dict, obj.get("waypoint"))
        mode = Mode.from_dict(obj.get("mode"))
        leg = from_list(Leg.from_dict, obj.get("leg"))
        summary = Summary.from_dict(obj.get("summary"))
        return Route(waypoint, mode, leg, summary)

    def to_dict(self) -> dict:
        result: dict = {}
        result["waypoint"] = from_list(lambda x: to_class(Waypoint, x), self.waypoint)
        result["mode"] = to_class(Mode, self.mode)
        result["leg"] = from_list(lambda x: to_class(Leg, x), self.leg)
        result["summary"] = to_class(Summary, self.summary)
        return result


@dataclass
class Response:
    meta_info: MetaInfo
    route: List[Route]
    language: str

    @staticmethod
    def from_dict(obj: Any) -> 'Response':
        assert isinstance(obj, dict)
        meta_info = MetaInfo.from_dict(obj.get("metaInfo"))
        route = from_list(Route.from_dict, obj.get("route"))
        language = from_str(obj.get("language"))
        return Response(meta_info, route, language)

    def to_dict(self) -> dict:
        result: dict = {}
        result["metaInfo"] = to_class(MetaInfo, self.meta_info)
        result["route"] = from_list(lambda x: to_class(Route, x), self.route)
        result["language"] = from_str(self.language)
        return result


@dataclass
class Traffic:
    response: Response

    @staticmethod
    def from_dict(obj: Any) -> 'Traffic':
        assert isinstance(obj, dict)
        response = Response.from_dict(obj.get("response"))
        return Traffic(response)

    def to_dict(self) -> dict:
        result: dict = {}
        result["response"] = to_class(Response, self.response)
        return result


def traffic_from_dict(s: Any) -> Traffic:
    return Traffic.from_dict(s)


def traffic_to_dict(x: Traffic) -> Any:
    return to_class(Traffic, x)
