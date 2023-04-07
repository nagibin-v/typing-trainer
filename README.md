# Typing Trainer
Python project to train typing skills
## Setup
To run this project, firstly clone the repository
```commandline
git clone git@github.com:nagibin-v/typing-trainer.git
cd typing-trainer
```
If you are running it for the first time, run init.sh
```commandline
./init.sh
```
To run the app itself
```commandline
./run.sh
```
## Features
In this app you can test your typing skills by completing different levels in which you have to type some text.

The app collects statistics about speed and accuracy of your attempts.

There are currently 25 pre-made educational levels and 10 extra levels. Also, you can create your own levels and upload them. Your level should be formatted as follows:
```text
<Title>
<Goal speed> <Goal accuracy>
<Text>
```
Title should be a one-line string, goal speed should be an integer number from 1 to 250 (it is measured in Words Per Minutes), goal accuracy should be a real number from 0 to 1. Text might contain uppercase and lowercase English letters, digits and special symbols. 

## Developers
Created by Vsevolod Nagibin in spring 2023