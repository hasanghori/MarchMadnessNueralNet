from keras.models import Sequential
from keras.layers import Dense
import csv
import pprint



class fullBracket:
    bracket = []
    def __init__(self, bracket):
        bracket = self.bracket

    def createNueralNetwork(self, gameData, winsLosses, bracketTest, bracketTestMachups, stats2021):
        fullBracket.bracket = ['Round 1']
        for i in range (0, len(bracketTestMachups)):
            for team in bracketTestMachups[i]:
                fullBracket.bracket.append(team)
        fullBracket.bracket.append('Round 2')
        X = gameData
        Y = winsLosses
        model = Sequential()
        model.add(Dense(34, input_dim=32, activation='relu'))
        model.add(Dense(40, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))

        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        model.fit(X, Y, epochs=150, batch_size=10)

        _, accuracy = model.evaluate(X, Y)
        print('Accuracy: %.2f' % (accuracy*100))



        predictions = model.predict(bracketTest)
        data = ['', bracketTestMachups]
        for i in range(0, 6):
            data = self.processsPredictions(predictions, data[1], stats2021)
            #print(fullBracket.bracket)
            if i == 4:
                fullBracket.bracket.append('Finally Your Champion vv')

            if i != 5:
                fullBracket.bracket.append('Round ' + str(i + 3))
                predictions = self.predictNextRound(model, data[0])
        return fullBracket.bracket


    def processsPredictions(self, predictions, bracketTestMatchups, team2021Data):
        count = 0
        matchUp = []
        fullMatchUps = []
        newData = []
        while count < len(predictions):
            if predictions[count] > .5:
                fullBracket.bracket.append(bracketTestMatchups[count][0])
                matchUp.append(bracketTestMatchups[count][0])
            else:
                fullBracket.bracket.append(bracketTestMatchups[count][1])
                matchUp.append(bracketTestMatchups[count][1])
            if len(matchUp) > 1:
                idxOfSeed = len(team2021Data[matchUp[0]]) - 1
                #fullMatchUps.append(matchUp)
                if team2021Data[matchUp[0]][idxOfSeed] > team2021Data[matchUp[1]][idxOfSeed]:
                    matchUpData = team2021Data[matchUp[0]] + team2021Data[matchUp[1]]
                    fullMatchUps.append([matchUp[0], matchUp[1]])
                    newData.append(matchUpData)
                else:
                    matchUpData = team2021Data[matchUp[1]] + team2021Data[matchUp[0]]
                    newData.append(matchUpData)
                    fullMatchUps.append([matchUp[1], matchUp[0]])
                matchUp = []
            count = count + 1
        #print(newData)
        return [newData, fullMatchUps]

    def predictNextRound(self, model, matchupData):
        predictions = model.predict(matchupData)
        return predictions
