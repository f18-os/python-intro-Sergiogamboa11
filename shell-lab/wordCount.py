import sys

if len(sys.argv) is not 3:
    print("Use correct format")
    exit()

userInput = sys.argv[1]
userOutput = sys.argv[2]

input = open(userInput, "r")
wordCount = {}
temp = input.read()

temp = temp.lower().replace('\n', ' ').split(" ")
tempLen = len(temp)

for i in range(tempLen):
    temp[i] = temp[i].rstrip(',')
    if temp[i] in wordCount:
        wordCount[temp[i]] += 1
    else:
        wordCount[temp[i]] = 1

output = open(userOutput, "w")
for key, value in sorted(wordCount.items()):
    output.write(str(key) + " " + str(value) + " \n")
output.close()
