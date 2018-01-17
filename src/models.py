'''Athanasios Anastasiou Jan 2018

In this file an abstract and a concrete schema are defined using Neomodel's facilities.

The definitions within this file, pose absolutely no problem. But the way they are interpreted, 
points to a narrow interpretation of inheritance.
'''

import neomodel

#Set up a core schema for the domain.
#From a modeling point of view, most of these classes would be considered Abstract but they are not 
#    marked as such in neomodel to preserve all the labels of the nodes that determine a class' lineage.
class baseModelRelationship(neomodel.StructuredRel):
    '''Models a relationship between baseModelClass1 and baseModelClass2'''
    theAttr = neomodel.StringProperty()
    
class baseModelClass1(neomodel.StructuredNode):
    '''Models a very simple node with an undirected 0..* relationship to a set of baseModelClass2 nodes'''
    someAttribute = neomodel.StringProperty(unique_index=True)
    someLink = neomodel.Relationship("baseModelClass2", "RELATED_TO", model = baseModelRelationship)
    
class baseModelClass2(neomodel.StructuredNode):
    '''Models a very simple node that is related to baseModelClass1'''
    anAttribute = neomodel.StringProperty(index = True)    

  
#Further down the line, the schema is specialised to entities that are particular to a specific part of the domain
class specificModelClass1(baseModelClass1):
    '''Models a class that is a specialisation of baseModelClass1
    
    NOTE:
        This class inherits the someLink relationship.
        Notice here that we are not re-specifying someLink
        to be pointing to specificModelClass2
    '''
    someOtherAttribute = neomodel.DateTimeProperty()
    
class specificModelClass2(baseModelClass2):
    '''Models a class that is a specialisation of baseModelClass2
    
    NOTE:
        This class is a specialisation of baseModelClass2, therefore it is perfectly 
        valid to be "attached" at someLink. 
    '''
    anotherAttribute = neomodel.StringProperty(unique_index = True)
    
class specificModelClass3(baseModelClass2):
    '''Models another class that is a specialisation of baseModelClass2
    
    NOTE:
        This class is a specialisation of baseModelClass2, therefore it is also perfectly valid 
        as an "attachment" to someLink
    '''
    yetAnotherAttribute = neomodel.StringProperty(index = True)
