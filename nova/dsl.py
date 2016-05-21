# coding: utf-8

# In this File contains Question Maps ,
# Defining the domain specific language

"""
Domain specific language for nova quepy.
"""

from quepy.dsl import FixedType, FixedRelation, HasKeyword, FixedDataRelation
# Setup the Keywords for this application
HasKeyword.relation = "ora:errorId"
# HasKeyword.language = "en"


class IsError(FixedType):
    fixedtype = "ora:ORA-Error"


class ErrorIdOf(FixedDataRelation):
    relation = "ora:errorId"
    # language = "en"
    # reverse = False


class HasErrorTip(FixedRelation):
    relation = "ora:hasSteps"
    reverse = True


class HasErrorCause(FixedRelation):
    relation = "ora:cause"
    reverse = True
