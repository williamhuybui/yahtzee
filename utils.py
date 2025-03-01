def get_score(dice_values, content):
    if content == 'Ones':
        return dice_values.count(1)
    elif content == 'Twos':
        return dice_values.count(2) * 2
    elif content == 'Threes':
        return dice_values.count(3) * 3
    elif content == 'Fours':
        return dice_values.count(4) * 4
    elif content == 'Fives':
        return dice_values.count(5) * 5
    elif content == 'Sixes':
        return dice_values.count(6) * 6
    elif content == 'Three of a kind':
        pass
    elif content == 'Four of a kind':
        pass
    elif content == 'Full House':
        pass
    elif content == 'Small Straight':
        pass
    elif content == 'Large Straight':
        pass
    elif content == 'Yahtzee':
        pass
    elif content == 'Chance':
        pass
    else:
        return None