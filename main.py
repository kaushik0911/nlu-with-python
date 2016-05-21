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


sparql = SPARQLWrapper("http://127.0.0.1:3030/ds/query")
nova = quepy.install("nova")

classType = ""


def print_define_for_nlg(results, target, metadata=None):
    root = etree.Element("root")

    for result in results["results"]["bindings"]:
        if not regex_for_url.search(result["value"]["value"]):
            child = etree.Element(str(result["property"]["value"]).split("#", 1)[1])
            child.text = str(result["value"]["value"])
            root.append(child)

    print etree.tostring(root, pretty_print=False)


def print_cause(results, target, metadata=None):
    root = etree.Element("root")

    for result in results["results"]["bindings"]:
        child = etree.Element("cause")
        child.text = str(result[target]["value"])
        root.append(child)

    print etree.tostring(root, pretty_print=False)


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

if __name__ == "__main__":

    question = str(sys.argv[1].replace("_", " "))

    # questions = [
    #     "Why ora-00942"
    # ]

    # "What is ora-00942"
    # "What is the meaning of ora-00942"
    # "Why ora-00942"
    # "What is the reason for ora-00942"

    print_handlers = {
        "errorNlg": print_define_for_nlg,
        "errorStepNlg": print_define_for_nlg,
        "whyError": print_cause
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

        target, query, metadata = nova.get_query(question)

        if isinstance(metadata, tuple):
            query_type = str(metadata[0])
            metadata = metadata[1]
            # print query_type
        else:
            query_type = metadata
            metadata = None

        if query is None:
            print "Sorry Question not Recognized :( \n"
            sys.exit(0)

        stringQuery = str(query)

        if query_type is "errorNlg":
            query = stringQuery.replace("?x0", "?property ?value", 1)
            query = query.replace("}", "\t?x0 ?property ?value. \n}", 2)
            classType = ""

        if query_type is "errorStepNlg":
            query = stringQuery.replace("?x1", "?property ?value", 1)
            query = query.replace("}", "\t?x1 ?property ?value. \n}", 2)
            classType = ""

        # print query

        if target.startswith("?"):
            target = target[1:]
        if query:
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()

            # print results

            if not results["results"]["bindings"]:
                print "No answer found :("
                sys.exit(0)

        print_handlers[query_type](results, target, metadata)
        print
