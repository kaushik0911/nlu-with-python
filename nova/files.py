# coding: utf-8

"""
Files queries for nova quepy.
"""
from quepy.parsing import Lemma, Pos, QuestionTemplate, Particle, Token, Match, Lemmas, Tokens
from refo import Group, Question, Plus, Literal, Predicate, patterns
from dsl import IsError, ErrorIdOf, HasErrorTip, HasErrorCause, IsFile, FileOf, FileExtensionOf, FileLocation

error_tokens = Token("ORA00942") | Token("ORA01034") | Token("ORA12514") | Token("ORA12541") \
               | Token("ORA12543") + Token("ORA28000") + Token("ORA01652") | Token("ORA12502")
file_tokens = Tokens("listener")
extension_tokens = Token("ora")


class WhatIsFile(QuestionTemplate):
    """
    Regex for questions like

    What is Listener.ora (?file)? -- ok
    What is the meaning of Listener.ora (?file)? -- ok
    """

    target = Group(file_tokens, "target_file_name") + Group(extension_tokens, "target_file_extension")

    regex = Lemma("what") + Lemma("be") + Question(Pos("DT") + Lemma("meaning") + Pos("IN")) + target + \
            Question(Pos("."))

    def interpret(self, match):

        name = match.target_file_name.tokens
        extension = match.target_file_extension.tokens

        target = IsFile() + FileOf(name+"."+extension)
        meta = "fileNlg", "What"

        return target, meta


class WhereIsFile(QuestionTemplate):
    """
    Regex for questions like

    Where is Listener.ora (?locate)? -- ok
    What is the (?file) location of Listener.ora ((?file)? -- ok
    How to find Listener.ora? -- ok
    """

    target = Group(file_tokens, "target_file_name") + Group(extension_tokens, "target_file_extension")

    regex = (Lemmas("how to") + Lemma("find") + target + Question(Lemma("file"))) | \
            (Lemma("where") + Lemma("be") + target + Question(Lemma("file")) + Question(Lemma("locate"))) | \
            (Pos("WP") + Lemma("be") + Question(Pos("DT")) + Question(Lemma("file")) + Lemma("location") + Pos("IN") +
             target + Question(Lemma("file")))

    def interpret(self, match):

        name = match.target_file_name.tokens
        extension = match.target_file_extension.tokens

        target = IsFile() + FileOf(name+"."+extension)
        meta = "fileLocationNlg", "WHERE", str(name+"."+extension)

        return FileLocation(target), meta
