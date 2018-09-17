import sys

if len(sys.argv) is not 3:
    print("Use correct format")
    exit()

userInput = sys.argv[1]
userOutput = sys.argv[2]

input = open(userInput, "r")
output = open(userOutput, "w+")
copy = False

for line in input.readlines():
        output.write(line)

input.close()
output.close()