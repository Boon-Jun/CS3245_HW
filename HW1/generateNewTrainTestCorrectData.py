import random

originalTrainData = open("input.train.txt", "r")

originalCorrectData = open("input.correct.txt", "r")

beforeFilteredCorrectData = originalCorrectData.readlines()
filteredCorrectData = ''.join([line for line in beforeFilteredCorrectData if (line.split())[0] != 'other'])

trainCompleteData = originalTrainData.read()
allTrainData = trainCompleteData + filteredCorrectData
actualAllData = trainCompleteData + ''.join(beforeFilteredCorrectData)

newTrainData = open("BJInput.train.txt", "a")
newCorrectData = open("BJInput.correct.txt", "a")
newTestData = open("BJInput.test.txt", "a")

newTrainData.seek(0)
newTrainData.truncate()
newTestData.seek(0)
newTestData.truncate()
newCorrectData.seek(0)
newCorrectData.truncate()


correctData = random.sample(actualAllData.splitlines(), 160)
trainData = [item for item in allTrainData.splitlines() if item not in correctData]

for item in trainData:
    newTrainData.write(item + '\n')


for item in correctData:
    newCorrectData.write(item + '\n')
    newTestData.write(' '.join((item.split())[1:]) + '\n')
