#!/usr/bin/env python3
#coding=utf-8

import random

def create_random_string(s,length):
    s1 = random.choice(s)
    lst = [random.choice(s) for i in range(length)]
    random.shuffle(lst)
    return ''.join(lst)



def create_random_phone():
    prefix_list = ['130','131','132','133','134','135','136','137','138','139','147','150','151','152','153','155','156','157','158','159','186','187','188']
    return random.choice(prefix_list) + create_random_string('0123456789',8)
if __name__ == '__main__':
    s = '123abc'
    length = 8
    print(create_random_string(s,length))
    print(create_random_phone())