# nova
# CDAP #ORACLE #2016

## Natural Language Understanding ##

The Question and Answering component get user question as text input. User input is
restricted to English Language. That text, input go to set of regular expressions. If the
question matches with a regular expression it loads interpret method to get relationship
mapping from DSL file to construct query structure. Then generate SPARQL query,
embedded with question meta data and pass that query to the ontology. Retrieved data
from the ontology organized as a xml string.

repo
----

> **Question**
Wht is the meanig of ora-00942?
 
 > **After correction**
What is the meaning of ora-00942?

**query out**

	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	PREFIX ora:<https://localhost/orafixing.owl#>
	SELECT DISTINCT ?property ?value WHERE{
		?x0 rdf:type ora:ORA-Error.
		?x0 ora:error_id "ORA12541".
		?x0 ?property ?value.
	}

