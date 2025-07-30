def create_big_letter(letter, size=10, uppercase=True):
    """Creates a large letter shape output made of the entered letter.

    Args:
      letter: The letter to use for the shape.
      size: The size of the output (default is 10).
      uppercase: Whether to render the letter in uppercase (default True).

    Returns:
      A string containing the large letter shape, or None if invalid input is provided.
    """

    if size < 1:
        return "Size must be at least 1."

    if not letter.isalpha():
        return "Invalid character entered. Please enter a letter."

    letter = letter.upper() if uppercase else letter.lower()
    letter_shapes = {
        "A": lambda s: [
            [letter] * s if row == 0 or row == s - 1
            else [letter] + [" "] * (s - 2) + [letter] for row in range(s)
        ],
        "B": lambda s: [
            [letter] * s if row == 0 or row == s - 1
            else [letter] + [" "] * (s - 2) + [letter] for row in range(s)
        ],
        # Add more letter shapes here...
        "C": lambda s: [
            [letter] * s if row == 0 or row == s - 1
            else [letter] + [" "] * (s - 2) for row in range(s)
        ],
    }


    if letter not in letter_shapes:
        return f"Letter '{letter}' not yet supported."


    shape = letter_shapes[letter](size)
    return "\n".join(["".join(row) for row in shape])


# Get user input
letter = input("Enter a letter: ")
size = int(input("Enter the size (default 10): ") or 10)
uppercase = input("Uppercase? (y/n, default y): ").lower() != "n"

result = create_big_letter(letter, size, uppercase)
print(result)