from enum import Enum

class DescriptiveEnum(str, Enum):
    def __new__(cls, value, description):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj