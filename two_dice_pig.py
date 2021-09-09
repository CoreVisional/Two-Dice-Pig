
import names

from random import sample


def ask_user_yes_no(yes_no_question) -> bool:
    """Simplifies if/else in determining the correct 
    answers from the user input.

    Returns True if the user answer the prompt with
    any of the values in choice_yes.

    Returns False if the user enters any of the values in choice_no.

    """
    CHOICE_YES = ("yes", 'y')
    CHOICE_NO = ("no", 'n')

    while True:
        user_choice = input(yes_no_question).lower()

        if user_choice in CHOICE_YES:
            return True
        elif user_choice in CHOICE_NO:
            return False
        else:
            print("\nInvalid Input. Try again.")


def greet_user() -> None:
    """Displays a greeting for the game Two-Dice Pig."""
    print(f"\n\nWelcome to Two-Dice Pig Match!")


def print_name(p1, p2) -> None:
    """Displays the name of the player and opponent."""
    print(f"\nYour Name: {p1}\n{'-' * 23}")
    print(f"Opponent's Name: {p2}\n")


def get_name() -> str:
    while True:
        player_name = input("\n\nEnter a name: ")

        if not player_name:
            print("\nPlayer Name Required!")
        else:
            break

    if ask_user_yes_no("\nWould you like to give the AI a name? (Y/N): "):
        while True:
            ai_name = input("\nEnter AI's name: ")
            if not ai_name:
                print("\nAI Name Required!")
            else:
                break
    else:
        print("\n\nA random name has been generated for the AI.")
        rand_name = "AI-" + names.get_first_name()
        three_digits = "".join(map(str, sample(range(10, 1000), 2)))
        ai_name = rand_name + three_digits[:3]

    greet_user()
    print_name(player_name, ai_name)

    return player_name, ai_name


class TwoDicePig:
    def __init__(self, p1_human=True, p2_human=False) -> None:
        self.player_1_name, self.player_2_name = get_name()
        self.dice = Dice()
        self.player_1 = Player(f"{self.player_1_name}", p1_human)
        self.player_2 = Player(f"{self.player_2_name}", p2_human)

    def play(self):
        while (self.player_1.total_score < 100 and self.player_2.total_score < 100):
            self.player_1.turns()
            if self.player_2.total_score < 100:
                self.player_2.turns()
        self.print_winner()

    def print_winner(self):
        if (self.player_1.total_score > self.player_2.total_score):
            print(f"\n{self.player_1_name} wins!")
        else:
            print(f"\n{self.player_2_name} wins!")


class Dice:
    def __init__(self) -> None:
        self.sides = 6

    def roll(self):
        self.faces = sample(range(1, self.sides), 2)


class Player:
    def __init__(self, title, human_player=False) -> None:
        self.name = title
        self.is_human = human_player
        self.total_score = 0
        self.dice = Dice()

    def get_dice_min_max(self):
        self.dice.roll()
        self.die_1 = min(self.dice.faces)
        self.die_2 = max(self.dice.faces)
        return self.die_1, self.die_2

    def turns(self):
        if self.is_human:
            self.human_turn()
        else:
            self.computer_turn()

    def human_turn(self):
        player_score = 0

        while True:
            roll_1, roll_2 = self.get_dice_min_max()

            if roll_1 == 1 or roll_2 == 1:
                print(f"\n\n{self.name} rolled a 1.")
                break
            elif roll_1 == 1 and roll_2 == 1:
                print(f"\n{self.name} rolled two 1s and lost all the scores.")
                player_score = 0
                break
            else:
                print(f"\n\n{self.name} rolled a {roll_1} and {roll_2}.")
                player_score += sum([roll_1, roll_2])
                if player_score == 1 or player_score == 0:
                    print(
                        f"\n{self.name} scored \033[1m{player_score} point\033[0m in this round.\n\n{'-' * 23}")
                else:
                    print(
                        f"\n{self.name} scored \033[1m{player_score} points\033[0m in this round.\n\n{'-' * 23}")

            if not ask_user_yes_no("\nRoll again? (Y/N): "):
                break

        self.total_score += player_score
        print(f"\n{self.name}'s turn ends.")
        print(f"\n({self.name}) Total Score: {self.total_score}\n\n{'-' * 23}")

    def computer_turn(self):
        computer_score = 0

        while True:
            roll_1, roll_2 = self.get_dice_min_max()

            if roll_1 == 1 or roll_2 == 1:
                print(f"\n{self.name} rolled a 1.")
                break
            elif roll_1 == 1 and roll_2 == 1:
                print(f"\n{self.name} rolled two 1s and lost all the scores.")
                computer_score = 0
                break
            else:
                print(f"\n{self.name} rolled a {roll_1} and {roll_2}.")
                computer_score += sum([roll_1, roll_2])
                if computer_score < 20:
                    print(f"\n{self.name} will roll the dice again.\n\n")
                else:
                    break

        self.total_score += computer_score
        print(f"\n{self.name}'s turn ends.")
        print(f"\n{self.name} scored {computer_score} in this round.")
        print(f"\n({self.name}) Total Score: {self.total_score}\n\n{'-' * 23}")


def should_play_again():
    """Asks the user if they want to play again.

    Restarts program if True, else prints a message
    telling the user that the program has exited.

    """
    if ask_user_yes_no("\n\nWould you like to Two-Dice Pig again? (Y/N): "):
        return main()
    else:
        print("\n\n-----Program Exited-----\n\n")


def main():
    play_game = TwoDicePig()
    play_game.play()
    should_play_again()


if __name__ == "__main__":
    main()
