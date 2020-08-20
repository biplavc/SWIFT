import random
import sys 

def my_num():
    file=open("test.txt","r")
    a=file.read()
    return (float(a)*3)
# print(my_num())
# my_num()
print(my_num(), file = open("result.txt", "w"))