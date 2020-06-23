import Subject
import random
class Student(object):
    """description of class"""
    def __init__(self,id, subjects,Percent,category):
       self.Id = id
       self.Category = category
       self.subjectsToConceptMapping = Student.GenerateStudentKnownConcepts(subjects,Percent)
    @staticmethod
    def GenerateStudentKnownConcepts(subjects,Percent):
        subjectsToConceptMapping = {}
        for subject in subjects:
            concepts = list(subject.conceptsToChapterMapping.keys())
            subjectsToConceptMapping[subject.SubjectName] = random.choices(concepts,k=int(Percent*len(concepts)))
        return subjectsToConceptMapping
