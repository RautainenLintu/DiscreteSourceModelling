import fractions
import json
import random
import time
import keyboard


# Function asks for file name to find the file
def ask_for_file():
    while True:
        print("Enter filename for the source description:")
        filename = input()
        if len(filename) <= 0:
            print("The file name is empty. Try again")
        try:
            file = open(filename)
            file.close()
        except FileNotFoundError:
            print("The file is not found. Please check the existence and location of the file, then try again")
        else:
            break
    return filename


# Function checks if the source description is correct
def description_correct(description):
    correctness = True
    models = []
    for model in description["models"].keys():
        models.append(model)
    switches = []
    for switch in description["switches"].keys():
        switches.append(switch)
    for switch in description["source"]:
        if switch not in switches:
            correctness = False
    for switch in description["switches"].values():
        for model in switch:
            if model not in models:
                correctness = False
    for model in description["models"].values():
        p = 0
        for element in model.values():
            p += fractions.Fraction(element)
        if p != 1:
            correctness = False
    for switch in description["switches"].values():
        p = 0
        for element in switch.values():
            p += fractions.Fraction(element)
        if p != 1:
            correctness = False
    return correctness


# Function counts the probability of subsequence to appear, based on sequence of size N
def count_probability(subsequence, sequence, N):
    p0 = sequence.count('0') / N
    p1 = 1 - p0
    probability = p0 ** subsequence.count('0') * p1 ** subsequence.count('1')
    return probability


# Functions generates sequence of size N (if N = -1, the process lasts until q is pressed)
def generate_sequence(source_dict, N):
    if N > 0:
        size = N
    else:
        size = 1
    sequence = []
    switch_count = -1
    while size > 0:
        switch_count = (switch_count + 1) % len(source_dict["source"])
        current_switch = source_dict["source"][switch_count]
        models = []
        model_probabilities = []
        for model in source_dict["switches"][current_switch].keys():
            models.append(model)
            model_probabilities.append(fractions.Fraction(source_dict["switches"][current_switch][model]))
        model = random.choices(models, weights=model_probabilities)
        model = model[0]
        outcomes = []
        outcome_probabilities = []
        for outcome in source_dict["models"][model].keys():
            outcomes.append(outcome)
            outcome_probabilities.append(fractions.Fraction(source_dict["models"][model][outcome]))
        outcome = random.choices(outcomes, weights=outcome_probabilities)
        outcome = outcome[0]
        if N > 0:
            sequence.append(outcome)
            print(outcome, end='')
            size -= 1
        else:
            sequence.append(outcome)
            print(outcome, end='')
            time.sleep(0.25)
            if keyboard.is_pressed('q'):
                size -= 1
    return sequence


while True:
    filename = "source_description.json"
    # filename = ask_for_file()
    source_file = open(filename, "r")
    source_dict = json.load(source_file)
    if not description_correct(source_dict):
        print("Incorrect description. The program is restarting")
        break
    print("Choose mode 1 (source implementation) or 2 (probability calculation):")
    mode = input()
    while mode != '1' and mode != '2':
        print("Incorrect mode. Try again:")
        mode = input()
    if mode == '1':
        print("Enter value of sequence length N or enter -1 for None")
        N = int(input())
        sequence = generate_sequence(source_dict, N)
    if mode == '2':
        print("Enter sample size N > 0:")
        N = int(input())
        while N <= 0:
            print("Incorrect sample size. Try again")
            N = int(input())
        print("Enter subsequence a_1, a_2, ... , a_k:")
        subsequence = input()
        print("Generated subsequence of size N:")
        sample_sequence = generate_sequence(source_dict, N)
        probability = count_probability(subsequence, sample_sequence, N)
        print()
        print("Probability is:", probability)
    source_file.close()
    print()
    print("Program finished")
    print("Press Enter to restart")
    input()
