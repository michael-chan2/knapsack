from collections import namedtuple
from random import randint

NUM_ITEMS = 10
WEIGHT_BOUNDS = (1, 10)
VALUE_BOUNDS = (1, 10)
KNAPSACK_CAPACITY = 20

def knapsack(items, weights, values, capacity):
    """Solves the knapsack problem for the given items. items, weights, and values must be lists
    where items[0] has weight of weights[0] and value of values[0]. This function assumes all
    weights and values will be positive.

    Parameters
    ----------
    - items : List[Object]
    - weights : List[float]
    - values : List[float]
    - capacity : float

    Returns
    -------
    - Tuple[float, List[Object]]
        - The optimal knapsack value and a list of items that produce the optimal value.
    """
    # Make sure the lists all have equal length
    num_items = len(items)
    if num_items != len(weights) or num_items != len(values) or len(weights) != len(values):
        raise Exception('The lengths of the items, weights, and values lists must be equal')

    # Organize the data
    Item = namedtuple('Item', 'item weight value')
    _items = []
    for i in range(num_items):
        _items.append(Item(item=items[i], weight=weights[i], value=values[i]))

    # Find the lowest weight
    lowest_weight = min(weights)

    # Create a table for our tabular method
    table = {item: {i: None for i in range(lowest_weight, capacity+1)} for item in _items}

    incumbent = []
    for i, item in enumerate(_items):
        if i == 0:
            # First item is a special case since there are no previous items to reference
            for cap in range(lowest_weight, capacity+1):
                table[item][cap] = [] if item.weight > cap else [item]
            continue

        previous_item = _items[i-1]
        for cap in range(lowest_weight, capacity+1):
            # Determine candidate_a (the best combination of items if we include the current item)
            candidate_a = []
            if cap >= item.weight:
                candidate_a.append(item)
                remaining_capacity = cap - item.weight
                if remaining_capacity >= lowest_weight:
                    candidate_a.extend(table[previous_item][remaining_capacity])

            # Determine candidate_b (the best combination of items if we do not include the current item)
            candidate_b = table[previous_item][cap]

            # Save the better of the two candidates
            candidate_a_value = sum(x.value for x in candidate_a)
            candidate_b_value = sum(x.value for x in candidate_b)
            table[item][cap] = candidate_a if candidate_a_value > candidate_b_value else candidate_b
    
             # Update the incumbent
            incumbent = table[item][cap] if sum(x.value for x in table[item][cap]) > sum(x.value for x in incumbent) else incumbent
    
    # Print the final table
    for item in _items:
        print(item.item, end='\t')
        for cap in range(lowest_weight, capacity+1):
            print(sum(x.value for x in table[item][cap]), end='\t')
        print()

    solution_value = sum(x.value for x in incumbent)
    solution_items = [x.item for x in incumbent][::-1] # Reverse the list so it appears in the order it was given
    return solution_value, solution_items

def main():
    # Create random set of items
    items, weights, values = [], [], []
    for i in range(NUM_ITEMS):
        items.append(f'Item {i}')
        weights.append(randint(WEIGHT_BOUNDS[0], WEIGHT_BOUNDS[1]))
        values.append(randint(VALUE_BOUNDS[0], VALUE_BOUNDS[1]))
        print(f'{items[-1]}, weight {weights[-1]}, value {values[-1]}')
    print()

    # Run the algorithm
    solution_value, solution_items = knapsack(items, weights, values, KNAPSACK_CAPACITY)

    # Display results
    print()
    print(', '.join(solution_items))
    print(f'Value = {solution_value}')

if __name__ == '__main__':
    main()
