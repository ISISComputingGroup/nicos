#pylint: skip-file
# Python stubs generated by omniidl from corbadevice.idl

import omniORB, _omnipy
from omniORB import CORBA, PortableServer
_0_CORBA = CORBA

_omnipy.checkVersion(3,0, __file__)


#
# Start of module "CARESS"
#
__name__ = "CARESS"
_0_CARESS = omniORB.openModule("CARESS", r"corbadevice.idl")
_0_CARESS__POA = omniORB.openModule("CARESS__POA", r"corbadevice.idl")


# enum ReturnType
_0_CARESS.OK = omniORB.EnumItem("OK", 0)
_0_CARESS.NOT_OK = omniORB.EnumItem("NOT_OK", 1)
_0_CARESS.ReturnType = omniORB.Enum("IDL:CARESS/ReturnType:1.0", (_0_CARESS.OK, _0_CARESS.NOT_OK,))

_0_CARESS._d_ReturnType  = (omniORB.tcInternal.tv_enum, _0_CARESS.ReturnType._NP_RepositoryId, "ReturnType", _0_CARESS.ReturnType._items)
_0_CARESS._tc_ReturnType = omniORB.tcInternal.createTypeCode(_0_CARESS._d_ReturnType)
omniORB.registerType(_0_CARESS.ReturnType._NP_RepositoryId, _0_CARESS._d_ReturnType, _0_CARESS._tc_ReturnType)

# typedef ... ArrayLong
class ArrayLong:
    _NP_RepositoryId = "IDL:CARESS/ArrayLong:1.0"
    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")
_0_CARESS.ArrayLong = ArrayLong
_0_CARESS._d_ArrayLong  = (omniORB.tcInternal.tv_sequence, omniORB.tcInternal.tv_long, 0)
_0_CARESS._ad_ArrayLong = (omniORB.tcInternal.tv_alias, ArrayLong._NP_RepositoryId, "ArrayLong", (omniORB.tcInternal.tv_sequence, omniORB.tcInternal.tv_long, 0))
_0_CARESS._tc_ArrayLong = omniORB.tcInternal.createTypeCode(_0_CARESS._ad_ArrayLong)
omniORB.registerType(ArrayLong._NP_RepositoryId, _0_CARESS._ad_ArrayLong, _0_CARESS._tc_ArrayLong)
del ArrayLong

# typedef ... ArrayFloat
class ArrayFloat:
    _NP_RepositoryId = "IDL:CARESS/ArrayFloat:1.0"
    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")
_0_CARESS.ArrayFloat = ArrayFloat
_0_CARESS._d_ArrayFloat  = (omniORB.tcInternal.tv_sequence, omniORB.tcInternal.tv_float, 0)
_0_CARESS._ad_ArrayFloat = (omniORB.tcInternal.tv_alias, ArrayFloat._NP_RepositoryId, "ArrayFloat", (omniORB.tcInternal.tv_sequence, omniORB.tcInternal.tv_float, 0))
_0_CARESS._tc_ArrayFloat = omniORB.tcInternal.createTypeCode(_0_CARESS._ad_ArrayFloat)
omniORB.registerType(ArrayFloat._NP_RepositoryId, _0_CARESS._ad_ArrayFloat, _0_CARESS._tc_ArrayFloat)
del ArrayFloat

# typedef ... ArrayByte
class ArrayByte:
    _NP_RepositoryId = "IDL:CARESS/ArrayByte:1.0"
    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")
_0_CARESS.ArrayByte = ArrayByte
_0_CARESS._d_ArrayByte  = (omniORB.tcInternal.tv_sequence, omniORB.tcInternal.tv_octet, 0)
_0_CARESS._ad_ArrayByte = (omniORB.tcInternal.tv_alias, ArrayByte._NP_RepositoryId, "ArrayByte", (omniORB.tcInternal.tv_sequence, omniORB.tcInternal.tv_octet, 0))
_0_CARESS._tc_ArrayByte = omniORB.tcInternal.createTypeCode(_0_CARESS._ad_ArrayByte)
omniORB.registerType(ArrayByte._NP_RepositoryId, _0_CARESS._ad_ArrayByte, _0_CARESS._tc_ArrayByte)
del ArrayByte

# typedef ... ArrayComplex
class ArrayComplex:
    _NP_RepositoryId = "IDL:CARESS/ArrayComplex:1.0"
    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")
