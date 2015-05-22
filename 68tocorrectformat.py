# -*- coding: utf-8 -*-
"""
Created on Tue May 19 13:29:23 2015

@author: Thomas
"""

import csv


csv_file_object = csv.reader(open('68colors.csv', 'rb'))

result_array = []
for row in csv_file_object:
    result = "'" + str(row) + "'"
    result_array.append(result)

result_file = open("newest68colors.csv", "wb")
result_file_object = csv.writer(result_file)

for i, row in enumerate(result_file_object):
    result_file_object.writerow(result_array[i])
    
result_file.close()