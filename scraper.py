from bs4 import BeautifulSoup as bs
import requests
import csv
import main as main




def captureAndNormalizeStat(stats, min, max, location, fullTeamData):
    stat = str(stats[location])
    stat = stat.split('>')
    stat = stat[1].split('<')
    stat = float(stat[0])
    stat = (stat - min) / max
    fullTeamData.append(stat)

def createDataArrayForGame(yearsData, gameFile):
    allGameStats = []
    winsLosses = []
    bracketTest2019 = []
    bracketTestMatchup = []
    count = 0
    with open(gameFile, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            try:
                if int(row['Year']) != 2021:
                    #if row['Team']
                    gameStats = []
                    team1Stats = yearsData[int(row['Year'])][row['Team']]
                    team1Seed = row['Seed']
                    for stat in team1Stats:
                        gameStats.append(float(stat))
                    gameStats.append(int(team1Seed))

                    team2Stats = yearsData[int(row['Year'])][row['Team2']]
                    team2Seed = row['Seed2']
                    for stat in team2Stats:
                        gameStats.append(float(stat))
                    gameStats.append(int(team2Seed))

                    #if higher seeded team won aka if team1 won
                    if (int(row['Score']) - int(row['Score2'])) > 0:
                        winsLosses.append(1)
                    else:
                        winsLosses.append(0)
                    allGameStats.append(gameStats)
                """else:
                    # if row['Team']
                    gameStats = []
                    team1Stats = yearsData[int(row['Year'])][row['Team']]
                    team1Seed = row['Seed']
                    for stat in team1Stats:
                        gameStats.append(float(stat))
                    gameStats.append(int(team1Seed))

                    team2Stats = yearsData[int(row['Year'])][row['Team2']]
                    team2Seed = row['Seed2']
                    for stat in team2Stats:
                        gameStats.append(float(stat))
                    gameStats.append(int(team2Seed))
                    bracketTest2019.append(gameStats)
                    matchup = []
                    matchup.append(row['Team'])
                    matchup.append(row['Team2'])
                    bracketTestMatchup.append(matchup)"""

            except:
                count = count + 1
                print()
                print(count)
                print(row['Team'])
                print(row['Team2'])
                print(row['Year'])
                print()


    with open('bracket2021.csv') as csv_file2:
        #print('in csv')
        csv_reader2 = csv.DictReader(csv_file2)
        for row in csv_reader2:
            print('in csv')
            try:
                gameStats = []
                team1Stats = []
                team2Stats = []

                team1Stats = yearsData[int(row['YEAR'])][row['Team']]
                #team1Stats.append(int(row['Seed']))
                team1Seed = row['Seed']
                count = 0
                for stat in team1Stats:
                    if count < 15:
                        gameStats.append(float(stat))
                    count = count + 1
                gameStats.append(float(team1Seed))

                team2Stats = yearsData[int(row['YEAR'])][row['Team2']]
                #team2Stats.append(int(row['Seed2']))
                team2Seed = row['Seed2']
                count = 0
                for stat in team2Stats:
                    if count < 15: #compensates for when we have some teams that show up twice cuz of the first four
                        gameStats.append(float(stat))
                    count = count + 1
                gameStats.append(float(team2Seed))
                bracketTest2019.append(gameStats)
                #team2Stats.append(int(row['Seed2']))
                #team1Stats.append(int(row['Seed']))
                matchup = []
                matchup.append(row['Team'])
                matchup.append(row['Team2'])
                print(matchup)
                bracketTestMatchup.append(matchup)
                print(len(yearsData[int(row['YEAR'])][row['Team']]))
                if len(yearsData[int(row['YEAR'])][row['Team']]) < 16:
                    yearsData[int(row['YEAR'])][row['Team']].append(int(row['Seed']))
                if len(yearsData[int(row['YEAR'])][row['Team2']]) < 16:
                    yearsData[int(row['YEAR'])][row['Team2']].append(int(row['Seed2']))
            except:
                print(row['Team'])
                print(row['Team2'])

        print(bracketTestMatchup)
    return [allGameStats, winsLosses, bracketTest2019, bracketTestMatchup, yearsData[2021]]



def mainMethod(weightings):
    fields = ['Name', 'Win%', 'SOS', 'Pace', 'offRtg', 'FTr', '3PAr', 'TS%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'eFG%', 'TOV',
              'ORB', 'FT/FGA', 'Year', 'Seed']
    fullTable = []
    yearsData = {}




    URLs = ['https://www.sports-reference.com/cbb/seasons/2018-advanced-school-stats.html',
            'https://www.sports-reference.com/cbb/seasons/2017-advanced-school-stats.html',
            'https://www.sports-reference.com/cbb/seasons/2016-advanced-school-stats.html',
            'https://www.sports-reference.com/cbb/seasons/2015-advanced-school-stats.html',
            'https://www.sports-reference.com/cbb/seasons/2014-advanced-school-stats.html',
            'https://www.sports-reference.com/cbb/seasons/2013-advanced-school-stats.html',
            'https://www.sports-reference.com/cbb/seasons/2012-advanced-school-stats.html',
            'https://www.sports-reference.com/cbb/seasons/2019-advanced-school-stats.html',
            'https://www.sports-reference.com/cbb/seasons/2021-advanced-school-stats.html']
    for URL in URLs:
        year = int(URL[45:49])
        page = requests.get(URL)

        #yearsData = {} #stores each year in a dictionary to make searching easy

        allTeamData = []

        soup = bs(page.content, 'html.parser')

        results = soup.find(id='adv_school_stats')

        #print(results.prettify())
        body = results.find('tbody')
        teamData = {}
        teams = body.findAll('tr')
        count = 0
        for team in teams:
            tourneyTeam = team.find('sup')
            if tourneyTeam is not None:

                fullTeamData = []
                count = count + 1
                #team name
                name = team.find('a')
                name = str(name)
                name = name.split('>')
                name = name[1].split('<')
                name = name[0]
                #print(name)
                #fullTeamData.append(name)

                stats = team.findAll('td')

                #Win Percentage
                winPerc = str(stats[4])
                winPerc = winPerc.split('>')
                winPerc = winPerc[1].split('<')
                winPerc = float(winPerc[0])
                fullTeamData.append(winPerc)

                #sos
                sos = str(stats[6])
                sos = sos.split('>')
                sos = sos[1].split('<')
                sos = float(sos[0])
                sos = (sos + 12)/25
                fullTeamData.append(sos)

                #pace
                pace = str(stats[20])
                pace = pace.split('>')
                pace = pace[1].split('<')
                pace = float(pace[0])
                pace = (pace - 60) / 20
                fullTeamData.append(pace)

                # 21 offRTG 85.5 to 122.2
                captureAndNormalizeStat(stats, 85.5, 122.2, 21, fullTeamData)
                # 22 FTr .218 to .48
                captureAndNormalizeStat(stats, .218, .48, 22, fullTeamData)
                # 23 #3PAr .225 to .576
                captureAndNormalizeStat(stats, .225, .576, 23, fullTeamData)
                # 24 TS% .446 to .62
                captureAndNormalizeStat(stats, .446, .62, 24, fullTeamData)
                # 25 TRB%  43.5 to 57.3
                captureAndNormalizeStat(stats, 43.5, 57.3, 25, fullTeamData)
                # 26 AST%  37.9 to 67.1
                captureAndNormalizeStat(stats, 37.9, 67.1, 26, fullTeamData)
                # 27 STL% 5.7 to 13.3
                captureAndNormalizeStat(stats, 5.7, 13.3, 27, fullTeamData)
                # 28 BLK% 4.3 to 17.7
                captureAndNormalizeStat(stats, 4.3, 17.7, 28, fullTeamData)
                # 29 eFG .414 to .59
                captureAndNormalizeStat(stats, .414, .59, 29, fullTeamData)
                # 30 TOV% 11.9 to 22
                captureAndNormalizeStat(stats, 11.9, 22, 30, fullTeamData)
                # 31 ORB% 15.6 to 38.8
                captureAndNormalizeStat(stats, 15.6, 38.8, 31, fullTeamData)
                # 32 FT/FGA .142 to .313
                captureAndNormalizeStat(stats, .142, .313, 32, fullTeamData)

                for i in range (0, len(fullTeamData) - 1):
                    fullTeamData[i] = fullTeamData[i] * weightings[i] #takes into account weightings by user

                teamData[name] = fullTeamData
                #print(teamData)
                #yearsData[year][name] = teamData[name]
                #allTeamData.append(teamData)

        yearsData[year] = teamData #allTeamData

    print(len(fullTable))

    gameFile = 'Big_Dance_CSV.csv'
    data = createDataArrayForGame(yearsData, gameFile)
    #print(data)
    #print('^^')
    bracket = main.fullBracket([])
    return bracket.createNueralNetwork(data[0], data[1], data[2], data[3], data[4])