_0_CARESS.ArrayComplex = ArrayComplex
_0_CARESS._d_ArrayComplex  = (omniORB.tcInternal.tv_sequence, omniORB.tcInternal.tv_any, 0)
_0_CARESS._ad_ArrayComplex = (omniORB.tcInternal.tv_alias, ArrayComplex._NP_RepositoryId, "ArrayComplex", (omniORB.tcInternal.tv_sequence, omniORB.tcInternal.tv_any, 0))
_0_CARESS._tc_ArrayComplex = omniORB.tcInternal.createTypeCode(_0_CARESS._ad_ArrayComplex)
omniORB.registerType(ArrayComplex._NP_RepositoryId, _0_CARESS._ad_ArrayComplex, _0_CARESS._tc_ArrayComplex)
del ArrayComplex

# typedef ... ArrayLong64
class ArrayLong64:
    _NP_RepositoryId = "IDL:CARESS/ArrayLong64:1.0"
    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")
_0_CARESS.ArrayLong64 = ArrayLong64
_0_CARESS._d_ArrayLong64  = (omniORB.tcInternal.tv_sequence, omniORB.tcInternal.tv_longlong, 0)
_0_CARESS._ad_ArrayLong64 = (omniORB.tcInternal.tv_alias, ArrayLong64._NP_RepositoryId, "ArrayLong64", (omniORB.tcInternal.tv_sequence, omniORB.tcInternal.tv_longlong, 0))
_0_CARESS._tc_ArrayLong64 = omniORB.tcInternal.createTypeCode(_0_CARESS._ad_ArrayLong64)
omniORB.registerType(ArrayLong64._NP_RepositoryId, _0_CARESS._ad_ArrayLong64, _0_CARESS._tc_ArrayLong64)
del ArrayLong64

# typedef ... ArrayDouble
class ArrayDouble:
    _NP_RepositoryId = "IDL:CARESS/ArrayDouble:1.0"
    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")
_0_CARESS.ArrayDouble = ArrayDouble
_0_CARESS._d_ArrayDouble  = (omniORB.tcInternal.tv_sequence, omniORB.tcInternal.tv_double, 0)
_0_CARESS._ad_ArrayDouble = (omniORB.tcInternal.tv_alias, ArrayDouble._NP_RepositoryId, "ArrayDouble", (omniORB.tcInternal.tv_sequence, omniORB.tcInternal.tv_double, 0))
_0_CARESS._tc_ArrayDouble = omniORB.tcInternal.createTypeCode(_0_CARESS._ad_ArrayDouble)
omniORB.registerType(ArrayDouble._NP_RepositoryId, _0_CARESS._ad_ArrayDouble, _0_CARESS._tc_ArrayDouble)
del ArrayDouble

# enum DataType
_0_CARESS.TypeLong = omniORB.EnumItem("TypeLong", 0)
_0_CARESS.TypeFloat = omniORB.EnumItem("TypeFloat", 1)
_0_CARESS.TypeArrayLong = omniORB.EnumItem("TypeArrayLong", 2)
_0_CARESS.TypeArrayFloat = omniORB.EnumItem("TypeArrayFloat", 3)
_0_CARESS.TypeArrayByte = omniORB.EnumItem("TypeArrayByte", 4)
_0_CARESS.TypeString = omniORB.EnumItem("TypeString", 5)
_0_CARESS.TypeComplex = omniORB.EnumItem("TypeComplex", 6)
_0_CARESS.TypeLong64 = omniORB.EnumItem("TypeLong64", 7)
_0_CARESS.TypeDouble = omniORB.EnumItem("TypeDouble", 8)
_0_CARESS.TypeArrayLong64 = omniORB.EnumItem("TypeArrayLong64", 9)
_0_CARESS.TypeArrayDouble = omniORB.EnumItem("TypeArrayDouble", 10)
_0_CARESS.DataType = omniORB.Enum("IDL:CARESS/DataType:1.0", (_0_CARESS.TypeLong, _0_CARESS.TypeFloat, _0_CARESS.TypeArrayLong, _0_CARESS.TypeArrayFloat, _0_CARESS.TypeArrayByte, _0_CARESS.TypeString, _0_CARESS.TypeComplex, _0_CARESS.TypeLong64, _0_CARESS.TypeDouble, _0_CARESS.TypeArrayLong64, _0_CARESS.TypeArrayDouble,))

