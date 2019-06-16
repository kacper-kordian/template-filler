#!/usr/bin/env python
#Developed by Kacper-K (https://github.com/kacper-kordian) & James Bruce 
from jinja2 import Environment, FileSystemLoader, select_autoescape
import glob
import sys

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

inputData = []

def main():
	readInput()
	selectedId = displayMenu()
	answers = askQuestion(selectedId)
	fillTemplate(answers, selectedId)

def readInput():
	for file in glob.glob("input/*.input"):
		data = open(file, "r").read()
		inputData.append(parseInput(data))

def parseInput(data):
	lines = data.split("\n")
	title = lines[0]
	templatePath = lines[1]
	questions = []
	for pair in lines[2:]:
		if pair == "":
			continue
		try:
			question, placeholder = pair.split(":")
		except Exception as e:
			print(f"{title} has invalid data:")
			print(f"\t{pair}")
			sys.exit(1)
		questions.append({"question":question+" ", "placeholder":placeholder})

	return (title, templatePath, questions)

def displayMenu():
	for i, value in enumerate(inputData):
		print(f"\t{i}) {value[0]}")
	return input("Please choose number: ")

def askQuestion(templateId):
	choiceQuestions = inputData[int(templateId)][2]
	answers = {}
	for value in choiceQuestions:
		value["answer"] = input(value["question"])
	return choiceQuestions

def fillTemplate(answers, templateId):
	data = {}
	for question in answers:
		data[question["placeholder"]] = question["answer"]
	template = env.get_template(inputData[int(templateId)][1])
	outputName = input("What would you like to call the output file ? ")
	template.stream(**data).dump("output/"+outputName)

if __name__ == '__main__':
	main()