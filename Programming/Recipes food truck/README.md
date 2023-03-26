# Recipes food truck

## Category
Programming

## Estimated difficulty
Medium

## Description
Web platform with different receipes with ingredients that change very x seconds, you have to lookup for weird ingredients in the receipes and use them to query a new receipe which will give you the flag.

## Scenario
A friend of mine talked to me about his new revolutionary application which takes ingredients as input and give you recipes as output.
He also told me that he hid an easter egg for the skilled hacker I am.
Finding the easter egg would allow me to join his el33t hacker team!

## Write-up
We looking at the ingredients in the recipes we can find non-food related words.
The game is basically find the odds out :)

Multiple ways exists to find the odds but let's use a simple method.
The method used in this case is basically:
1. Getting x amount of responses comparing each responses with each others
2. Finding differents words
3. Checking how many times those different words appears in the requests
4. Based on that give a weight and store them in a list

The idea is that the odd words will appear less then the legit ones, so finding the less present words is a way to get the odd words.

Once you've gather enough responses and generated a list with the odd words, you only have to check if those odd words exist in the page.
If they exist then you send them and get the flag! :)

## PoC script
Check the `solve.py` in the resources folder

## Flag
CSC{flAv0ur_1s_tUn3d}

## Creator
Julian Dotreppe

## Creator bio
l33t hacker