_0_CARESS._d_DataType  = (omniORB.tcInternal.tv_enum, _0_CARESS.DataType._NP_RepositoryId, "DataType", _0_CARESS.DataType._items)
_0_CARESS._tc_DataType = omniORB.tcInternal.createTypeCode(_0_CARESS._d_DataType)
omniORB.registerType(_0_CARESS.DataType._NP_RepositoryId, _0_CARESS._d_DataType, _0_CARESS._tc_DataType)

# union Value
_0_CARESS.Value = omniORB.newEmptyClass()
class Value (omniORB.Union):
    _NP_RepositoryId = "IDL:CARESS/Value:1.0"

_0_CARESS.Value = Value

Value._m_to_d = {"l": _0_CARESS.TypeLong, "f": _0_CARESS.TypeFloat, "al": _0_CARESS.TypeArrayLong, "af": _0_CARESS.TypeArrayFloat, "ab": _0_CARESS.TypeArrayByte, "s": _0_CARESS.TypeString, "c": _0_CARESS.TypeComplex, "l64": _0_CARESS.TypeLong64, "d": _0_CARESS.TypeDouble, "al64": _0_CARESS.TypeArrayLong64, "ad": _0_CARESS.TypeArrayDouble}
Value._d_to_m = {_0_CARESS.TypeLong: "l", _0_CARESS.TypeFloat: "f", _0_CARESS.TypeArrayLong: "al", _0_CARESS.TypeArrayFloat: "af", _0_CARESS.TypeArrayByte: "ab", _0_CARESS.TypeString: "s", _0_CARESS.TypeComplex: "c", _0_CARESS.TypeLong64: "l64", _0_CARESS.TypeDouble: "d", _0_CARESS.TypeArrayLong64: "al64", _0_CARESS.TypeArrayDouble: "ad"}
Value._def_m  = None
Value._def_d  = None

_0_CARESS._m_Value  = ((_0_CARESS.TypeLong, "l", omniORB.tcInternal.tv_long), (_0_CARESS.TypeFloat, "f", omniORB.tcInternal.tv_float), (_0_CARESS.TypeArrayLong, "al", omniORB.typeMapping["IDL:CARESS/ArrayLong:1.0"]), (_0_CARESS.TypeArrayFloat, "af", omniORB.typeMapping["IDL:CARESS/ArrayFloat:1.0"]), (_0_CARESS.TypeArrayByte, "ab", omniORB.typeMapping["IDL:CARESS/ArrayByte:1.0"]), (_0_CARESS.TypeString, "s", (omniORB.tcInternal.tv_string,0)), (_0_CARESS.TypeComplex, "c", omniORB.typeMapping["IDL:CARESS/ArrayComplex:1.0"]), (_0_CARESS.TypeLong64, "l64", omniORB.tcInternal.tv_longlong), (_0_CARESS.TypeDouble, "d", omniORB.tcInternal.tv_double), (_0_CARESS.TypeArrayLong64, "al64", omniORB.typeMapping["IDL:CARESS/ArrayLong64:1.0"]), (_0_CARESS.TypeArrayDouble, "ad", omniORB.typeMapping["IDL:CARESS/ArrayDouble:1.0"]),)
_0_CARESS._d_Value  = (omniORB.tcInternal.tv_union, Value, Value._NP_RepositoryId, "Value", omniORB.typeMapping["IDL:CARESS/DataType:1.0"], -1, _0_CARESS._m_Value, None, {_0_CARESS.TypeLong: _0_CARESS._m_Value[0], _0_CARESS.TypeFloat: _0_CARESS._m_Value[1], _0_CARESS.TypeArrayLong: _0_CARESS._m_Value[2], _0_CARESS.TypeArrayFloat: _0_CARESS._m_Value[3], _0_CARESS.TypeArrayByte: _0_CARESS._m_Value[4], _0_CARESS.TypeString: _0_CARESS._m_Value[5], _0_CARESS.TypeComplex: _0_CARESS._m_Value[6], _0_CARESS.TypeLong64: _0_CARESS._m_Value[7], _0_CARESS.TypeDouble: _0_CARESS._m_Value[8], _0_CARESS.TypeArrayLong64: _0_CARESS._m_Value[9], _0_CARESS.TypeArrayDouble: _0_CARESS._m_Value[10]})
_0_CARESS._tc_Value = omniORB.tcInternal.createTypeCode(_0_CARESS._d_Value)
omniORB.registerType(Value._NP_RepositoryId, _0_CARESS._d_Value, _0_CARESS._tc_Value)
del Value

