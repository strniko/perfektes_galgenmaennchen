from collections import Counter
import re
import sys

while True:
    length = input(" [?] Wie lang ist das gesuchte Wort?\n [+] ")
    try:
        length = int(length)
        break
    except ValueError:
        print("\n [-] Bitte geben sie eine Zahl ein.\n")

possible_words = []

with open("words.lst", 'r') as wordlist_file:
    wordlist = wordlist_file.readlines()
    for word in wordlist:
        if len(word) - 1 == length:
            possible_words.append(word.removesuffix("\n").upper())

current_word = "_" * length
guessed_letters = []
not_containing_letters = []

while True:
    if len(possible_words) == 1:
        print(f"\nDu hast gewonnen! Das Wort lautet {possible_words[0]}.")
        break
    else:
        regex_pattern = re.compile('^' + current_word.replace('_', '.') + '$')
        possible_words = [word for word in possible_words if regex_pattern.match(word)]
        possible_words = [word for word in possible_words if not any(letter in word for letter in not_containing_letters)]
        possible_words_string = "".join(possible_words)
        char_counts = Counter(possible_words_string)

        common_letter = None

        for letter, count in char_counts.most_common():
            if letter not in guessed_letters:
                common_letter = letter
                break

        if common_letter is None:
            print(" [-] word not in list")
            sys.exit(-1)
        else:
            places = input(
                f"\nDas aktuelle Wort lautet\n{current_word}\n\nIch empfehle den Buchstaben {common_letter} zu raten"
                f"\n [?] An welchen Stellen im Wort befindet sich der Buchstabe {common_letter}?\n [+] ")
            if places == '':
                not_containing_letters.append(common_letter)
            else:
                while True:
                    try:
                        places = places.split(", ")
                        places = [int(element) - 1 for element in places]
                        break
                    except ValueError as error:
                        print(f" [-] Fehler: {error}")
                        sys.exit(-1)

        guessed_letters.append(common_letter)

        for place in places:
            current_word = current_word[:place] + common_letter + current_word[place + 1:]

sys.exit(0)
