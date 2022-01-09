
"""A simple CLI-based dice roll simulation game."""

from random import sample

import names


def ask_user_yes_no(yes_no_question) -> bool:
    """Simplify if/else to determine the correct answers from the user input.

    Args:
        yes_no_question: A string that asks user a yes or no question.

    Returns:
        True if the user's answer is in choice_yes,
        and False otherwise.

        Prints a message to the user if their input are not similar
        to the ones in choice_yes and choice_no.

    """
    choice_yes = ("yes", 'y')
    choice_no = ("no", 'n')

    while True:
        user_choice = input(yes_no_question).lower()

        if user_choice in choice_yes:
            return True

        if user_choice in choice_no:
            return False

        print("\nInvalid Input. Try again.")


def greet_user() -> None:
    """Display a greeting for the game Two-Dice Pig."""
    print("\n\nWelcome to Two-Dice Pig Match!")


def print_names(p_1, p_2) -> None:
    """Display the name of the player and opponent."""
    print(f"\n\nYour Name: {p_1}\n{'-' * 23}")
    print(f"Opponent's Name: {p_2}\n")


def get_player_names():
    """Ask the user to input their name.

    The program will generate a random name if the
    user do not wish to give player 2 a name.

    Returns:
        A tuple of string containing the names
        of both player 1 and player 2.

    This process is repeated until the user has provided
    a name and an AI name to the program.

    """
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
        rand_name = f"AI-{names.get_first_name()}"
        three_digits = "".join(map(str, sample(range(10, 1000), 2)))
        ai_name = rand_name + three_digits[:3]

    greet_user()
    print_names(player_name, ai_name)

    return player_name, ai_name


class TwoDicePig:
    """Begin the game and prints out the winner.

    Args:
        p1_human: Indicates whether it is a human player.
                  Defaults to True.

        p2_human: Indicates whether it is a non-human player.
                  Defaults to False.

    Attributes:
        player_1_name, player_2_name (str): The names of both players.

        player_1, player_2 (Player): Instances of the Player class.

    """

    def __init__(self, p1_human: bool = True, p2_human: bool = False) -> None:
        self.player_1_name, self.player_2_name = get_player_names()
        self.player_1 = Player(f"{self.player_1_name}", p1_human)
        self.player_2 = Player(f"{self.player_2_name}", p2_human)

    def play(self) -> None:
        """Start and continue the game if a player has not scored over 100 yet.

        Call print_winner method when a player scored over 100.

        """
        while (self.player_1.total_score < 100 and self.player_2.total_score < 100):
            self.player_1.turns()
            if self.player_2.total_score < 100:
                self.player_2.turns()
        self.print_winner()

    def print_winner(self) -> None:
        """Print out the winner."""
        if self.player_1.total_score > self.player_2.total_score:
            print(
                f"\n\033[1m{self.player_1_name.upper() + ' WINS!':^30}\033[0m")
        else:
            print(
                f"\n\033[1m{self.player_2_name.upper() + ' WINS!':^30}\033[0m")

        self.print_result()

    def print_result(self) -> None:
        """Print out the player's name and total points scored by each player."""
        p1_final_points = f"{self.player_1_name}: {self.player_1.total_score}"
        p2_final_points = f"{self.player_2_name}: {self.player_2.total_score}"

        print(f"\n\n {p1_final_points} Points | {p2_final_points} Points")


class Player:
    """Set up the turns and get total score after each round.

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

        die_1 (None): The minimum integer value of the dice.

        die_2 (None): The maximum integer value of the dice.

    """

    def __init__(self, players_name: str, human_player: bool = False) -> None:
        self.name = players_name
        self.is_human = human_player
        self.total_round = 0
        self.total_score = 0
        self.die_1 = None
        self.die_2 = None

    def get_dice_min_max(self) -> tuple[int]:
        """Set the minimum and maximum numbers of the dice.

        Returns:
            A tuple of integers containing the lowest
            and highest face values of the dice.

        """
        die_sides = 6
        dice_face_values = sample(range(1, die_sides), 2)
        self.die_1 = min(dice_face_values)
        self.die_2 = max(dice_face_values)
        return self.die_1, self.die_2

    def turns(self) -> None:
        """Switch player's turn.

        Game turn will change to the actual player if is_human is
        True, sets the turn to the computer otherwise.

        """
        if self.is_human:
            self.human_turn()
        else:
            self.computer_turn()

    def human_turn(self) -> None:
        """Total up the score and print the total score after end of each round."""
        player_score = 0

        self.total_round += 1

        # Continue the game if the player chooses to roll the dice again,
        # ends the round otherwise.
        while True:
            print("{:^20}\033[1mROUND: {}\033[0m\n".format('\n' * 3, self.total_round))

            print(f"({self.name})".center(25))

            roll_1, roll_2 = self.get_dice_min_max()

            if roll_1 == 1 or roll_2 == 1:
                print(f"\n\n{self.name} rolled a 1.")
                break

            if roll_1 == 1 and roll_2 == 1:
                print(f"\n\n{self.name} rolled two 1s and lost all the scores.")
                player_score = 0
                break

            if roll_1 != 1 and roll_2 != 1:
                print(f"\n\n{self.name} rolled a {roll_1} and {roll_2}.")
                player_score += sum([roll_1, roll_2])
                if player_score in (0, 1):
                    print(f"\n{self.name} scored \033[1m{player_score} point\033[0m in this round.\n\n{'-' * 23}")
                else:
                    print(f"\n{self.name} scored \033[1m{player_score} points\033[0m in this round.\n\n{'-' * 23}")

            if ask_user_yes_no("\nRoll again? (Y/N): "):
                self.total_round += 1
            else:
                break

        self.total_score += player_score
        print(f"\n\n{self.name}'s turn ends.")
        print(
            f"\n\033[1m({self.name}) Total Score: {self.total_score}\033[0m\n\n{'=' * 30}\n")

    def computer_turn(self):
        """Total up the score and print out total score after the end of each round."""
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

            if roll_1 == 1 and roll_2 == 1:
                print(f"\n\n{self.name} rolled two 1s and lost all the scores.")
                computer_score = 0
                break

            if roll_1 != 1 and roll_2 != 1:
                print(f"\n\n{self.name} rolled a {roll_1} and {roll_2}.")
                computer_score += sum([roll_1, roll_2])
                if computer_score < 20:
                    print(f"\n{self.name} will roll the dice again.\n")
                else:
                    break

        self.total_score += computer_score
        print(f"\n{self.name}'s turn ends.")
        print(f"\n{self.name} scored {computer_score} in this round.")
        print(f"\n\033[1m({self.name}) Total Score: {self.total_score}\033[0m\n\n{'=' * 30}\n")


def should_play_again() -> bool:
    """Ask the user if they want to play again.

    Returns:
        True if the user wants to play
        again, False otherwise.

    """
    return ask_user_yes_no("\n\nWould you like to play "
                           "Two-Dice Pig again? (Y/N): ")


def main():
    """Start the program.

    Restarts program if should_play_again function returns True, prints a
    message telling the user that the program has exited otherwise.

    """
    while True:
        play_game = TwoDicePig()
        play_game.play()

        if not should_play_again():
            break

    print("\n\n-----Program Exited-----\n\n")


if __name__ == "__main__":
    main()
