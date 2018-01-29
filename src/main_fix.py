'''Athanasios Anastasiou, Jan 2018

A potential fix for the inheritance issue of neomodel.

The main idea is to create a lookup dictionary that maps a set of labels to the class to be inflated
'''

import os
import datetime
import neomodel
import models

def createLookupDict(classList):
    '''Creates a lookup dictionary of the labels that denote a particular class in a class hierarchy'''
    lookupDict = {}
    for aClassDef in classList:
        if issubclass(aClassDef, neomodel.StructuredNode):
            lookupDict[frozenset(aClassDef.inherited_labels())] = aClassDef
    return lookupDict
    
def node2Instance(lookupDict, nodeResultSet):
    '''Converts the results of a cypher query to model instances based on their labels'''
    returnResults = []
    for aResultRow in nodeResultSet:
        temp = []
        for anItem in aResultRow:
            temp.append(lookupDict[frozenset(anItem.labels)].inflate(anItem))
        returnResults.append(temp)
    return returnResults
    
if __name__ == "__main__":
    #The setup is exactly the same as the main.py. It only stores data for a few entities in the database
    #Set up 
    neo4jUsername = os.environ['NEO4J_USERNAME']
    neo4jPassword = os.environ['NEO4J_PASSWORD']
    dbConURI = "bolt://{uname}:{pword}@localhost:7687".format(uname=neo4jUsername, pword=neo4jPassword)
    
    #This must be called before any further calls to neomodel.
    neomodel.db.set_connection(dbConURI)
    
    #Uncomment to create data
    ##Create some entities in the data
    #A = models.specificModelClass1(someAttribute="Alpha", someOtherAttribute = datetime.datetime.now()).save()
    #
    #B = models.specificModelClass2(anAttribute = "Bonkers", anotherAttribute = "Dizzie Rascal").save()
    #C = models.specificModelClass3(anAttribute = "Heavy", yetAnotherAttribute = "Metal").save()
    #    
    ##This does not complain
    #A.someLink.connect(B)
    #A.someLink.connect(C)
    #
    #del(A,B,C)
    
    #Potential solution
    #
    #Create a lookup dictionary which maps a **SET** of labels to the actual class to instantiate.
    #The set of labels is already available to us via inherited_labels provided by neomodel.
    #
    #NOTE: It is not necessary to create a lookup of ALL the classes defined in a package.
    luDict = createLookupDict([models.baseModelClass1, models.baseModelClass2, models.specificModelClass1, models.specificModelClass2, models.specificModelClass3])
    
    #Now, create a query that can return mixed results. Neomodel returns a list of Neo4j.Node in this case
    U = neomodel.db.cypher_query("match (a) where id(a) in [2,4,6,8,10] return a")
    #Convert the Node objects to model objects
    V = insightCoreFunctionality.node2Instance(luDict, results)
    
    #This does not represent a complete fix because:
    # 1. It is not part of StructuredNode or StructredRel
    # 2. It does not perform a check against a particular class / type
    #
    # Number 2 is easily solved by checking that the labels of the class 
    #at the end of a relationship are a subset of the labels of the 
    #object that is about to be instantiated from the db
    