# exception ErrorDescription
_0_CARESS.ErrorDescription = omniORB.newEmptyClass()
class ErrorDescription (CORBA.UserException):
    _NP_RepositoryId = "IDL:CARESS/ErrorDescription:1.0"

    def __init__(self, description):
        CORBA.UserException.__init__(self, description)
        self.description = description

_0_CARESS.ErrorDescription = ErrorDescription
_0_CARESS._d_ErrorDescription  = (omniORB.tcInternal.tv_except, ErrorDescription, ErrorDescription._NP_RepositoryId, "ErrorDescription", "description", (omniORB.tcInternal.tv_string,0))
_0_CARESS._tc_ErrorDescription = omniORB.tcInternal.createTypeCode(_0_CARESS._d_ErrorDescription)
omniORB.registerType(ErrorDescription._NP_RepositoryId, _0_CARESS._d_ErrorDescription, _0_CARESS._tc_ErrorDescription)
del ErrorDescription

# interface CORBADevice
_0_CARESS._d_CORBADevice = (omniORB.tcInternal.tv_objref, "IDL:CARESS/CORBADevice:1.0", "CORBADevice")
omniORB.typeMapping["IDL:CARESS/CORBADevice:1.0"] = _0_CARESS._d_CORBADevice
_0_CARESS.CORBADevice = omniORB.newEmptyClass()
class CORBADevice :
    _NP_RepositoryId = _0_CARESS._d_CORBADevice[1]

    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")

    _nil = CORBA.Object._nil


_0_CARESS.CORBADevice = CORBADevice
_0_CARESS._tc_CORBADevice = omniORB.tcInternal.createTypeCode(_0_CARESS._d_CORBADevice)
omniORB.registerType(CORBADevice._NP_RepositoryId, _0_CARESS._d_CORBADevice, _0_CARESS._tc_CORBADevice)

