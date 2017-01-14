from collections import Counter

class StrawPoll(object):

    def __init__(self, creator, question, superusers=set()):
        self.creator = creator
        self.superusers = superusers
        self.question = question
        self.votes = {}
        self.counter = Counter()

    def vote(self, name, response):
        previous = self.votes.get(name)
        if previous is not None:
            self.counter[previous] -= 1

        self.votes[name] = response
        self.counter[response] += 1

    def tally(self):
        totals = self.counter.most_common()
        winner = totals[0][0]
        return totals, winner

    def canend(self, user):
        return user in self.superusers or user in self.creator
