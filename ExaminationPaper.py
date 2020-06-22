import Question
import student
import Subject
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
def GetHistogram(df, colName,filePath):
    fig = plt.hist(df[colName])
    plt.savefig(filePath)
    plt.close()
def GetEstimatedTime(df, subjectName):
    return df.loc[df['subjects'] == subjectName]['time'].sum()/60
def GetAverageDifficultyLevel(df, subjectName):
    return df.loc[df['subjects']==subjectName]['difficultyLevel'].mean()
def GenerateExamAnalyis(questions):
	subjects = []
	time = []
	concepts =[]
	chapters = []
	difficultyLevel = []
	for question in questions:
		subjects.append(question.Subject.SubjectName)
		time.append(question.IdealTime)
		concepts.append(question.Concepts)
		difficultyLevel.append(question.DifficultyLevel)
		chapters.append(question.Chapter)
	df = pd.DataFrame({'subjects':subjects,'chapters':chapters,'difficultyLevel':difficultyLevel,'time':time,'concepts':concepts})
	f = open('ExaminationAnalysis.txt','w')
	f.write("Difficulty Level of the Examination:"+str(df['difficultyLevel'].mean())+'\n')
	f.write("Difficulty Level of the Mathematics Questions:"+str(GetAverageDifficultyLevel(df,"mathematics"))+'\n')
	f.write("Difficulty Level of the Physics Questions:"+str(GetAverageDifficultyLevel(df,"physics"))+'\n')
	f.write("Difficulty Level of the Chemistry Questions:"+str(GetAverageDifficultyLevel(df,"chemistry"))+'\n')
	f.write("Total estimated time for the Examination:"+str(df['time'].sum()/ 60)+' minutes \n')
	f.write("Estimated time for the Mathematics Questions:"+str(GetEstimatedTime(df,"mathematics"))+' minutes\n')
	f.write("Estimated time for the Physics Questions:"+str(GetEstimatedTime(df,"physics"))+' minutes\n')
	f.write("Estimated time for the Chemistry Questions:"+str(GetEstimatedTime(df,"chemistry"))+' minutes\n')
	f.close()
	GetHistogram(df,'time', 'TimeDistribution.png')
	GetHistogram(df, 'difficultyLevel','DifficultyLevelDistribution.png')
	GetHistogram(df, 'chapters','ChaptersDistribution.png')
	GetHistogram(df, 'concepts','ConceptsDistribution.png')
def GenerateDifficultLevel(questionsPerSubject):
	## 30 percent easy questions[1,2,3,4]
	## 30 percent medium questions[5,6,7]
	## rest of them Hard questions[8,9,10]
	easyCount = int(0.3*questionsPerSubject)
	mediumCount = int(0.3*questionsPerSubject)
	hardCount = questionsPerSubject- easyCount - mediumCount
	difficultLevels = random.choices([1,2,3,4],k = easyCount)+random.choices([5,6,7],k = mediumCount)+random.choices([8,9,10],k = hardCount)
	return difficultLevels
def GenerateAverageTime(difficultLevel):
	## easy [1,2,3,4] NormalDistribution with mean 60 sec var 10 sec
	## medium[5,6,7] NormalDistribution with mean 120 sec var 20 sec
	## hard [8,9,10] NormalDistribution with mean 200 sec var 30 sec
	easy = [1,2,3,4]
	medium = [5,6,7]
	averageTime = []
	for item in difficultLevel:
		if item in easy:
			averageTime.append(int(np.random.normal(60,10)))
		elif item in medium:
			averageTime.append(int(np.random.normal(120,20)))
		else:
			averageTime.append(int(np.random.normal(200,30)))
	return averageTime
def GenerateSubjectPaper(subject, questionsPerSubject):
	questions = []
	difficultLevel = GenerateDifficultLevel(questionsPerSubject)
	averageTime = GenerateAverageTime(difficultLevel)
	chapters = random.choices(subject.chapters,k = questionsPerSubject)
	for i in range(questionsPerSubject):
		concepts = random.choices(subject.chaptersToConceptMapping[chapters[i]], k =random.randint(3,6))
		concepts = ":".join(concepts)
		questions.append(Question.Question(subject, chapters[i],concepts,difficultLevel[i],averageTime[i]))
	return questions