# CORBADevice operations and attributes
CORBADevice._d_init_module = ((omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long, (omniORB.tcInternal.tv_string,0)), (omniORB.typeMapping["IDL:CARESS/ReturnType:1.0"], omniORB.tcInternal.tv_long), None)
CORBADevice._d_init_module_ex = ((omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long, (omniORB.tcInternal.tv_string,0), (omniORB.tcInternal.tv_string,0)), (omniORB.typeMapping["IDL:CARESS/ReturnType:1.0"], omniORB.tcInternal.tv_long, (omniORB.tcInternal.tv_string,0)), None)
CORBADevice._d_release_module = ((omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long), (omniORB.typeMapping["IDL:CARESS/ReturnType:1.0"], ), {_0_CARESS.ErrorDescription._NP_RepositoryId: _0_CARESS._d_ErrorDescription})
CORBADevice._d_start_module = ((omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long), (omniORB.typeMapping["IDL:CARESS/ReturnType:1.0"], omniORB.tcInternal.tv_long), {_0_CARESS.ErrorDescription._NP_RepositoryId: _0_CARESS._d_ErrorDescription})
CORBADevice._d_stop_module = ((omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long), (omniORB.typeMapping["IDL:CARESS/ReturnType:1.0"], omniORB.tcInternal.tv_long), {_0_CARESS.ErrorDescription._NP_RepositoryId: _0_CARESS._d_ErrorDescription})
CORBADevice._d_drive_module = ((omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long, omniORB.typeMapping["IDL:CARESS/Value:1.0"], omniORB.tcInternal.tv_long), (omniORB.typeMapping["IDL:CARESS/ReturnType:1.0"], omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_boolean, omniORB.tcInternal.tv_long), {_0_CARESS.ErrorDescription._NP_RepositoryId: _0_CARESS._d_ErrorDescription})
CORBADevice._d_load_module = ((omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long, omniORB.typeMapping["IDL:CARESS/Value:1.0"]), (omniORB.typeMapping["IDL:CARESS/ReturnType:1.0"], omniORB.tcInternal.tv_long), {_0_CARESS.ErrorDescription._NP_RepositoryId: _0_CARESS._d_ErrorDescription})
CORBADevice._d_loadblock_module = ((omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long, omniORB.typeMapping["IDL:CARESS/Value:1.0"]), (omniORB.typeMapping["IDL:CARESS/ReturnType:1.0"], omniORB.tcInternal.tv_long), {_0_CARESS.ErrorDescription._NP_RepositoryId: _0_CARESS._d_ErrorDescription})
CORBADevice._d_read_module = ((omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long), (omniORB.typeMapping["IDL:CARESS/ReturnType:1.0"], omniORB.tcInternal.tv_long, omniORB.typeMapping["IDL:CARESS/Value:1.0"]), {_0_CARESS.ErrorDescription._NP_RepositoryId: _0_CARESS._d_ErrorDescription})
CORBADevice._d_readblock_params = ((omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long, omniORB.typeMapping["IDL:CARESS/DataType:1.0"]), (omniORB.typeMapping["IDL:CARESS/ReturnType:1.0"], omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long, omniORB.typeMapping["IDL:CARESS/DataType:1.0"]), {_0_CARESS.ErrorDescription._NP_RepositoryId: _0_CARESS._d_ErrorDescription})
CORBADevice._d_readblock_module = ((omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long), (omniORB.typeMapping["IDL:CARESS/ReturnType:1.0"], omniORB.tcInternal.tv_long, omniORB.typeMapping["IDL:CARESS/Value:1.0"]), {_0_CARESS.ErrorDescription._NP_RepositoryId: _0_CARESS._d_ErrorDescription})
CORBADevice._d_is_readable_module = ((omniORB.tcInternal.tv_long, ), (omniORB.tcInternal.tv_boolean, ), None)
CORBADevice._d_is_drivable_module = ((omniORB.tcInternal.tv_long, ), (omniORB.tcInternal.tv_boolean, ), None)
CORBADevice._d_is_counting_module = ((omniORB.tcInternal.tv_long, ), (omniORB.tcInternal.tv_boolean, ), None)
CORBADevice._d_is_status_module = ((omniORB.tcInternal.tv_long, ), (omniORB.tcInternal.tv_boolean, ), None)
CORBADevice._d_needs_reference_module = ((omniORB.tcInternal.tv_long, ), (omniORB.tcInternal.tv_boolean, ), None)
CORBADevice._d_get_attribute = ((omniORB.tcInternal.tv_long, (omniORB.tcInternal.tv_string,0)), (omniORB.typeMapping["IDL:CARESS/Value:1.0"], ), {_0_CARESS.ErrorDescription._NP_RepositoryId: _0_CARESS._d_ErrorDescription})
CORBADevice._d_set_attribute = ((omniORB.tcInternal.tv_long, (omniORB.tcInternal.tv_string,0), omniORB.typeMapping["IDL:CARESS/Value:1.0"]), (), {_0_CARESS.ErrorDescription._NP_RepositoryId: _0_CARESS._d_ErrorDescription})

