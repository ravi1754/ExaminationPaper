from nltk.corpus import words
import nltk
import numpy as np
import random
class Question(object):
    """Question class generates questions with all the attributes filled"""
    def __init__(self, subject, chapter, concepts,difficultyLevel,averageTime):
        self.IdealTime = averageTime
        self.DifficultyLevel = difficultyLevel
        self.Concepts = concepts
        self.Chapter = chapter
        self.Subject = subject
        self.Question = Question.GenerateQuestion()
        self.Options = Question.GenerateOptions()
        self.Answer = Question.GenerateAnswer(self.Options)

    @staticmethod
    def GenerateIdealTime():
        ## return a normal distrbution number i.e, ideal seconds for the completion 600 seconds on an average
        time = int(np.random.normal(600, 120))
        return time

    @staticmethod
    def GenerateDifficultyLevel():
      return random.randint(1,10)
    @staticmethod
    def GenerateQuestion():
        ## Generate Question
        numWords = random.randint(10,25)
        words = random.sample(nltk.corpus.words.words(),k = numWords)
        return " ".join(words)
    @staticmethod
    def GenerateOptions():
        return random.sample(nltk.corpus.words.words(), k = 4)
    @staticmethod
    def GenerateAnswer(options):
        return random.choice(options)




