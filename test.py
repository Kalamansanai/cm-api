def calculate_return(input_cash):
    notes = [5, 10, 20, 50, 100, 200, 500]

    storage = {
        5: 10,
        10: 21,
        20: 15,
        50: 11,
        100: 24,
        200: 13,
        500: 4,
    }

    output_cash = {
        5: 0,
        10: 0,
        20: 0,
        50: 0,
        100: 0,
        200: 0,
        500: 0,
    }

    i = len(notes) - 1
    while input_cash > 0:
        if input_cash >= notes[i]:
            in_stock = storage[notes[i]]
            note_in_cash = input_cash / notes[i]
            if in_stock < note_in_cash:
                input_cash = input_cash - in_stock * notes[i]
                storage[notes[i]] = 0
                output_cash[notes[i]] = output_cash[notes[i]] + in_stock
            else:
                input_cash = input_cash - (note_in_cash * notes[i])
                storage[notes[i]] = storage[notes[i]] - note_in_cash
                output_cash[notes[i]] = note_in_cash

        if i == 0 and input_cash > 0:
            return "error"
        i = i - 1

    return output_cash


print(calculate_return(5000))
