# coding: utf-8

"""
Basic queries for nova quepy.
"""
from quepy.parsing import Lemma, Pos, QuestionTemplate, Particle, Token, Match, Lemmas, Tokens
from refo import Group, Question, Plus, Literal, Predicate, patterns
from dsl import IsError, ErrorIdOf, HasErrorTip, HasErrorCause, IsFile, FileOf, FileExtensionOf, FileLocation

error_tokens = Token("ORA00942") | Token("ORA00943")
file_tokens = Tokens("listener")
extension_tokens = Token("ora")


class WhatIsOraError(QuestionTemplate):
    """
    Regex for questions like

    What is ora-00942?
    What is the meaning of ora-00942?
    """

    target = Question(Pos("DT")) + Question(Lemma("meaning") + Pos("IN")) +\
        Group(error_tokens, "target")

    regex = Lemma("what") + Lemma("be") + target + Question(Pos("."))

    def interpret(self, match):

        thing = match.target.tokens

        target = IsError() + ErrorIdOf(thing)
        meta = "errorNlg", "What"

        return target, meta


class HowToFixError(QuestionTemplate):
    """
    Regex for questions like

    How to fix ora-00942?
    """

    target = Question(Pos("DT")) + Question(Lemma("meaning") + Pos("IN")) +\
             Group(Token("ORA00942"), "target")
    # regex = Pos("WRB") + Question(Pos("DT")) + Lemma("fix") + target
    regex = Lemmas("how to") + Lemma("fix") + target + Question(Pos("."))

    def interpret(self, match):
        thing = match.target.tokens
        target = IsError() + ErrorIdOf(thing)

        tip = HasErrorTip(target)
        meta = "errorStepNlg", "What"
        return tip, meta


class WhyError(QuestionTemplate):
    """
    Regex for questions like

    Why ora-00942?
    What is the reason for ora-00942
    """

    target = Group(Token("ORA00942"), "target")

    # regex =

    # target = Question(Pos("DT")) + Question(Lemma("meaning") + Pos("IN")) +\
    #     Group(Token("ORA00942"), "target")
    # wh_type = Group()
    # # regex = Pos("WRB") + Question(Pos("DT")) + Lemma("fix") + target
    regex = (Group (Pos("WRB"), "wh") | Group(Lemma("what"), "wh") + Lemma("be") + Question(Pos("DT")) +\
             Lemma("reason") + Pos("IN")) + target

    def interpret(self, match):
        thing = match.target.tokens
        target = IsError() + ErrorIdOf(thing)

        meta = "whyError", str(match.wh.tokens)
        return HasErrorCause(target), meta


class WhatIsFile(QuestionTemplate):
    """
    Regex for questions like

    What is Listener.ora
    """

    target = Group(file_tokens, "target_file_name") + Group(extension_tokens, "target_file_extension")

    regex = Lemma("what") + Lemma("be") + target + Question(Pos("."))

    def interpret(self, match):

        name = match.target_file_name.tokens
        extension = match.target_file_extension.tokens

        target = IsFile() + FileOf(name) + FileExtensionOf(extension)
        meta = "fileNlg", "What"

        return target, meta


class WhereIsFile(QuestionTemplate):
    """
    Regex for questions like

    Where is Listener.ora (?locate)
    What is the (?file) location of Listener.ora
    How to find Listener.ora
    """

    target = Group(file_tokens, "target_file_name") + Group(extension_tokens, "target_file_extension")

    regex = Lemma("how") + Lemma("to") + Lemma("find") + target + Question(Pos("."))

    def interpret(self, match):

        name = match.target_file_name.tokens
        extension = match.target_file_extension.tokens

        target = IsFile() + FileOf(name) + FileExtensionOf(extension)
        meta = "fileLocationNlg", "What", str(name+"."+extension)

        return FileLocation(target), meta
