""" this is a rebar lib with pres stored rebar information """
import csv

def get_rebars():
    rebarlib = {}
    fr = open('rebarlib.csv','rb')

    reader = csv.reader(fr,delimiter=',')
    
    headerline = reader.next()
    unitline = reader.next()
    
    for row in reader:
        rebarlib[row[0]] = {}
        
        for i in range(1,len(row)):
            rebarlib[row[0]][headerline[i]] = row[i]
            

    return  rebarlib