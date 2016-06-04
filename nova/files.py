# coding: utf-8

"""
Basic queries for nova quepy.
"""
from quepy.parsing import Lemma, Pos, QuestionTemplate, Particle, Token, Match, Lemmas, Tokens
from refo import Group, Question, Plus, Literal, Predicate, patterns
from dsl import IsError, ErrorIdOf, HasErrorTip, HasErrorCause, IsFile, FileOf, FileExtensionOf, FileLocation

error_tokens = Token("ORA00942") | Token("ORA00943")
file_tokens = Tokens("listener")
extension_tokens = Token("ora") | Token("log")


class WhatIsFile(QuestionTemplate):
    """
    Regex for questions like

    What is Listener.ora
    What is the meaning of Listener.ora
    """

    target = Group(file_tokens, "target_file_name") + Group(extension_tokens, "target_file_extension")

    regex = Lemma("what") + Lemma("be") + Question(Pos("DT") + Lemma("meaning") + Pos("IN")) + target + \
        Question(Pos("."))

    def interpret(self, match):

        name = match.target_file_name.tokens
        extension = match.target_file_extension.tokens

        target = IsFile() + FileOf(name) + FileExtensionOf(extension)
        meta = "fileNlg", "What"

        return target, meta


class WhereIsFile(QuestionTemplate):
    """
    Regex for questions like

    Where is Listener.ora (?locate) -- ok
    What is the (?file) location of Listener.ora
    How to find Listener.ora -- ok
    """

    target = Group(file_tokens, "target_file_name") + Group(extension_tokens, "target_file_extension")

    # regex = (Lemma("how") | Pos("WRB") | Lemma("what")) + Question(Pos("IN") | Lemma("be")) + \
    #     Question(Lemma("find") + Question(Pos("DT"))) + Question(Lemma("file")) +\
    #     Question(Lemma("location") + Pos("IN")) + target + Question(Lemma("locate")) + Question(Pos("."))

    # regex = Lemma("how to") + Lemma("find") + target

    # regex = Lemma("where") + Lemma("be") + target + Lemma("locate")

    # regex = Pos("WP") + Lemma("be") + Question(Pos("DT")) + Lemma("location") + Pos("IN") + target

    def interpret(self, match):

        name = match.target_file_name.tokens
        extension = match.target_file_extension.tokens

        target = IsFile() + FileOf(name) + FileExtensionOf(extension)
        meta = "fileLocationNlg", "Where", str(name+"."+extension)

        return FileLocation(target), meta
