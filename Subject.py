import random 
import string
class Subject(object):
    """description of class"""
    def __init__(self, SubjectName):
        self.SubjectName = SubjectName
        self.chapters = Subject.GenerateChapters(SubjectName)
        self.chaptersToConceptMapping, self.conceptsToChapterMapping = Subject.GenerateConcepts(SubjectName, self.chapters)
    @staticmethod
    def GenerateChapters(SubjectName):
        chaptersNum = random.randint(25,35)
        chapters = []
        for i in range(1,chaptersNum+1):
            chapterName = SubjectName[0:2]+"-"+"C"+str(i)
            chapters.append(chapterName)
        return chapters
    @staticmethod
    def GenerateConcepts(SubjectName,chapters):
        chaptersToConceptsMapping = {}
        conceptsToChapterMapping = {}
        commonConcepts = []
        for i in range(1,26):
            commonConcepts.append("CC"+str(i))
        for item in commonConcepts:
            conceptsToChapterMapping[item] = []
            conceptsToChapterMapping[item].extend(chapters)
        letters = list(string.ascii_uppercase)
        for chapter in chapters:
            chaptersToConceptsMapping[chapter]= commonConcepts
            speicificConceptNumbers = random.randint(70,78)
            for i in range(1,speicificConceptNumbers+1):
                concept =random.choice(letters)+random.choice(letters)+str(i)
                chaptersToConceptsMapping[chapter].append(concept)
                if concept in chaptersToConceptsMapping:
                   conceptsToChapterMapping[concept].append(chapter)
                else:
                   conceptsToChapterMapping[concept] = []
                   conceptsToChapterMapping[concept].append(chapter)
        return chaptersToConceptsMapping,conceptsToChapterMapping






