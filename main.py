# coding: utf-8

"""
Main script for nova quepy.
"""

import quepy
import re
import sys
from SPARQLWrapper import SPARQLWrapper
from spelling import correct
from xml_converter import print_cause, print_define_for_error_nlg,print_file_location
# regex for validate inputs and outputs

regex_for_error_code = re.compile(r'\b ora\W?\d{5}\b', re.I | re.M)
regex_for_oracle_file = re.compile(r'\b .*\W?(ora|log)\b', re.I | re.M)

# onto url
sparql = SPARQLWrapper("http://localhost:3030/ds/query")
nova = quepy.install("nova")

root_type = ""
query_type = ""
file_name = ""
error_no = ""
target_keyword = ""
question_type = ""


def has_numbers(input_String):
    return any(char.isdigit() for char in input_String)

if __name__ == "__main__":

    """
    Questions that can ask from the system

    What is ora-00942? -- ok
    What is the meaning of ora-00942? -- ok
    what is meant by ora-00942? -- ok ! check question pattern
    (?What is) definition of ora-00942? -- ok

    How to fix ora-00942? -- ok
    (?proper) way of fixing ora-00942? -- ok
    (?proper) steps to fixing ora-00942 -- ok

    Why ora-00942? -- ok
    (?What is the) reason for ora-00942? -- ok

    What is the meaning of listener.ora -- ok

    Where is listener.ora (?file) locate -- ok
    How to find listener.ora (?file) -- ok
    """

    # question = "What is ORA12541"
    # question = "What is the meaning of ORA12541"

    # question = "What is meant by ora-00942"
    # question = "definition of ora-00942"
    # question = "What is the meaning of listener.ora"
    # question = "How to fix ora-00942"
    # question = "steps to fix ora-00942"
    # question = "proper way of fix ora-00942?"
    # question = "proper steps to fix ora-00942"
    # question = "Why ora-00942"
    # question = "what is the reason for ora-00942"
    # question = "what is the location of listener.ora file"
    question = "how to find listener.ora"
    # question = "Where is listener.ora locate"
    # question = "What is the meaning of listener.ora"
    # question = "What is listener.ora"

    # question = question.replace("_", " ")

    # question = str(sys.argv[1].replace("_", " "))
    question = question.lower()

    word_list = question.split()
    question = ""

    for word in word_list:
        question += correct(word) + " "

    # print question

    # print functions
    print_handlers = {
        "errorNlg": print_define_for_error_nlg,
        "errorStepNlg": print_define_for_error_nlg,
        "whyError": print_cause,
        "fileNlg": print_define_for_error_nlg,
        "fileLocationNlg": print_file_location
    }

    if question:

        # check whether question contains error number
        # if has , remove unnecessary parts and suit according to the ontology
        if has_numbers(question):

            # check error code typed correctly
            if regex_for_error_code.search(question):
                question = question.replace("-", "")
                question = question.replace("ora", "ORA")
                target_keyword = "ORA-"+question.split('ORA')[1][0:5]
                # target_keyword = error_no

            else:
                print "Please type error code correctly. eg :- ora00942"
                sys.exit(0)

        # if question ask about a db file
        # following will check if file name typed correctly
        elif regex_for_oracle_file.search(question):
            question = question.replace(".", " ")

        # print question

        # received the generate the query according to the asked question
        target, query, metadata = nova.get_query(question)

        # get all meta data if any
        if isinstance(metadata, tuple):
            query_type = metadata[0]
            question_type = metadata[1]
            if len(metadata) == 3 and metadata[2]:
                target_keyword = metadata[2]

        else:
            query_type = metadata
            metadata = None

        # if query not build
        # means asked question not appropriately typed or not valid for the domainS
        if query is None:
            print "Sorry Question not Recognized. May be out of domain."
            sys.exit(0)

        stringQuery = str(query)

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
            root_type = "error"

        if query_type == "fileLocationNlg":
            root_type = "file"

        # print query

        print query.replace("\n", " ")
        print question_type
        print root_type
        print query_type

        if target_keyword:
            print target_keyword

        print question

        # if target.startswith("?"):
        #     target = target[1:]
        # if query:
        #     sparql.setQuery(query)
        #     sparql.setReturnFormat(JSON)
        #     results = sparql.query().convert()
        #
        #     print results
        #
        #     if not results["results"]["bindings"]:
        #         print "No answer found :("
        #         sys.exit(0)
        #
        # print_handlers[query_type](results, target, root_type, question_type, target_keyword)
