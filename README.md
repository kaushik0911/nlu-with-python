# nova
# CDAP #ORACLE #2016

Natural Language Understanding

The Question and Answering component get user question as text input. User input is
restricted to English Language. That text, input go to set of regular expressions. If the
question matches with a regular expression it loads interpret method to get relationship
mapping from DSL file to construct query structure. Then generate SPARQL query,
embedded with question meta data and pass that query to the ontology. Retrieved data
from the ontology organized as a xml string.

repo
