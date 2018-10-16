import numpy as np
import operator


class Recommendation:
    data = []
    context_day = []
    context_place = []
    grades = {}
    k = 7

    def __init__(self, data, context1, context2):
        self.data = np.array(data, ndmin=2, dtype=np.float)
        self.context_day = np.array(context1)
        self.context_place = np.array(context2)

    # Определяем сходство пользователя u с v
    def sim(self, u: int, v: int):
        nomerator = 0
        denominator1 = 0
        denominator2 = 0
        for i in range(len(self.data[0])):
            if self.data[u][i] != -1 and self.data[v][i] != -1:
                nomerator += self.data[u][i] * self.data[v][i]
                denominator1 += self.data[u][i] ** 2
                denominator2 += self.data[v][i] ** 2

        result = nomerator / (np.sqrt(denominator1) * np.sqrt(denominator2))
        return result

    # Выбираем 7 наиболее похожих на данного пользователя
    def mostSimilars(self, u):
        needed = []
        for v in range(0, len(self.data)):
            if u != v:
                needed.append((v, self.sim(u, v)))

        needed = sorted(needed, key=operator.itemgetter(1), reverse=True);
        return needed

    # считаем оценку фильма i для пользователя u
    def rui(self, u, i):
        result = 0
        nominator = 0
        denominator = 0

        # Считаем среднее для u
        ru = self.avg(u)

        # Находим 7 максимально похожих на u
        similar = self.mostSimilars(u)

        counter = 0
        # Проходим по каждому похожему
        for v in similar:

            if self.data[v[0]][i] != -1:
                rv = self.avg(v[0])
                nominator += v[1] * ((self.data[v[0]][i]) - rv)
                denominator += np.abs(v[1])
                if counter < self.k - 1:
                    counter += 1
                else:
                    result = nominator / denominator + ru
                    return result

    # Среднее значение оценок фильмов для пользователя u без учета непросмотренных
    def avg(self, u):
        res = 0
        counter = 0
        for i in self.data[u]:
            if i != -1:
                res += i
                counter += 1
        return res / counter

    # Проходимся по каждому пользователю и добавляем оценку фильму, который он не смотрел
    def fillEmpty(self):
        string = ""
        res = ""
        best = {}
        for u in range(len(self.data)):
            string = '\n"user": ' + str(u + 1) + ",\n"
            string += '"' + '1' + '": {\n'
            for i in range(len(self.data[u])):
                if self.data[u][i] == -1:
                    string += '     "movie ' + str(i + 1) + '": ' + str(round(self.rui(u, i), 3)) + ",\n"

                    if not (u + 1 in self.grades):
                        self.grades[u + 1] = {}
                    self.grades[u + 1]["movie " + str(i + 1)] = round(self.rui(u, i), 3)
            string = string.rstrip(',\n')
            string += "\n},\n" + '"2": {\n'

            # Подбираем фильм для просмотра дома в выходной - оценка выше среднего у других пользователей, которые смотрели этот фильм также
            # в выходной дома
            similar = self.mostSimilars(u)
            for v in similar:
                if u + 1 in best: break
                for i in range(len(self.data[u])):
                    if self.data[u][i] == -1 and self.context_place[v[0]][i] == " h" and \
                            (self.context_day[v[0]][i] == " Sat" or self.context_day[v[0]][i] == " Sun") and \
                            self.data[v[0]][i] > self.avg(v[0]):
                        best[u + 1] = "movie: " + str(i + 1)
                        string += '     "movie ' + str(i + 1) + '": ' + str(
                            self.grades[u + 1]['movie ' + str(i + 1)]) + '\n     },'
                        break
            res += string
        return res

    def recommend(self):
        result = self.fillEmpty()
        with open("grades.json", 'w') as file:
            file.write('{\n' + result.rstrip(',') + '\n\n}')

        #print(self.grades)
