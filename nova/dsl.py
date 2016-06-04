# coding: utf-8

# In this File contains Question Maps ,
# Defining the domain specific language

"""
Domain specific language for nova quepy.
"""

from quepy.dsl import FixedType, FixedRelation, HasKeyword, FixedDataRelation
# Setup the Keywords for this application
HasKeyword.relation = "ora:error_id"
# HasKeyword.language = "en"


class IsError(FixedType):
    fixedtype = "ora:ORA-Error"


class IsFile(FixedType):
    fixedtype = "ora:ORA-Files"


class ErrorIdOf(FixedDataRelation):
    relation = "ora:error_id"
    # language = "en"
    # reverse = False


class FileOf(FixedDataRelation):
    relation = "ora:oraFileName"
    # language = "en"
    # reverse = False


class FileExtensionOf(FixedDataRelation):
    relation = "ora:fileExtension"
    # language = "en"
    # reverse = False


class HasErrorTip(FixedRelation):
    relation = "ora:hasSteps"
    reverse = True


class HasErrorCause(FixedRelation):
    relation = "ora:caused_due_to"
    reverse = True


class FileLocation(FixedRelation):
    relation = "ora:fileLocation"
    reverse = True
