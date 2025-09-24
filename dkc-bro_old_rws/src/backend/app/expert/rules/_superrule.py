import app.enums as enums

# SUPERCLASS for the rules.
# This one implements all the getter classes so u don't have to on the subs


class superRule:
    def __init__(
        self,
        code,
        name,
        object_type,
        importance,
        feedbackMessage,
        explanation,
        docstring,
        ruleType=enums.RuleType.SINGLE,
    ):
        self.__code = code
        self.__name = name
        self.__importance = importance
        self.__feedbackMessage = feedbackMessage
        self.__explanation = explanation
        self.__docstring = docstring
        self.__ruleType = ruleType
        self.__objectType = object_type

    def getCode(self):
        return self.__code

    def getName(self):
        return self.__name

    def getObjectType(self):
        return self.__objectType

    def getImportance(self):
        return self.__importance

    def getImportanceDisplayName(self):
        if self.__importance == enums.Importance.INFO:
            return "Info"
        elif self.__importance == enums.Importance.WARNING:
            return "Waarschuwing"
        elif self.__importance == enums.Importance.ERROR:
            return "Fout"
        return "Onbekend"

    def getFeedbackMessage(self):
        return self.__feedbackMessage

    def getExplanation(self):
        return self.__explanation

    def getDocstring(self):
        return self.__docstring

    def getRuleType(self):
        return self.__ruleType
