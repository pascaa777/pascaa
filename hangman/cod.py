with open('data.txt', 'r', encoding='utf-8') as file_data:
    game_data = file_data.read()

with open('dictionar.txt', 'r', encoding='utf-8') as file_dict:
    dictionary_data = file_dict.read()

total_attempts = 0
hidden_puzzle = ""
current_progress = ""
letter_sequence = "ERNLOĂCTSMAUPDGFVZBHIȚȘÂJXÎKYWQ"

lines = game_data.strip().split("\n")
dictionary_words = [entry.upper() for entry in dictionary_data.strip().split("\n")]

for entry in lines:
    alphabet_position = 0
    puzzle_id, hidden_puzzle, complete_word = entry.split(";")
    correct_word = complete_word
    current_progress = hidden_puzzle

    possible_matches = [candidate for candidate in dictionary_words if len(candidate) == len(correct_word)]

    possible_matches = [candidate for candidate in possible_matches if all(
        current_progress[i] == "*" or current_progress[i] == candidate[i] for i in range(len(current_progress))
    )]

    attempts_for_word = 0
    while correct_word != current_progress:
        print(f"Progress: {current_progress}, trying letter: {letter_sequence[alphabet_position]}, attempts: {attempts_for_word}")

        if len(possible_matches) == 1:
            current_progress = possible_matches[0]
            attempts_for_word += 1
            print(f"Word guessed: {current_progress} in {attempts_for_word} attempts!")
            break

        if letter_sequence[alphabet_position] in current_progress:
            print(f"Letter {letter_sequence[alphabet_position]} is already in the word.")
            alphabet_position += 1
            continue

        possible_matches = [candidate for candidate in possible_matches if all(
            current_progress[i] == "*" or current_progress[i] == candidate[i] for i in range(len(current_progress))
        )]

        found_letter = any(letter_sequence[alphabet_position] in candidate for candidate in possible_matches)

        if not found_letter:
            attempts_for_word += 1
            print(f"Letter {letter_sequence[alphabet_position]} is not in the word.")
            alphabet_position += 1
            continue

        for i in range(len(correct_word)):
            if current_progress[i] == "*":
                if correct_word[i] == letter_sequence[alphabet_position]:
                    attempts_for_word += 1
                    current_progress = current_progress[:i] + letter_sequence[alphabet_position] + current_progress[i + 1:]
                    print(f"Added letter {letter_sequence[alphabet_position]}, attempts for this word: {attempts_for_word}")

        alphabet_position += 1

    total_attempts += attempts_for_word
    print("____________________")

print(f"Total attempts: {total_attempts}. Game finished!")
