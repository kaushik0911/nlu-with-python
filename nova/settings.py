# coding: utf-8

# This setting file provide access to NLTK and Quepy Framework
# All SPARQL prefixes can give under "SPARQL_PREAMBLE"

"""
Settings.
"""

# Generated query language
LANGUAGE = "sparql"

# NLTK config
NLTK_DATA_PATH = ["/home/shamantha/nltk","/root/nltk_data"]  # List of paths with NLTK data

# Encoding config
DEFAULT_ENCODING = "utf-8"

# Sparql config
SPARQL_PREAMBLE = u"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ora:<http://www.semanticweb.org/saranga/orafixer#>
"""
