def check(attempt, correct):
    found = {}
    result = ["_" for _ in range(5)]
    for i in range(5):
        if attempt[i] == correct[i]:
            result[i] = "#"
            if found.get(attempt[i], 0) == 0:
                found[attempt[i]] = 0
            found[attempt[i]] += 1
    for i in range(5):
        if result[i] == "#":
            continue
        if found.get(attempt[i], 0) < correct.count(attempt[i]):
            result[i] = "+"
            if found.get(attempt[i], 0) == 0:
                found[attempt[i]] = 0
            found[attempt[i]] += 1
    return "".join(result)

words = set()
with open("/home/mhavos/Desktop/programovanie/wordle/words.txt", "r") as file:
    for line in file:
        words.add(line[:-1])
answers = set()
with open("/home/mhavos/Desktop/programovanie/wordle/answers.txt", "r") as file:
    for line in file:
        answers.add(line[:-1])

difficulty = 2

def compare_keys(a, b):
    if a.count("#") < b.count("#"):
        return a
    elif a.count("#") > b.count("#"):
        return b
    elif a.count("+") < b.count("+"):
        return a
    elif a.count("+") > b.count("+"):
        return b

    return a if (a > b) else b

def solve(possible):
    if len(possible) == 1:
        return [(target, "#####")]

    i = 0
    guesses = []
    choices = words if difficulty == 0 else (answers if difficulty == 1 else possible)
    for choice in choices:
        i += 1
        buckets = {}
        for answer in possible:
            result = check(choice, answer)
            l = buckets.get(result, set())
            l.add(answer)
            buckets[result] = l

        newkey = None
        keys = list(buckets.keys())
        keys.sort()
        for key in keys[::-1]:
            if newkey is None:
                newkey = key

            elif len(buckets[key]) > len(buckets[newkey]):
                newkey = key
            elif len(buckets[key]) == len(buckets[newkey]):
                newkey = compare_keys(key, newkey)

        if target not in buckets[newkey]:
            continue
        if len(buckets[newkey]) < len(possible):
            newpossible = reduce(possible, choice, newkey)

            #print(f"guessing {choice}")
            call = solve(newpossible)
            if call:
                call.append((choice, newkey))
                return call

def reduce(possible, choice, result):
    newpossible = set()
    for answer in possible:
        if check(choice, answer) == result:
            newpossible.add(answer)

    return newpossible

with open("/home/mhavos/Desktop/programovanie/wordle/solved.txt", 'r+') as write:
    write.truncate(0)

import time
total = 0

with open("/home/mhavos/Desktop/programovanie/wordle/answers.txt", "r") as file:
    i = 0
    line = file.readline()
    done = False
    while not done:
        istart = i + 1
        start = time.time_ns()
        with open("/home/mhavos/Desktop/programovanie/wordle/solved.txt", "a+") as write:
            for j in range(100):
                i += 1
                target = line.strip("\n")
                if len(target) != 5:
                    done = True
                    break
                print(f"{target}:", " ".join([x[0] for x in solve(answers)[::-1]]), file=write)
                line = file.readline()
        end = (time.time_ns() - start)/10**9
        total += end
        print("lines {} to {} completed in {:6f}s".format(istart, i, end))
print("finished!\nlines 1 to {} completed in {:6f}s".format(i, total))
