# coding: utf-8

"""
Basic queries for nova quepy.
"""
from quepy.parsing import Lemma, Pos, QuestionTemplate, Particle, Token, Match, Lemmas, Tokens
from refo import Group, Question, Plus, Literal, Predicate, patterns
from dsl import IsError, ErrorIdOf, HasErrorTip, HasErrorCause, IsFile, FileOf, FileExtensionOf, FileLocation

errors = [line.rstrip('\n') for line in open('error_tokens')]
print errors

error_tokens = Token("")

for error in errors:
    error_tokens |= Token(error)

print error_tokens

# error_tokens = Token("ORA00942")
# print error_tokens

# error_tokens = Token("ORA00942") | Token("ORA00943") | Token("")

print error_tokens
file_tokens = Tokens("listener")
extension_tokens = Token("ora")


class WhatIsOraError(QuestionTemplate):
    """
    Regex for questions like

    What is ora-00942? -- ok
    What is the meaning of ora-00942? -- ok
    """

    target = Question(Pos("DT")) + Question(Lemma("meaning") + Pos("IN")) +\
        Group(error_tokens, "target")

    regex = Lemma("what") + Lemma("be") + target + Question(Pos("."))

    def interpret(self, match):

        thing = match.target.tokens

        target = IsError() + ErrorIdOf(thing)
        meta = "errorNlg", "WHAT"

        return target, meta


class HowToFixError(QuestionTemplate):
    """
    Regex for questions like

    How to fix ora-00942? -- ok
    """

    target = Question(Pos("DT")) + Question(Lemma("meaning") + Pos("IN")) +\
             Group(Token("ORA00942"), "target")
    # regex = Pos("WRB") + Question(Pos("DT")) + Lemma("fix") + target
    regex = Lemmas("how to") + Lemma("fix") + target + Question(Pos("."))

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
    What is the reason for ora-00942? -- ok
    """

    target = Group(Token("ORA00942"), "target")

    # regex =

    # target = Question(Pos("DT")) + Question(Lemma("meaning") + Pos("IN")) +\
    #     Group(Token("ORA00942"), "target")
    # wh_type = Group()
    # # regex = Pos("WRB") + Question(Pos("DT")) + Lemma("fix") + target
    regex = (Group(Pos("WRB"), "wh") | Group(Lemma("what"), "wh") + Lemma("be") + Question(Pos("DT")) +\
        Lemma("reason") + Pos("IN")) + target

    def interpret(self, match):
        thing = match.target.tokens
        target = IsError() + ErrorIdOf(thing)

        meta = "whyError", str(match.wh.tokens)
        return HasErrorCause(target), meta
