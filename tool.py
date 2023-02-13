# write your code here
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


class WrongKeyException(Exception):
    def __init__(self, key):
        self.message = f"{key} is not an option"
        super().__init__(self.message)


class EmptyInputException(Exception):
    pass


Base = declarative_base()


class Flashcard(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    question = Column(String(75))
    answer = Column(String(75))
    box = Column(Integer, default=1)


class FlashcardApplication:
    def __init__(self):
        engine = create_engine('sqlite:///flashcard.db?check_same_thread=False',  # check_same_thread=False
                               echo=False,  # so that Hyperskill can test the project properly
                               poolclass=NullPool)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def add_flashcard(self, a_question, an_answer):
        new_flashcard = Flashcard(question=a_question, answer=an_answer)
        self.session.add(new_flashcard)
        self.session.commit()

    def get_all_flashcards(self):
        result_list = self.session.query(Flashcard).all()
        return result_list

    def delete_flashcard(self, a_flashcard):
        self.session.delete(a_flashcard)
        self.session.commit()

    def edit_flashcard(self, a_flashcard):
        print('current question:', a_flashcard.question)
        a_flashcard.question = self.take_not_empty_input('please write a new question:')
        print('current answer:', a_flashcard.answer)
        a_flashcard.answer = self.take_not_empty_input('please write a new answer:')
        self.session.commit()

    def change_learning_box(self, a_flashcard, is_correct):
        if is_correct == 'y':
            if a_flashcard.box == 3:
                self.delete_flashcard(a_flashcard)
            else:
                a_flashcard.box += 1
        elif is_correct == 'n':
            if a_flashcard.box > 1:
                a_flashcard.box -= 1
        self.session.commit()

    def practice_cards(self):
        all_cards = self.get_all_flashcards()
        n = len(all_cards)
        if n == 0:
            print('There is no flashcard to practice!')
        else:
            for i in range(n):
                print(f"Question: {all_cards[i].question}")
                practice_menu_button = self.take_not_empty_input('press "y" to see the answer:\n'
                                                                 'press "n" to skip:\n'
                                                                 'press "u" to update:',
                                                                 expected_answers=['y', 'n', 'u'])
                if practice_menu_button == 'y':
                    print(f"Answer: {all_cards[i].answer}")
                    learning_menu_button = self.take_not_empty_input('press "y" if your answer is correct:\n'
                                                                     'press "n" if your answer is wrong:',
                                                                     expected_answers=['y', 'n'])
                    self.change_learning_box(all_cards[i], learning_menu_button)
                elif practice_menu_button == 'u':
                    update_menu_button = self.take_not_empty_input('press "d" to delete the flashcard:\n'
                                                                   'press "e" to edit the flashcard:',
                                                                   expected_answers=['d', 'e'])
                    if update_menu_button == 'd':
                        self.delete_flashcard(all_cards[i])
                    elif update_menu_button == 'e':
                        self.edit_flashcard(all_cards[i])

    def print_menu(self, a_status):
        if a_status:
            return "1. Add a new flashcard\n" \
                   "2. Exit"
        else:
            return "1. Add flashcards\n" \
                   "2. Practice flashcards\n" \
                   "3. Exit"

    def take_not_empty_input(self, a_question, expected_answers=None):
        while True:
            print(a_question)
            user_input = input()
            try:
                if expected_answers and user_input not in expected_answers:
                    raise WrongKeyException(user_input)
                elif len(user_input.strip()) == 0:
                    raise EmptyInputException
            except WrongKeyException as err:
                print(err)
            except EmptyInputException:
                pass
            else:
                return user_input

    def user_choice(self, a_status):
        if a_status:
            message = self.take_not_empty_input(self.print_menu(a_status),
                                                expected_answers=['1', '2'])

            if message == '1':  # Add a new flashcard
                question = self.take_not_empty_input("Question:")
                answer = self.take_not_empty_input("Answer:")
                self.add_flashcard(question, answer)
                return True
            elif message == '2':  # Exit from submenu
                return False
        else:
            message = self.take_not_empty_input(self.print_menu(a_status),
                                                expected_answers=['1', '2', '3'])

            if message == '1':  # Add flashcards
                return True
            elif message == '2':  # Practice flashcards
                self.practice_cards()
                return False
            elif message == '3':  # Exit
                self.session.close()
                print("Bye!")
                return None


if __name__ == '__main__':
    status = None
    app = FlashcardApplication()
    while True:
        status = app.user_choice(status)
        if status is None:
            break