# CORBADevice object reference
class _objref_CORBADevice (CORBA.Object):
    _NP_RepositoryId = CORBADevice._NP_RepositoryId

    def __init__(self):
        CORBA.Object.__init__(self)

    def init_module(self, *args):
        return _omnipy.invoke(self, "init_module", _0_CARESS.CORBADevice._d_init_module, args)

    def init_module_ex(self, *args):
        return _omnipy.invoke(self, "init_module_ex", _0_CARESS.CORBADevice._d_init_module_ex, args)

    def release_module(self, *args):
        return _omnipy.invoke(self, "release_module", _0_CARESS.CORBADevice._d_release_module, args)

    def start_module(self, *args):
        return _omnipy.invoke(self, "start_module", _0_CARESS.CORBADevice._d_start_module, args)

    def stop_module(self, *args):
        return _omnipy.invoke(self, "stop_module", _0_CARESS.CORBADevice._d_stop_module, args)

    def drive_module(self, *args):
        return _omnipy.invoke(self, "drive_module", _0_CARESS.CORBADevice._d_drive_module, args)

    def load_module(self, *args):
        return _omnipy.invoke(self, "load_module", _0_CARESS.CORBADevice._d_load_module, args)

    def loadblock_module(self, *args):
        return _omnipy.invoke(self, "loadblock_module", _0_CARESS.CORBADevice._d_loadblock_module, args)

    def read_module(self, *args):
        return _omnipy.invoke(self, "read_module", _0_CARESS.CORBADevice._d_read_module, args)

    def readblock_params(self, *args):
        return _omnipy.invoke(self, "readblock_params", _0_CARESS.CORBADevice._d_readblock_params, args)

    def readblock_module(self, *args):
        return _omnipy.invoke(self, "readblock_module", _0_CARESS.CORBADevice._d_readblock_module, args)

    def is_readable_module(self, *args):
        return _omnipy.invoke(self, "is_readable_module", _0_CARESS.CORBADevice._d_is_readable_module, args)

    def is_drivable_module(self, *args):
        return _omnipy.invoke(self, "is_drivable_module", _0_CARESS.CORBADevice._d_is_drivable_module, args)

    def is_counting_module(self, *args):
        return _omnipy.invoke(self, "is_counting_module", _0_CARESS.CORBADevice._d_is_counting_module, args)

    def is_status_module(self, *args):
        return _omnipy.invoke(self, "is_status_module", _0_CARESS.CORBADevice._d_is_status_module, args)

    def needs_reference_module(self, *args):
        return _omnipy.invoke(self, "needs_reference_module", _0_CARESS.CORBADevice._d_needs_reference_module, args)

    def get_attribute(self, *args):
        return _omnipy.invoke(self, "get_attribute", _0_CARESS.CORBADevice._d_get_attribute, args)

    def set_attribute(self, *args):
        return _omnipy.invoke(self, "set_attribute", _0_CARESS.CORBADevice._d_set_attribute, args)

    __methods__ = ["init_module", "init_module_ex", "release_module", "start_module",
                   "stop_module", "drive_module", "load_module", "loadblock_module",
                   "read_module", "readblock_params", "readblock_module",
                   "is_readable_module", "is_drivable_module", "is_counting_module",
                   "is_status_module", "needs_reference_module", "get_attribute",
                   "set_attribute"] + CORBA.Object.__methods__

omniORB.registerObjref(CORBADevice._NP_RepositoryId, _objref_CORBADevice)
_0_CARESS._objref_CORBADevice = _objref_CORBADevice
del CORBADevice, _objref_CORBADevice

# CORBADevice skeleton
__name__ = "CARESS__POA"
class CORBADevice (PortableServer.Servant):
    _NP_RepositoryId = _0_CARESS.CORBADevice._NP_RepositoryId


    _omni_op_d = {"init_module": _0_CARESS.CORBADevice._d_init_module,
                  "init_module_ex": _0_CARESS.CORBADevice._d_init_module_ex,
                  "release_module": _0_CARESS.CORBADevice._d_release_module,
                  "start_module": _0_CARESS.CORBADevice._d_start_module,
                  "stop_module": _0_CARESS.CORBADevice._d_stop_module,
                  "drive_module": _0_CARESS.CORBADevice._d_drive_module,
                  "load_module": _0_CARESS.CORBADevice._d_load_module,
                  "loadblock_module": _0_CARESS.CORBADevice._d_loadblock_module,
                  "read_module": _0_CARESS.CORBADevice._d_read_module,
                  "readblock_params": _0_CARESS.CORBADevice._d_readblock_params,
                  "readblock_module": _0_CARESS.CORBADevice._d_readblock_module,
                  "is_readable_module": _0_CARESS.CORBADevice._d_is_readable_module,
                  "is_drivable_module": _0_CARESS.CORBADevice._d_is_drivable_module,
                  "is_counting_module": _0_CARESS.CORBADevice._d_is_counting_module,
                  "is_status_module": _0_CARESS.CORBADevice._d_is_status_module,
                  "needs_reference_module": _0_CARESS.CORBADevice._d_needs_reference_module,
                  "get_attribute": _0_CARESS.CORBADevice._d_get_attribute,
                  "set_attribute": _0_CARESS.CORBADevice._d_set_attribute}

CORBADevice._omni_skeleton = CORBADevice
_0_CARESS__POA.CORBADevice = CORBADevice
omniORB.registerSkeleton(CORBADevice._NP_RepositoryId, CORBADevice)
del CORBADevice
__name__ = "CARESS"

#
# End of module "CARESS"
#
__name__ = "nicos.device.vendor.caress.corbadevice_idl"

_exported_modules = ( "CARESS", )

# The end.
