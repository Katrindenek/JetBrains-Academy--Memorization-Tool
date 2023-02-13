# Flashcard Application

The project is a part of [SQL with Python](https://hyperskill.org/tracks/30) track made by JetBrains Academy and Hyperskill.

This is a command-line flashcard application that allows you to create, store, and practice flashcards. The application uses SQLAlchemy for database management and stores the data in a SQLite database.

## Features
- Adding a new flashcard with a question and an answer
- Displaying all flashcards
- Deleting a flashcard
- Editing a flashcard
- Practicing flashcards
- Moving a flashcard to a different box based on whether you answered the question correctly

## Requirements
This program requires `sqlalchemy` library. You can install it by running `pip install sqlalchemy`.

## Usage
1. Run the `tool.py` file to start the program.
2. Choose an option from the menu:
   - Add a flashcard: Enter a question and an answer for the flashcard.
   - Practice flashcards: Practice all flashcards and answer each question. If you answer the question correctly, the flashcard will move to the next box.
   - Exit: Exits the program.

## Error handling
The program includes two custom exceptions `WrongKeyException` and `EmptyInputException` to handle invalid inputs.

## Note
The `echo` attribute in the SQLAlchemy engine is set to False so that the Hyperskill platform can properly test the project.

## Example
1. Start
```commandline
> python tool.py
1. Add flashcards
2. Practice flashcards
3. Exit
```
2. Add a new flashcard
```commandline
> 1
1. Add a new flashcard
2. Exit
> 1
Question:
> What is the capital of France?
Answer:
> Paris
```
3. Practice flashcards
```commandline
> 2
Question: What is the capital of France?
press "y" to see the answer:
press "n" to skip:
press "u" to update:
> y
Answer: Paris
press "y" if your answer is correct:
press "n" if your answer is wrong:
> y
```