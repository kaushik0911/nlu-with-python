# coding: utf-8

"""
Basic queries for nova quepy.
"""
from quepy.parsing import Lemma, Pos, QuestionTemplate, Particle, Token, Match, Lemmas
from refo import Group, Question, Plus, Literal, Predicate, patterns

from dsl import IsError, ErrorIdOf, HasErrorTip, HasErrorCause


class ErrorCode(Particle):

    regex = Group((Pos("NN") | Pos("NNP") | Pos("NNS")) | Pos("VBN"), "target")

    def interpret(self, match):
        code = match.words.tokens
        return ErrorIdOf(code)


class WhatIsOraError(QuestionTemplate):
    """
    Regex for questions like

    What is ora-00942?
    What is the meaning of ora-00942?
    """

    target = Question(Pos("DT")) + Question(Lemma("meaning") + Pos("IN")) +\
             Group((Pos("NN") | Pos("NNP") | Pos("NNS")) | Pos("VBN"), "target")
    regex = Lemma("what") + Lemma("be") + target + Question(Pos("."))

    def interpret(self, match):
        thing = match.target.tokens
        target = IsError() + ErrorIdOf(thing)

        return target, "errorNlg"


class HowToFixError(QuestionTemplate):
    """
    Regex for questions like

    How to fix ora-00942?
    """

    target = Question(Pos("DT")) + Question(Lemma("meaning") + Pos("IN")) +\
             Group((Pos("NN") | Pos("NNP") | Pos("NNS")) | Pos("VBN"), "target")
    # regex = Pos("WRB") + Question(Pos("DT")) + Lemma("fix") + target
    regex = Lemmas("how to") + Lemma("fix") + target + Question(Pos("."))

    def interpret(self, match):
        thing = match.target.tokens
        target = IsError() + ErrorIdOf(thing)

        tip = HasErrorTip(target)

        return tip, "errorStepNlg"


class WhyError(QuestionTemplate):
    """
    Regex for questions like

    Why ora-00942?
    What is the reason for ora-00942
    """

    target = Question(Pos("DT")) + Question(Lemma("meaning") + Pos("IN")) +\
             Group((Pos("NN") | Pos("NNP") | Pos("NNS")) | Pos("VBN"), "target")
    # regex = Pos("WRB") + Question(Pos("DT")) + Lemma("fix") + target
    regex = (Pos("WRB") | Lemma("what") + Lemma("be") + Question(Pos("DT")) + Lemma("reason") + Pos("IN")) + target

    def interpret(self, match):
        thing = match.target.tokens
        target = IsError() + ErrorIdOf(thing)

        return HasErrorCause(target) , "whyError"
