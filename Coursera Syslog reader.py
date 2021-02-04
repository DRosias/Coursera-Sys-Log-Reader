#!/usr/bin/env python3

import re
import csv

ErrorCount = {} #key is error message
UserUsageInfo = {} #key is username, index 0 is info count per user, index 1 is error count per user
#matches are (date)(quoted text)(message)(username)
ErrorMatchPattern = "(.*)(ubuntu\.local ticky: ERROR )(.*)( \()(.*)(\))"
InfoMatchPattern = "(.*)(ubuntu\.local ticky: INFO )(.*\()(.*)(\))"

with open("syslog.log") as file:
    for line in file:
        ErrorMatch = re.search(ErrorMatchPattern, line.strip()) #match object for errors
        InfoMatch = re.search(InfoMatchPattern, line.strip()) #match object for info
        if ErrorMatch:
            if ErrorMatch.group(3) in ErrorCount: #if key already exists in dictionary, add 1 count
                ErrorCount[ErrorMatch.group(3)] += 1
            else: #create key
                ErrorCount[ErrorMatch.group(3)] = 1
            if ErrorMatch.group(5) in UserUsageInfo: #if key already exists in dictionary, add 1 count
                UserUsageInfo[ErrorMatch.group(5)][1] += 1 #increment Error count (index 1)
            else:
                UserUsageInfo[ErrorMatch.group(5)] = [0, 1] #initialize list
        elif InfoMatch:
            if InfoMatch.group(4) in UserUsageInfo: #if key already exists in dictionary, add 1 count
                UserUsageInfo[InfoMatch.group(4)][0] += 1  #increment Info count (index 0)
            else:
                UserUsageInfo[InfoMatch.group(4)] = [1, 0]  #initialize list

with open('user_statistics.csv', 'w', newline='') as f:
    items = UserUsageInfo.items()
    sorted_items = sorted(items)
    writer = csv.DictWriter(f, fieldnames=['Username', 'INFO', 'ERROR'])
    writer.writeheader()
    for item in sorted_items:
        tempdict = {'Username': item[0], 'INFO': item[1][0], 'ERROR': item[1][1]}
        writer.writerow(tempdict)

with open('error_message.csv', 'w', newline='') as f:
    items = ErrorCount.items()
    reversedItems = []
    for item in items:
        reversedItem = (item[1], item[0])
        reversedItems.append(reversedItem)
    sorted_items = sorted(reversedItems, reverse=True)
    writer = csv.DictWriter(f, fieldnames=['Error', 'Count'])
    writer.writeheader()
    for item in sorted_items:
        tempdict = {'Error': item[1], 'Count': item[0]}
        writer.writerow(tempdict)
