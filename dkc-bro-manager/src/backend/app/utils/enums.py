from enum import Enum, IntFlag

MISSINGVALUE = -999999
PENETRATIONLENGTH_NOT_IN_SCOPE = 0.3


class DocumentAttribute(Enum):
    LOCATION = 1


class CPTParams(Enum):
    PENETRATIONLENGTH = (0, "penetrationLength")
    DEPTH = (1, "depth")
    ELAPSEDTIME = (2, "elapsedTime")
    CONERESISTANCE = (3, "coneResistance")
    CORRECTEDCONERESISTANCE = (4, "correctedConeResistance")
    NETCONERESISTANCE = (5, "netConeResistance")
    MAGNETICFIELDSTRENGTHX = (6, "magneticFieldStrenghtX")
    MAGNETICFIELDSTRENGTHY = (7, "magneticFieldStrengthY")
    MAGNETICFIELDSTRENGTHZ = (8, "magneticFieldStrengthZ")
    MAGNETICFIELDSTRENGTHTOTAL = (9, "magneticFieldStrengthTotal")
    ELECTRICALCONDUCTIVITY = (10, "electricalConductivity")
    INCLINATIONEW = (11, "inclinationEW")
    INCLINATIONNS = (12, "inclinationNS")
    INCLINATIONX = (13, "inclinationX")
    INCLINATIONY = (14, "inclinationY")
    INCLINATIONRESULTANT = (15, "inclinationResultant")
    MAGNETICINCLINATION = (16, "magneticInclination")
    MAGNETICDECLINATION = (17, "magneticDeclination")
    LOCALFRICTION = (18, "localFriction")
    PORERATIO = (19, "poreRatio")
    TEMPERATURE = (20, "temperature")
    POREPRESSUREU1 = (21, "porePressureU1")
    POREPRESSUREU2 = (22, "porePressureU2")
    POREPRESSUREU3 = (23, "porePressureU3")
    FRICTIONRATIO = (24, "frictionRatio")


class DissipationtestParams(IntFlag):
    CONUSWEERSTAND = 1
    WATERSPANNINGU1 = 2
    WATERSPANNINGU2 = 3
