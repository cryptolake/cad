#!/usr/bin/env python3
from ad_generator import GenAds
    
print("Product Name:")
product_name = input()

print("Product Description:")
product_description = input()

print("Product Link:")
product_link = input()

print("Extra parameters:")
parameters = input()

ads = GenAds(name=product_name, description=product_description,
             link=product_link, parameters=parameters)

print("Max number of words:")
max_words = int(input())

print("Number of Ad descriptions to generate:")
n = int(input())

ads.generate(n, max_words)

print(ads)
