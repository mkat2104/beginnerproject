import random, sys

HEARTS = chr(9829)           # character 9829 is '♥'
DIAMONDS = chr(9830)        # character 9830 is '♦'
SPADES = chr(9824)          # character 9824 is '♠'
CLUBS = chr(9827)           # character 9827 is '♣'
BACKSIDE = 'backside'


def main():
    money = 5000
    while True:
        # Check if player is run out of money
        if money <= 0:
            print("You're broke!")
            print("Good thing you weren't playing with real money.")
            print("Thanks for playing!")
            sys.exit()

        # Let the player enter the bet for this round
        print("Money: ", money)
        bet = get_bet(money)

        deck = get_deck()
        dealer_hand = [deck.pop(), deck.pop()]
        player_hand = [deck.pop(), deck.pop()]
        print(dealer_hand)
        print(player_hand)

        print('Bet: ', bet)
        while True:
            display_hands(player_hand, dealer_hand, False)
            print()

            if get_hand_value(player_hand) > 21:
                break

            # Get player's move
            move = get_move(player_hand, money - bet)
            if move == 'D':
                addition_bet = get_bet(min(bet, (money - bet)))
                bet += addition_bet
                print("Bet increased to {}." .format(bet))
                print("Bet: ", bet)

            if move in ('H', 'D'):
                new_card = deck.pop()
                rank, suit = new_card
                print(f"You drew a {rank} of {suit}.")
                player_hand.append(new_card)

                if get_hand_value(player_hand) > 21:
                    print("You busted!")
                    money -= bet
                    continue

            if move in ('S', 'D'):
                break

        if get_hand_value(player_hand) <= 21:
            while get_hand_value(dealer_hand) < 17:
                print("Dealer hits...")
                dealer_hand.append(deck.pop())
                display_hands(player_hand, dealer_hand, False)

                if get_hand_value(dealer_hand) > 21:
                    break
                input("Press Enter to continue...")
                print("\n\n")

            display_hands(player_hand, dealer_hand, True)

            player_value = get_hand_value(player_hand)
            dealer_value = get_hand_value(dealer_hand)

            if dealer_value > 21:
                print("Dealer busts! You wins ${}".format(bet))
                money += bet
            elif (player_value > 21) or (player_value <  dealer_value):
                print("You lost!")
                money -= bet
            elif player_value > dealer_value:
                print("You won ${}!".format(bet))
                money += bet
            elif player_value == dealer_value:
                print("It's a tie, the bet is returned to you.")

            input("Press Enter to continue...")
            print("\n\n")


def get_bet(max_bet):
    while True:
        print(f"How much do you bet? (1 - {max_bet}),or QUIT")
        bet = input("> ").upper().strip()
        if bet == "QUIT":
            print("Thanks for playing!")
            sys.exit()
        if not bet.isdigit():
            continue
        bet = int(bet)
        if 1 <= bet <= max_bet:
            return bet


def get_deck():
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck


def display_hands(player_hand, dealer_hand, show_dealer_hand):
    print()
    if show_dealer_hand:
        print("DEALER:", get_hand_value(dealer_hand))
        display_cards(dealer_hand)
    else:
        print("DEALER: ???" )
        display_cards([BACKSIDE] + dealer_hand[1:])

    print("PLAYER:", get_hand_value(player_hand))
    display_cards(player_hand)


def get_hand_value(cards):
    value = 0
    ace_count = 0
    for card in cards:
        rank = card[0]
        if rank == 'A':
            ace_count += 1
        elif rank in ('J', 'Q', 'K'):
            value += 10
        else:
            value += int(rank)

    # Add value for ace
    value += ace_count
    for i in range(ace_count):
        if value + 10 <= 21:
            value += 10
    return value


def display_cards(cards):
    rows = ['', '', '', '']
    for i, card in enumerate(cards):
        rows[0] += ' ___ '
        if card == BACKSIDE:
            rows[1] += '|## |'
            rows[2] += '|###|'
            rows[3] += '|_##|'
        else:
            rank, suit = card
            rows[1] += '|{} |'.format(rank.ljust(2))
            rows[2] += '| {} |'.format(suit)
            rows[3] += '|_{}|'.format(rank.rjust(2, '_'))

    for row in rows:
        print(row)


def get_move(player_hand, money):
    while True:
        moves = ['(H)IT', '(S)tand']
        if len(player_hand) == 2 and money > 0:
            moves.append('(D)ouble down')

        move_prompt = ', '.join(moves) + '> '
        move = input(move_prompt).upper()
        if move in ('H', 'S'):
            return move
        if move == 'D' and '(D)ouble down' in moves:
            return move


if __name__ == '__main__':
    main()