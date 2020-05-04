from . import custom_exceptions
from . import users

subjects = {}
quests = {}


class Subject:
    def __init__(self, name, levels, quest_per_level):
        """
        name will be the name of the subject. 
        levels will be how many levels in in the subject. 
        quest_per_level is the amount of questions per level.
        """

        self.name = name.lower()
        self.levels = levels
        self.quest_per_level = quest_per_level

        self.__make_subject_dict()
    
    def new_quest(self, level, question, answer):
        """Adds a new question to subject_dict."""

        if level > self.levels:
            raise custom_exceptions.LevelIsTooBig()

        questions_dict = self.subject_dict[self.subject_dict[self.name + '_ranks'][level - 1]]['questions']
        
        if len(questions_dict.keys()) > self.quest_per_level:
            raise custom_exceptions.TooManyQuestionsInOneLevel()

        if question in questions_dict:
            raise custom_exceptions.QuestionAlreadyExists()

        self.subject_dict[self.subject_dict[self.name + '_ranks'][level - 1]]['questions'][question] = str(answer)
    
    def rm_quest(self, level, question):
        """Removes a question from subject_dict."""

        questions_dict = self.subject_dict[self.subject_dict[self.name + '_ranks'][level - 1]]['questions']
        
        if level > self.levels:
            raise custom_exceptions.LevelIsTooBig()

        if question not in questions_dict:
            raise custom_exceptions.QuestionDoesNotExists()

        del questions_dict[question]

    def get_quest_answer(self, id_):
        """Returns the question and the answer to a question."""

        user = users.users[id_]
        subject = user['subject']

        # The dictionary containing all the questions and their answers.
        quest_answers = quests[subject][user['subject-level']]['questions']
        
        questions = list(quest_answers.keys())

        question = questions[user['points']]
        answer = quest_answers[question]
        
        return [question, answer]

    def __make_subject_dict(self):
        subject_dict = {}
        ranks = [self.name]

        levels = range(2, self.levels + 1)

        subject_dict[self.name] = {
            'questions': {}
        }

        for level in levels:
            level_name = self.name + ' level ' + str(level)

            ranks.append(level_name)
            subject_dict[level_name] = {
                'questions': {}
            }
        
        subject_dict[self.name + '_ranks'] = ranks

        self.subject_dict = subject_dict
