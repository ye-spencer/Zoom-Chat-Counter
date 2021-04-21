import sys
import datetime
"""
Author: Spencer Ye
Last Modified: April 15, 2021
Version: 1.0
"""

#Takes the list of entries and sees who sent each entry
#Parameters: A list of entries
#Returns: A list of who sent each message
def parseToSender(entries):
	senders = []
	for inputLine in entries:
		indexOne = inputLine.index("From") + 5
		indexTwo = inputLine.index("to") - 1
		senders.append(inputLine[indexOne:indexTwo])
	return senders
#Takes the full name of the entry and changes it to last name then first name
#Parameters: A string of a senders full name
#Returns: A string of hte senders name with last name first
def getSenderFormattedName(previousName):
	try:
		index = previousName.index(" ")
		return previousName[index:] + previousName[:index]
	except ValueError:
		return previousName
	return "ERROR IN SENDER NAME: " + previousName

#Counts how many times a sender appears in the list
#Parameters: A list of who sent each message
#Returns: A dictionary of each sender and how many messages they sent
def consolidateToSenderCount(senders):
	senderDict = {} #String sender, int times
	for sender in senders:
		try:
			senderDict[sender] = senderDict.get(sender) + 1
		except TypeError: #sender is not in dictionary yet
			senderDict[sender] = 1
	return senderDict

# Returns all the entries in the given input file
# Parameters: A File on read
# Returns: A list of strings of all the entries
def getEntries(inputFile):
	entries = []
	for inputLine in inputFile.readlines():
		try:
			inputLine.index("From")
			entries.append(inputLine)
		except ValueError:
			entries[len(entries) - 1] = entries[len(entries) - 1] + inputLine
	return entries

#Gets the messages sent by a particular sender
#Parameters: String name of the sender, A list of who sent each message, A list of all entries
#Returns: A string list of all the messages that the sender sent 
def getMessages(sender, senderList, entries):
	senderEntries = []
	for i in range(len(senderList)):
		if sender == senderList[i]:
			senderEntries.append(entries[i])
	return senderEntries

#Formats the dictionary so that it is alphabetized and margined, then adds the related entries
#Parameters: A dictonary of each sender and how many messages they sent, A list of who sent each message, A list of strings of entries
#Returns: A string that is ready to be outputted
def formatDictionary(senderDict, senderList, entryList):
	toSend = ""
	maxNameLength = 25
	for sender in sorted(senderDict.keys()):
		if (len(sender) > maxNameLength):
			toSend += sender[:maxNameLength] + getSenderFormattedName(str(senderDict[sender])) + "\n"
		else:
			toSend += sender.ljust(maxNameLength) + getSenderFormattedName(str(senderDict[sender])) + "\n"
		for message in getMessages(sender, senderList, entryList):
			toSend += "\t" + message
	return toSend

#Writes the text to a file
#Parameters: The text to be written, a file on write
#Returns: Nothing
def writeToFile(text, outputFile):
	outputFile.write(text)

#Does the whole process that this program is supposed to do
#Parameters: A file on read, A file on write
#Returns: Nothing
def doProcess(inputFile, outputFile):
	entryList = getEntries(inputFile)
	senders = parseToSender(entryList)
	sendersCount = consolidateToSenderCount(senders)
	text = formatDictionary(sendersCount, senders, entryList)
	writeToFile(text, outputFile)

def main():
	begin_time = datetime.datetime.now()
	if (len(sys.argv) != 3):
		print("\nInvalid Input: Type in the command \"python zoomchatcounter.py [input file] [output file]\"\n")
	else:
		try: 
			inFile = open(sys.argv[1], "r", encoding="utf8")
			outFile = open(sys.argv[2], "w", encoding="utf8")
			doProcess(inFile, outFile)
		except Exception:
			print("A problem occured while registering files")

	#print("Runtime is:", end=" ")
	#print(datetime.datetime.now() - begin_time)

if __name__ == "__main__":
	main()