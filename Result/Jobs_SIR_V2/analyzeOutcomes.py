import os

dirs = []
for i in range(1,10) :
    dirs.append("Run_V2_" + str(i))
#print(dirs)

#for dir in dirs :
results = []
for dir in dirs :
    temp = []
    files = [file for file in os.listdir(dir) if file[-3:] == "out"]
    #print("look here", files)
    for filename in files :
        f = open(dir + "/" + filename, "r")
        for i in range(10):
            temp.append(f.readline()[0])
        f.close()
    results.append(temp)

#print(len(results))

outcomes = []
for result in results :
    aWins = result.count('A')
    bWins = result.count('B')
    probA = aWins / len(result)
    probB = bWins / len(result)
    outcomes.append(["Prob A Wins " + str(probA), "Prob B Wins " + str(probB)])
print(outcomes)
