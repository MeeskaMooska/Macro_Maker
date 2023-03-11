x = 3
value = 2
event_order = [1,2,3,2,4,2]


# Designed to find the x occurrence of a value in the event order list
def find_x_occurrence(x, value, event_order):
    count = 0
    # Enumerates through event_order
    for index, item in enumerate(event_order):
        # Evaluates value of item
        if item == value:
            count += 1
            if count == x:
                event_order.pop(index)
    return event_order

find_x_occurrence(x)