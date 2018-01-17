'''Athanasios Anastasiou, Jan 2018

The main file that attempts to create and recall data from a schema that 
has been defined by neomodel.

It demonstrates the problem with inheritance.
'''

import os
import datetime
import neomodel
import models

if __name__ == "__main__":
    #Set up 
    neo4jUsername = os.environ['NEO4J_USERNAME']
    neo4jPassword = os.environ['NEO4J_PASSWORD']
    dbConURI = "bolt://{uname}:{pword}@localhost:7687".format(uname=neo4jUsername, pword=neo4jPassword)
    
    #This must be called before any further calls to neomodel.
    neomodel.db.set_connection(dbConURI)
    
    #Create some entities in the data
    A = models.specificModelClass1(someAttribute="Alpha", someOtherAttribute = datetime.datetime.now()).save()
    
    B = models.specificModelClass2(anAttribute = "Bonkers", anotherAttribute = "Dizzie Rascal").save()
    C = models.specificModelClass3(anAttribute = "Heavy", yetAnotherAttribute = "Metal").save()
    
    #This does not complain
    A.someLink.connect(B)
    A.someLink.connect(C)
    
    del(A,B,C)
    
    #Recall an A object
    A = models.specificModelClass1.nodes.get(someAttribute = "Alpha")
    
    #So far so good, but let's now look at someLink
    for anObject in A.someLink:
        print(type(anObject))
    
    #An assertion on the type of the objects to be specificModelClass2 and specificModelClass3 
    #would fail right here.
    #
    #This indeed shows two objects but they have both already been instantiated to 
    #models.baseModelClass2.
    #
    #Unfortunately, it is now impossible to re-cast them to specificModelClass2, specificModelClass3 
    #without re-querying the database
    #
    #More importantly, baseModelClass2 does not even contain the fields of specificModelClass2. 
    #Although the entity does have them, these are not marshalled in Python because neomodel instantiates 
    #to the actual class of the link rather than the FAMILY of classes implied by the generalisation.
