# Open the file 'data.txt' in read mode with UTF-8 encoding
with open('data.txt', 'r', encoding='utf-8') as file_data:
    game_data = file_data.read()  # Read all the content of the file into 'game_data'

# Open the file 'dictionar.txt' in read mode with UTF-8 encoding
with open('dictionar.txt', 'r', encoding='utf-8') as file_dict:
    dictionary_data = file_dict.read()  # Read all the content of the file into 'dictionary_data'

total_attempts = 0  # Initialize a counter for total attempts across all words
hidden_puzzle = ""  # Placeholder for the current puzzle word being guessed
current_progress = ""  # Placeholder for the current progress of the guessed word
letter_sequence = "ERNLOĂCTSMAUPDGFVZBHIȚȘÂJXÎKYWQ"  # Sequence of letters to guess

# Split the game data into lines and strip whitespace
lines = game_data.strip().split("\n")
# Convert all dictionary words to uppercase for uniformity
dictionary_words = [entry.upper() for entry in dictionary_data.strip().split("\n")]

# Loop through each entry in the game data
for entry in lines:
    alphabet_position = 0  # Initialize the current position in the letter sequence
    puzzle_id, hidden_puzzle, complete_word = entry.split(";")  # Unpack the puzzle data
    correct_word = complete_word  # The full word to guess
    current_progress = hidden_puzzle  # The masked version of the word (e.g., "* * * *")

    # Select words from the dictionary that match the length of the correct word
    possible_matches = [candidate for candidate in dictionary_words if len(candidate) == len(correct_word)]

    # Filter possible matches by checking revealed letters
    possible_matches = [candidate for candidate in possible_matches if all(
        current_progress[i] == "*" or current_progress[i] == candidate[i] for i in range(len(current_progress))
    )]

    attempts_for_word = 0  # Initialize the attempts counter for the current word
    # While the current progress doesn't match the correct word
    while correct_word != current_progress:
        # Print the current progress, the letter being tried, and the number of attempts so far
        print(f"Progress: {current_progress}, trying letter: {letter_sequence[alphabet_position]}, attempts: {attempts_for_word}")

        # If only one possible match remains, it must be the correct word
        if len(possible_matches) == 1:
            current_progress = possible_matches[0]  # Guess the word
            attempts_for_word += 1  # Increment attempts
            print(f"Word guessed: {current_progress} in {attempts_for_word} attempts!")  # Confirm the guess
            break  # Exit the guessing loop

        # If the letter has already been guessed, skip to the next letter
        if letter_sequence[alphabet_position] in current_progress:
            print(f"Letter {letter_sequence[alphabet_position]} is already in the word.")
            alphabet_position += 1  # Move to the next letter
            continue  # Restart the loop

        # Update possible matches based on the current guess
        possible_matches = [candidate for candidate in possible_matches if all(
            current_progress[i] == "*" or current_progress[i] == candidate[i] for i in range(len(current_progress))
        )]

        # Check if the current letter is present in any of the possible matches
        found_letter = any(letter_sequence[alphabet_position] in candidate for candidate in possible_matches)

        # If the letter is not found in any possible matches
        if not found_letter:
            attempts_for_word += 1  # Increment the attempts count
            print(f"Letter {letter_sequence[alphabet_position]} is not in the word.")  # Indicate that the letter is incorrect
            alphabet_position += 1  # Move to the next letter
            continue  # Restart the loop

        # Check each character in the correct word
        for i in range(len(correct_word)):
            if current_progress[i] == "*":  # Only check masked characters
                if correct_word[i] == letter_sequence[alphabet_position]:  # If the letter matches
                    attempts_for_word += 1  # Increment attempts
                    current_progress = current_progress[:i] + letter_sequence[alphabet_position] + current_progress[i + 1:]  # Update the current progress
                    print(f"Added letter {letter_sequence[alphabet_position]}, attempts for this word: {attempts_for_word}")  # Confirm the addition

        # Move to the next letter in the sequence
        alphabet_position += 1

    # Add the local attempts for the current word to the total attempts
    total_attempts += attempts_for_word
    print("____________________")  # Separator for clarity in output

# After all words have been processed, print the total number of attempts
print(f"Total attempts: {total_attempts}. Game finished!")  now delete all the explanations