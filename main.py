# coding: utf-8

"""
Main script for nova quepy.
"""

import quepy
import re
import sys
from lxml import etree
from SPARQLWrapper import SPARQLWrapper, JSON

regex_for_url = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

regex_for_error_code = re.compile(r'\b ora\W?\d{5}\b', re.I | re.M)
regex_for_oracle_file = re.compile(r'\b .*\W?(ora|log)\b', re.I | re.M)


sparql = SPARQLWrapper("http://127.0.0.1:3030/ds/query")
nova = quepy.install("nova")

root_type = ""
query_type = ""
file_name = ""


def print_define_for_error_nlg(results, target, metadata=None):
    root = etree.Element(root_type)

    question_type_tag = etree.Element("question_type")
    question_type_tag.text = question_type
    # root.append(question_type_tag)

    for result in results["results"]["bindings"]:
        if not regex_for_url.search(result["value"]["value"]):

            tag_name = str(result["property"]["value"]).split("#", 1)[1]
            tag_text = str(result["value"]["value"])

            if tag_name == "oraFileName":
                file_name = tag_text
                continue

            if tag_name == "fileExtension":
                tag_name = "fileName"
                tag_text = str(file_name) + "." + tag_text

            child = etree.Element(tag_name)
            child.text = tag_text
            root.append(child)

    print etree.tostring(question_type_tag, pretty_print=False) + etree.tostring(root, pretty_print=False)


def print_cause(results, target, metadata=None):
    root = etree.Element(root_type)

    question_type_tag = etree.Element("question_type")
    question_type_tag.text = question_type
    root.append(question_type_tag)

    for result in results["results"]["bindings"]:
        child = etree.Element("cause")
        child.text = str(result[target]["value"])
        root.append(child)

    print etree.tostring(root, pretty_print=False)


def print_file_location(results, target, metadata=None):
    root = etree.Element(root_type)

    question_type_tag = etree.Element("question_type")
    question_type_tag.text = question_type
    root.append(question_type_tag)

    for result in results["results"]["bindings"]:
        child = etree.Element("fileLocation")
        child.text = str(result[target]["value"])
        root.append(child)

    file_name_tag = etree.Element("fileName")
    file_name_tag.text = file_name
    root.append(file_name_tag)

    print etree.tostring(root, pretty_print=False)


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

if __name__ == "__main__":

    # question = "What is ora-00942"
    # question = "What is listener.ora"
    question = "How to fix ora-00942"
    question = question.replace("_", " ")
    # str(sys.argv[1].replace("_", " "))

    # questions = [
    #     "Why ora-00942"
    # ]

    # "What is ora-00942"
    # "What is the meaning of ora-00942"
    # "Why ora-00942"
    # "What is the reason for ora-00942"
    # "What is Listener.ora"

    print_handlers = {
        "errorNlg": print_define_for_error_nlg,
        "errorStepNlg": print_define_for_error_nlg,
        "whyError": print_cause,
        "fileNlg": print_define_for_error_nlg,
        "fileLocationNlg": print_file_location
    }

    if question:
        # print "question " + question
        # print "-" * len(question)

        # question = question.replace("-", "")
        # question = question.replace("ora", "ORA")

        if has_numbers(question):
            if regex_for_error_code.search(question):
                question = question.replace("-", "")
                question = question.replace("ora", "ORA")
                # print question

            else:
                print "type error code correctly"
                sys.exit(0)

        if regex_for_oracle_file.search(question):

            question = question.replace(".", " ")
            # print question

        print question

        target, query, metadata = nova.get_query(question)

        if isinstance(metadata, tuple):
            query_type = metadata[0]
            question_type = metadata[1]
            # if metadata[2]:
            #     file_name = metadata[2]
            # print query_type
            # print metadata
        else:
            query_type = metadata
            metadata = None

        if query is None:
            print "Sorry Question not Recognized :( \n"
            sys.exit(0)

        stringQuery = str(query)

        # print type(query_type)
        # print query_type

        if query_type == 'errorNlg' or query_type == 'fileNlg':
            query = stringQuery.replace("?x0", "?property ?value", 1)
            query = query.replace("}", "\t?x0 ?property ?value. \n}", 2)

            if query_type == 'errorNlg':
                root_type = "error"
            else:
                root_type = "file"

        if query_type == "errorStepNlg":
            query = stringQuery.replace("?x1", "?property ?value", 1)
            query = query.replace("}", "\t?x1 ?property ?value. \n}", 2)
            root_type = "steps"

        if query_type == "whyError":
            root_type = "Cause"

        if query_type == "fileLocationNlg":
            root_type = "fileLocation"

        print query

        if target.startswith("?"):
            target = target[1:]
        if query:
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()

            print results

            if not results["results"]["bindings"]:
                print "No answer found :("
                sys.exit(0)

        print
        print_handlers[query_type](results, target, metadata)
        print
