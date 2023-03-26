# Hungry Hungry Panda

## Category

Programming

## Estimated difficulty

Easy

## Description

A short programming challenge based on battleships. You get 50 tries to find all 16 pandas in a grid of 10x10.

## Scenario

Can you please feed the pandas? They're hungry!

Execute the following command to connect to the service: `nc <ip> 9876`

## Write-up

You have to do a bit of guessing and a bit of extrapolating to find the correct locations of all the pandas.

From the intro, you know that there are 4 groups, one of 6, 5, 4 and 1. The single panda (Bob) is the most difficult to find, but you should still find him in 50% of your runs.

## PoC script

Run PoC script with `python3 run.py <ip> <port>`. pwntools required.

## Flag

`csc{1_l1k3_b1g_p4nd4s_4nd_1_c4nn0t_l13!}`

## Creator

Jeroen Beckers

## Creator bio

The ususal
