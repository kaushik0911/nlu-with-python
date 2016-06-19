# coding: utf-8

"""
Basic queries for nova quepy.
"""
from quepy.parsing import Lemma, Pos, QuestionTemplate, Particle, Token, Match, Lemmas, Tokens
from refo import Group, Question, Plus, Literal, Predicate, patterns
from dsl import IsError, ErrorIdOf, HasErrorTip, HasErrorCause, IsFile, FileOf, FileExtensionOf, FileLocation

error_tokens = Token("ORA00942") | Token("ORA01034") | Token("ORA12514") | Token("ORA12541") \
               | Token("ORA12543") + Token("ORA28000") + Token("ORA01652") | Token("ORA12502")
file_tokens = Token("listener")
extension_tokens = Token("ora")


class WhatIsOraError(QuestionTemplate):
    """
    Regex for questions like

    What is ora-00942? -- ok
    What is the meaning of ora-00942? -- ok
    what is meant by ora-00942? -- ok
    What means by ora-00942? -- ok
    (?What is) definition of ora-00942? -- ok

    target; is the key token in the question
    interpret; create the query link to get specific data, it build the query
    meta data contains some information for xml creation
    """

    # target = Question(Pos("DT")) + Question((Lemma('mean')) + Pos("IN")) +\
    #     Group(error_tokens, "target")

    target = Group(error_tokens, "target")

    regex = (Question(Lemma("what")) + Question(Lemma("be")) + Question(Pos("DT")) +
             Question(Lemma("meaning") | Lemma("mean")) + Question(Pos("IN")) + target + Question(Pos("."))) | \
            (Question(Lemma("what")) + Question(Lemma("be"))) + Question(Pos("DT")) +\
             Lemma("definition") + Pos("IN") + target + Question(Pos("."))

    def interpret(self, match):

        thing = match.target.tokens

        target = IsError() + ErrorIdOf(thing)
        meta = "errorNlg", "WHAT"

        return target, meta


class HowToFixError(QuestionTemplate):
    """
    Regex for questions like

    How to fix ora-00942? -- ok
    (?proper) way of fixing ora-00942? -- ok
    (?proper) steps to fixing ora-00942 -- ok
    """

    target = Group(error_tokens, "target")

    regex = Lemmas("how to") + Lemma("fix") + target + Question(Pos(".")) | \
            Question(Lemma("proper")) + Lemma("way") + Pos("IN") + Lemma("fix") + target + Question(Pos(".")) | \
        Question(Lemma("proper")) + Lemma("steps") + Lemma("to") + Lemma("fix") + target + Question(Pos("."))

    def interpret(self, match):
        thing = match.target.tokens
        target = IsError() + ErrorIdOf(thing)

        tip = HasErrorTip(target)
        meta = "errorStepNlg", "HOW"
        return tip, meta


class WhyError(QuestionTemplate):
    """
    Regex for questions like

    Why ora-00942? -- ok
    (?What is the) reason for ora-00942? -- ok
    """

    target = Group(error_tokens, "target")

    regex = (Group(Pos("WRB"), "wh") | Question(Group(Lemma("what"), "wh")) + Question(Lemma("be")) + Question(Pos("DT")) +
             Lemma("reason") + Pos("IN")) + target

    def interpret(self, match):
        thing = match.target.tokens
        target = IsError() + ErrorIdOf(thing)

        meta = "whyError", "WHY"
        return HasErrorCause(target), meta
