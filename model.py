import random
import pickle
import re


class TextGenerator:
    @staticmethod
    def refactoring(text) -> list:
        rule = re.compile('[^а-яё0-9-]')
        text = rule.sub(' ', text).split(' ')

        return list(filter(None, text))

    @staticmethod
    def createtrigramms(listwords):
        w0, w1 = listwords[0], listwords[1]
        len_ = len(listwords)

        for i in range(3, len_):
            w2 = listwords[i]
            yield w0, w1, w2
            w0, w1 = w1, w2

    def fit(self, readytext, dirmodel) -> None:
        text = self.refactoring(readytext)
        trigramms = self.createtrigramms(text)

        bigram, trigram = {}, {}

        for w0, w1, w2 in trigramms:
            if (w0, w1) not in bigram:
                bigram[w0, w1] = 0
            bigram[w0, w1] += 1

            if (w0, w1, w2) not in trigram:
                trigram[w0, w1, w2] = 0
            trigram[w0, w1, w2] += 1
        self.createmodel(trigram, dirmodel, bigram)

    @staticmethod
    def createmodel(trigram, dirmodel, bigram) -> None:
        model = {}
        for (w0, w1, w2), freq in trigram.items():
            if (w0, w1) in model:
                model[w0, w1].append((w2, freq/bigram[w0, w1]))
            else:
                model[w0, w1] = [(w2, freq / bigram[w0, w1])]

        f = open(dirmodel, 'wb')
        pickle.dump(model, f)
        f.close()

    def generate(self, dirmodel, prefix, length) -> list:
        f = open(dirmodel, 'rb')
        model = pickle.load(f)
        f.close()

        finaltext, initword = self.prefixprocessing(prefix, model)
        if initword is None:
            return list("Sorry, but generator cannot create smth with this phrase :(".split(' '))

        return self.createfinaltext(finaltext, initword, length, model)

    @staticmethod
    def prefixprocessing(prefix, model):
        initword, finaltext = None, []

        if prefix:
            finaltext = prefix.lower().split(' ').copy()[:-1:]
            last = finaltext[-1]

            for word in model.keys():
                if last in word and word[0] == last:
                    initword = word
                    return finaltext, initword

        return finaltext, random.choice(list(model.keys()))

    @staticmethod
    def createfinaltext(finaltext, initword, length, model):
        finaltext.append(initword[0])
        len_ = len(finaltext)
        if length > len_:
            finaltext.append(initword[1])
            next_ = random.choice(model[initword])
            curr = initword

            for i in range(length - len_ - 2):
                finaltext.append(next_[0])
                curr = (curr[1], next_[0])
                next_ = random.choice(model[curr])

        return finaltext