
import names

from random import sample


def ask_user_yes_no(yes_no_question) -> bool:
    """Simplifies if/else to determine the correct answers from the user input.

    Args:
        yes_no_question: A string that asks user a yes or no question.

    Returns:
        True if the user's answer is in CHOICE_YES,
        and False otherwise.

        Prints a message to the user if their input are not similar
        to the ones in CHOICE_YES and CHOICE_NO.

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


def print_names(p1, p2) -> None:
    """Displays the name of the player and opponent."""
    print(f"\n\nYour Name: {p1}\n{'-' * 23}")
    print(f"Opponent's Name: {p2}\n")


def get_player_names() -> str:
    """Asks the user to enter their name and generates a random
    name if the user do not wish to give player 2 a name.

    Returns:
        A string of both player 1 and player 2's names.

    This is repeated until the user has provided a 
    name and an AI name to the program.

    """
    while True:
        player_name = input("\n\nEnter a name: ")

        if not player_name:
            print("\nPlayer Name Required!")
        break

    if ask_user_yes_no("\nWould you like to give the AI a name? (Y/N): "):
        while True:
            ai_name = input("\nEnter AI's name: ")
            if not ai_name:
                print("\nAI Name Required!")
            break
    else:
        print("\n\nA random name has been generated for the AI.")
        rand_name = f"AI-{names.get_first_name()}"
        three_digits = "".join(map(str, sample(range(10, 1000), 2)))
        ai_name = rand_name + three_digits[:3]

    greet_user()
    print_names(player_name, ai_name)

    return player_name, ai_name


class TwoDicePig:
    """Begins the game and prints out the winner.

    Args:
        p1_human: Indicates whether it is a human player.
                  Defaults to True.

        p2_human: Indicates whether it is a non-human player.
                  Defaults to False.

    Attributes:
        player_1_name, player_2_name (str): The names of both players.
        dice (Dice): An instance of Dice class.
        player_1, player_2 (Player): Instances of the Player class.

    """

    def __init__(self, p1_human: bool = True, p2_human: bool = False) -> None:
        self.player_1_name, self.player_2_name = get_player_names()
        self.dice = Dice()
        self.player_1 = Player(f"{self.player_1_name}", p1_human)
        self.player_2 = Player(f"{self.player_2_name}", p2_human)

    def play(self) -> None:
        """Starts and continue the game if a player has not scored over 100 yet.

        Calls print_winner method when a player scored over 100.

        """
        while (self.player_1.total_score < 100 and self.player_2.total_score < 100):
            self.player_1.turns()
            if self.player_2.total_score < 100:
                self.player_2.turns()
        self.print_winner()

    def print_winner(self) -> None:
        """Prints out the winner."""
        if (self.player_1.total_score > self.player_2.total_score):
            print(f"\n{self.player_1_name} wins!")
        else:
            print(f"\n{self.player_2_name} wins!")


class Dice:
    """Sets the sides count of a die to 6.

    Attribute:
        sides (int): The sides count of a die.

    """

    def __init__(self) -> None:
        self.sides = 6

    def roll(self):
        """Rolls a list of two randomly selected numbers that starts
        from 1 to 6. Each number represents the value of the die.
        """
        self.faces = sample(range(1, self.sides), 2)


class Player():
    """Sets up the turns for player 1 and player 2,
    and get the total score once a round is over.

    Args:
        players_name: The names of both players.

        human_player = Indicates whether or not it is the actual player
                       or computer's turns. Defaults to False.

    Attributes:
        name (str): The names of player 1 and player 2.

        is_human (bool): True if it is the actual player's turn, False otherwise.
                         Defaults to False.

        total_round (int): The total round taken to win the game. Increments by 1
                           after the end of each player's turn.

        total_score (int): The total score of the players after the end of a round.

        dice (Dice): An instance of Dice class.

    """

    def __init__(self, players_name: str, human_player: bool = False) -> None:
        self.name = players_name
        self.is_human = human_player
        self.total_round = 0
        self.total_score = 0
        self.dice = Dice()

    def get_dice_min_max(self) -> int:
        """Finds the minimum and maximum numbers of the dice.

        Calls an instance method, roll(), to get the minimum 
        and maximum values of the dice.

        Returns:
            die_1 (int): An integer of the lowest value in the list.
            die_2 (int): An integer of the highest value in the list.

        """
        self.dice.roll()
        self.die_1 = min(self.dice.faces)
        self.die_2 = max(self.dice.faces)
        return self.die_1, self.die_2

    def turns(self) -> None:
        """Switches the turn to the actual player if is_human is 
        True, sets the turns to the computer otherwise.

        """
        if self.is_human:
            self.human_turn()
        else:
            self.computer_turn()

    def human_turn(self) -> None:
        """Totals up player 1's score of each round and prints out
        the total score after the end of every round.

        """
        player_score = 0
        self.total_round += 1

        # Continues the game if the player chooses to roll the
        # dice again, ends the round otherwise.
        while True:
            print("{:^20}\033[1mROUND: {}\033[0m\n".format(
                '\n' * 3, self.total_round))

            print(f"({self.name})".center(25))

            roll_1, roll_2 = self.get_dice_min_max()

            if roll_1 == 1 or roll_2 == 1:
                print(f"\n\n{self.name} rolled a 1.")
                break
            elif roll_1 == 1 and roll_2 == 1:
                print(f"\n\n{self.name} rolled two 1s and lost all the scores.")
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

            if ask_user_yes_no("\nRoll again? (Y/N): "):
                self.total_round += 1
            else:
                break

        self.total_score += player_score
        print(f"\n\n{self.name}'s turn ends.")
        print(
            f"\n\033[1m({self.name}) Total Score: {self.total_score}\033[0m\n\n{'=' * 30}")

    def computer_turn(self):
        """Totals up the computer's score and prints out the 
        total score after the end of each round.

        """
        computer_score = 0
        self.total_round += 1

        print("{:^20}\033[1mROUND: {}\033[0m\n".format(
            '\n' * 3, self.total_round))

        print(f"({self.name})".center(25))

        # Let the AI rolls the dice again if its score is lesser
        # than 20, ends its turns otherwise.
        while True:
            roll_1, roll_2 = self.get_dice_min_max()

            if roll_1 == 1 or roll_2 == 1:
                print(f"\n\n{self.name} rolled a 1.")
                break
            elif roll_1 == 1 and roll_2 == 1:
                print(f"\n\n{self.name} rolled two 1s and lost all the scores.")
                computer_score = 0
                break
            else:
                print(f"\n\n{self.name} rolled a {roll_1} and {roll_2}.")
                computer_score += sum([roll_1, roll_2])
                if computer_score < 20:
                    print(f"\n{self.name} will roll the dice again.\n")
                else:
                    break

        self.total_score += computer_score
        print(f"\n{self.name}'s turn ends.")
        print(f"\n{self.name} scored {computer_score} in this round.")
        print(
            f"\n\033[1m({self.name}) Total Score: {self.total_score}\033[0m\n\n{'=' * 30}")


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
