from lxml import etree
import re

regex_for_url = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
    r'localhost|'  # localhost
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ip
    r'(?::\d+)?'  # port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def print_define_for_error_nlg(results, target, root_type=None, question_type=None, Empty= None):
    """
    This function create xml for error definition or oracle file definition.

    xml contains question_type tag to recognise the WH question type for NLG
    root tag identify the information inside the xml
    """
    count = 0
    root = etree.Element(root_type)

    question_type_tag = etree.Element("question_type")
    question_type_tag.text = question_type

    # loop through the JSON and gather all information out from the query
    for result in results["results"]["bindings"]:
        if not regex_for_url.search(result["value"]["value"]):

            # naming the tag and put values into it
            tag_name = str(result["property"]["value"]).split("#", 1)[1]
            tag_text = str(result["value"]["value"])

            if tag_name == "oraFileName":
                file_name = tag_text
                continue

            if tag_name == "fileExtension":
                tag_name = "fileName"
                tag_text = str(file_name) + "." + tag_text

            # append data
            child = etree.Element(tag_name)
            child.text = tag_text
            root.append(child)

    # print xml
    print etree.tostring(question_type_tag, pretty_print=False) + etree.tostring(root, pretty_print=False)


def print_cause(results, target, root_type=None, question_type=None, error_no=None):
    """
    This function create xml for error cause.
    """

    root = etree.Element(root_type)

    question_type_tag = etree.Element("question_type")
    question_type_tag.text = question_type

    for result in results["results"]["bindings"]:
        child = etree.Element("caused_due_to")
        child.text = str(result[target]["value"])
        root.append(child)

    error_name_tag = etree.Element("error_id")
    error_name_tag.text = error_no
    root.append(error_name_tag)

    print etree.tostring(question_type_tag, pretty_print=False) + etree.tostring(root, pretty_print=False)


def print_file_location(results, target, root_type=None, question_type=None, file_name=None):
    """
    This function create xml for oracle db file location.
    """
    root = etree.Element(root_type)

    question_type_tag = etree.Element("question_type")
    question_type_tag.text = question_type
    # root.append(question_type_tag)

    for result in results["results"]["bindings"]:
        child = etree.Element("located_in")
        child.text = str(result[target]["value"])
        root.append(child)

    file_name_tag = etree.Element("file_name")
    file_name_tag.text = file_name
    root.append(file_name_tag)

    print etree.tostring(question_type_tag, pretty_print=False) + etree.tostring(root, pretty_print=False)