def GenerateExaminationPaper():
	examinationQuestions = []
	subjects = []
	questionsPerSubject = 30
	mathematics = Subject.Subject("mathematics")
	subjects.append(mathematics)
	physics = Subject.Subject("physics")
	subjects.append(physics)
	chemistry = Subject.Subject("chemistry")
	subjects.append(chemistry)
	mathematicsQuestions = GenerateSubjectPaper(mathematics, questionsPerSubject)
	physicsQuestions = GenerateSubjectPaper(physics, questionsPerSubject)
	chemistryQuestions = GenerateSubjectPaper(chemistry, questionsPerSubject)
	examinationQuestions.extend(mathematicsQuestions)
	examinationQuestions.extend(physicsQuestions)
	examinationQuestions.extend(chemistryQuestions)
	return examinationQuestions, subjects
def WriteQuestionPaper(questionPaper):
    f = open("QuestionPaper.txt",'w')
    counter = 0
    for question in questionPaper:
        counter = counter + 1
        f.write(str(counter)+"."+question.Question+'\n')
        f.write('A.'+question.Options[0]+'\n')
        f.write('B.'+question.Options[1]+'\n')
        f.write('C.'+ question.Options[2]+'\n')
        f.write('D.'+question.Options[3]+'\n')
        f.write("************************\n")
    f.close()
def GenerateStudents(numOfStudents, subjects):
    students = []
## Categorize students into five ratings
## 1 rating    knows 20 percent of concepts
## 2 rating ..knows 40 percent of concepts
## 3.rating ...knows 60 percent of concepts
## 4 rating....knows 80 percent of concepts
## 5. rating ...knows 95 percent of concepts
    percentConcepts =[20,40,60,80,95]
    studentRating = random.choices(percentConcepts,k=numOfStudents)
    studentCategory = {20:'1',40:'2',60:'3',80:'4',95:'5'}
    for i in range(numOfStudents):
      studentObject = student.Student(str(i+1),subjects,studentRating[i],studentCategory[studentRating[i]])
      students.append(studentObject)
    return students
def ComputeTestTakingEvent(student, question):
    testTakingEvents = ['VQ','SAC','SA','SQ']
    knownConceptWeights = [0.1,0.1,0.7,0.1]
    unknownConceptWeights= [0.3,0.3,0.1,0.3]
    concepts = question.Concepts.split(':')
    subjectName = question.Subject.SubjectName
    if concepts <= student.subjectsToConceptMapping [subjectName]:
       return np.random.choice(testTakingEvents, p =knownConceptWeights)
    else:
       return np.random.choice(testTakingEvents, p = unknownConceptWeights)
def GetTestEventBarChart(dfStudent,colName,filePath,x_axis = 'testEvent'):
    ax = sns.catplot(x=x_axis,kind='count', hue=colName,data = dfStudent)
    ax.fig.savefig(filePath)
def GenerateStudentAnalysis(students, questionPaper):
    questionIdsList = []
    studentIdsList= []
    subjectsList = []
    testTakingEventList = []
    studentRatingList = []
    for studentObject in students:
        counter = 0
        for question in questionPaper:
            counter = counter + 1
            questionIdsList.append(counter)
            studentIdsList.append(studentObject.Id)
            subjectsList.append(question.Subject.SubjectName)
            testTakingEventList.append(ComputeTestTakingEvent(studentObject, question))
            studentRatingList.append(studentObject.Category)
    dfStudent =  pd.DataFrame({'studentId':studentIdsList,'questionId':questionIdsList,'subject':subjectsList,'testEvent':testTakingEventList,'category':studentRatingList})
    GetTestEventBarChart(dfStudent,'subject','StudentSubjectDistribution.png')
    GetTestEventBarChart(dfStudent,'category','StudentCategoryDistribution.png')
if __name__=="__main__":
    questionPaper, subjects = GenerateExaminationPaper()
    WriteQuestionPaper(questionPaper)
    GenerateExamAnalyis(questionPaper)
    numOfStudents = 300
    students = GenerateStudents(numOfStudents,subjects)
    GenerateStudentAnalysis(students, questionPaper)



