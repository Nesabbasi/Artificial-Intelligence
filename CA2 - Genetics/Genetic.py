import random
import time
import copy

populationSize = 100
carryPercentage = 0.1
crossoverProbability = 0.1


class EquationBuilder:

    def __init__(self, operators, operands, equationLength, goalNumber):
        self.operators = operators
        self.operands = operands
        self.equationLength = int(equationLength)
        self.goalNumber = int(goalNumber)
        self.population = self.makeFirstPopulation()

    def update(self):
        data = []
        for j in range(populationSize):
            finalNumber = eval(''.join(self.population[j]['stringOps']))
            data.append({'stringOps': self.population[j]['stringOps'],
                        'answer': finalNumber,
                        'difference': 0})
        self.population = data

    def makeFirstPopulation(self):
        numberOfOperands = int(self.equationLength / 2) + 1
        numberOfOperators = self.equationLength - numberOfOperands
        data = []
        for j in range(populationSize):
            randomOperands = random.choices(self.operands, k=numberOfOperands)
            randomOperators = random.choices(self.operators, k=numberOfOperators)
            stringOps = []
            for i in range(numberOfOperators):
                stringOps.append(randomOperands[i])
                stringOps.append(randomOperators[i])
            stringOps.append(randomOperands[numberOfOperands - 1])
            finalNumber = eval(''.join(stringOps))
            data.append({'stringOps': stringOps,
                        'answer': finalNumber,
                        'difference': 0})
        return data

    def createMatingPool(self):
        matingPool = []
        for i in range(populationSize):
            for j in range(populationSize - i):
                matingPool.append(self.population[i])
        return matingPool

    def createCrossoverPool(self, matingPool):
        crossoverPool = []
        for i in range(len(matingPool)):
            if random.random() > crossoverProbability:
                crossoverPool.append(matingPool[i])
            else:
                idx0 , idx1 = random.sample(range(len(matingPool)), 2)
                rand = random.randint(0, self.equationLength - 1)
                for j in range(rand):
                    temp = matingPool[idx0]['stringOps'][j]
                    matingPool[idx0]['stringOps'][j] = matingPool[idx1]['stringOps'][j]
                    matingPool[idx1]['stringOps'][j] = temp
                crossoverPool.append(matingPool[i])
        return crossoverPool

    def mutate(self, chromosome):
        rand = random.randint(0, self.equationLength - 1)
        if rand % 2:
            randVar = random.choices(self.operators, k=1)
            chromosome['stringOps'][rand] = randVar[0]
        else:
            randVar = random.choices(self.operands, k=1)
            chromosome['stringOps'][rand] = randVar[0]

        return chromosome

    def findEquation(self):
        count = 0
        while (True):
            random.shuffle(self.population)
            if count != 0:
                self.update()
            isFind = False
            for i in range(populationSize):
                self.population[i]['difference'] = abs(self.goalNumber - self.population[i]['answer'])
                if self.population[i]['answer'] == self.goalNumber:
                    print(''.join(self.population[i]['stringOps']))
                    isFind = True
                    break

            if isFind:
                break

            self.population = sorted(self.population, key=lambda d: d['difference'], reverse=False)

            carriedChromosomes = []
            for i in range(int(populationSize*carryPercentage)):
                carriedChromosomes.append(copy.deepcopy(self.population[i]))

            matingPool = self.createMatingPool()
            random.shuffle(matingPool)
            choosedData = random.choices(matingPool, k = populationSize - int(populationSize*carryPercentage))
            crossoverPool = self.createCrossoverPool(choosedData)
            self.population.clear()
            for i in range(populationSize - int(populationSize*carryPercentage)):
                self.population.append(self.mutate(crossoverPool[i]))
            self.population.extend(carriedChromosomes)
            count += 1


def getInput():
    f = open('input.txt', 'r')
    equationLength = f.readline()
    operands = f.readline().split()
    operators = f.readline().split()
    goalNumber = f.readline()

    return equationLength, operands, operators, goalNumber

begin = time.time()
equationLength, operands, operators, goalNumber = getInput()
equationBuilder = EquationBuilder(operators, operands, equationLength, goalNumber)

equationBuilder.findEquation()
print("time :", time.time() - begin)