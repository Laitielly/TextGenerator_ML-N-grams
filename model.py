import random
import pickle
import re
import sys


class TextGenerator:
    # метод для проверки на существование файла
    # вообще питон сам выбросит исключение, но тут я хотела
    # показать умение работать с исключениями)
    @staticmethod
    def checkfile(file, method):
        try:
            f = open(file, method)
        except IOError:
            print(f'Не могу открыть {file}, пожалуйста, попробуйте снова')
            exit()
        else:
            return f

    # функция изменения текста (показываю работу
    # с функциями типа filter)
    @staticmethod
    def refactoring(text) -> list:
        rule = re.compile('[^а-яё0-9-]')
        text = rule.sub(' ', text).split(' ')

        return list(filter(None, text))

    # формируем "триплеты" для триграммы
    # (показываю работу с генераторами)
    @staticmethod
    def createtrigramms(listwords) -> tuple:
        w0, w1 = listwords[0], listwords[1]
        len_ = len(listwords)

        for i in range(3, len_):
            w2 = listwords[i]
            yield w0, w1, w2
            w0, w1 = w1, w2

    # основная функция обучения
    # проверяем наличие введеной директории, иначе вводим с консоли
    # до EOF
    # вызываем коррекцию текст, создаем триграммы и биграммы
    # создаем модель
    def fit(self, dirmodel, file=None) -> None:
        text = ''
        if file is None:
            print('Пожалуйста, введите свой текст:')
            for line in sys.stdin:
                text += line.lower()
        else:
            f = self.checkfile(file, 'r')
            for stroke in f:
                text += stroke.lower()
            f.close()

        readytext = self.refactoring(text)
        trigramms = self.createtrigramms(readytext)

        trigram, bigram = self.createbitri(trigramms)

        self.createmodel(trigram, dirmodel, bigram)

    # создание биграмм и триграмм (наша модель построена
    # на триграммах, биграммы нужны для вычисления
    # вероятности след слова)
    @staticmethod
    def createbitri(trigramms) -> tuple:
        bigram, trigram = {}, {}

        for w0, w1, w2 in trigramms:
            if (w0, w1) not in bigram:
                bigram[w0, w1] = 0
            bigram[w0, w1] += 1

            if (w0, w1, w2) not in trigram:
                trigram[w0, w1, w2] = 0
            trigram[w0, w1, w2] += 1

        return trigram, bigram

    # строим модель, заводим словарь типа
    # {(префикс1, префикс2):[(вероятное слово, вероятность)...],...}
    # сохраняем в файл обученную модель
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

    # функция генерации текста, вытаскиваем модель из файла
    # выбираем начало генерируемого текста в функции префикспроцессинг
    # если длина последовательности еще не достигнута, то генерируем текст
    def generate(self, dirmodel, prefix, length, seed=None) -> list:
        f = self.checkfile(dirmodel, 'rb')
        if f:
            model = pickle.load(f)
            f.close()

        if seed is not None:
            random.seed(seed)

        finaltext, initword = self.prefixprocessing(prefix, model)
        if initword is None:
            return list("Не могу сгенерировать последовательность с данной фразой :(".split(' '))

        len_ = len(finaltext)
        if length > len_:
            finaltext.append(initword[1])
            return self.createfinaltext(finaltext, initword, length, model, len_)
        return finaltext

    # если перфикс есть, то берем последнее слово и ищем кортеж
    # с данным словом, иначе берем рандомно
    @staticmethod
    def prefixprocessing(prefix, model) -> (list, tuple):
        initword, finaltext = None, []

        if prefix:
            finaltext = prefix.lower().split(' ').copy()
            last = finaltext[-1]

            for word in model.keys():
                if last in word and word[0] == last:
                    initword = word
                    return finaltext, initword

        return finaltext, random.choice(list(model.keys()))

    # генерация текста с выбором последующего слова с учетом
    # вероятностных весов, если кортежа нет в модели, то берем след
    # слово рандомно
    @staticmethod
    def createfinaltext(finaltext, curr, length, model, len_) -> list:
        for i in range(length - len_ - 2):
            next_ = random.choices([word for (word, freq) in model[curr]],
                                   weights=[freq for (word, freq) in model[curr]])
            finaltext.append(next_[0])
            curr = (curr[1], next_[0]) if (curr[1], next_[0]) in model else random.choice(list(model.keys()))

        return finaltext

# модель можно было описать меньшим кол-вом действий, но я старалась показать
# свои познания в работе с питоном
