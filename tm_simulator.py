import sys


# function to parse the definition of the TM
def parse_tm_definition(filename):
    # open the file in read mode
    with open(filename, 'r') as file:
        # strip each line of white space
        lines = [line.strip() for line in file.readlines()]
    
    # line 1 is list of states, 
    states = lines[1].split(',')

    # line 2 is a list of input alphabet
    input_alphabet = set(lines[2].split(','))

    # line 3 is the tape alphabet
    tape_alphabet = set(lines[3].split(','))

    # line 4 is the initial state
    initial_state = lines[4]

    # line 5 is the blank symbol
    blank_symbol = lines[5]

    # line 6 is the list of final states
    final_states = set(lines[6].split(','))
    
    # line 7 and beyond are the transitions

    # using a dictionary database
    transitions = {}

    for line in lines[7:]:
        if line.startswith('('):
            # strip line of () and ,
            parts = line.strip('()').split(',')

            # strip of abnormal spaces
            parts = [part.strip() for part in parts]

            # key: current state, input symbol
            # value: resulting state, symbol to write, direction to move
            key = (parts[0], parts[1])
            value = (parts[2], parts[3], parts[4])

            # add it to the database
            transitions[key] = value

    # return everything
    return states, input_alphabet, tape_alphabet, initial_state, blank_symbol, final_states, transitions



# function to run the recognizer
def run_recognizer(tm_definition, tm_input):

    # unpack tm_definition into individual variables
    # states, input alphabet, tape alphabet not necessary
    _, _, _, initial_state, blank_symbol, final_states, transitions = tm_definition

    # result string
    result = []
    
    # for each input
    for input_string in tm_input:

        # create a tape, which is a list version of the input string
        tape = list(input_string)

        # begin at the head of the tape
        head_position = 0

        # start at the initial state
        current_state = initial_state

        while True:
            # ensure symbol within bounds of the tape
            # if it's out of bounds, then it's a _
            if head_position < 0 or head_position >= len(tape):
                symbol = blank_symbol
            else:
                symbol = tape[head_position]
            
            # create the key (for transition)
            key = (current_state, symbol)

            # no valid transition (DIE!)
            if key not in transitions:
                break

            # look up transition rule with the key
            next_state, write_symbol, direction = transitions[key]

            # write the write_symbol onto the tape
            if 0 <= head_position < len(tape):
                tape[head_position] = write_symbol
            elif head_position >= len(tape):
                tape.append(write_symbol)
            elif head_position < 0:
                # insert at the beginning
                tape.insert(0, write_symbol)
                # still have to move to the front
                head_position = 0

            # update the current state and move the tape head
            current_state = next_state
            if direction == 'R':
                head_position += 1
            elif direction == 'L':
                head_position -= 1

        # accept if landed in accepting state
        result.append("accept" if current_state in final_states else "reject")

    return result



def run_transducer(tm_definition, tm_input):

    # unpack tm_definition into individual variables
    # states, input alphabet, tape alphabet not necessary
    _, _, _, initial_state, blank_symbol, final_states, transitions = tm_definition

    # resulting list to return
    result = []

    # for each input
    for input_string in tm_input:

        # create a tape of the input itself
        # this is already a list
        tape = list(input_string)

        # begin at the 0 position
        head_position = 0

        # current state is the defined initial state
        current_state = initial_state

        while True:

            # ensure symbol within bounds of the tape
            # if it's out of bounds, then it's a _
            if head_position < 0 or head_position >= len(tape):
                symbol = blank_symbol
            else:
                symbol = tape[head_position]
            
            # create the key (for the transition)
            key = (current_state, symbol)

            # if transition is not available (DIE!)
            if key not in transitions:
                break

            # apply the transition
            next_state, write_symbol, direction = transitions[key]

            # write the write_symbol onto the tape
            if 0 <= head_position < len(tape):
                tape[head_position] = write_symbol
            elif head_position >= len(tape):
                tape.append(write_symbol)
            elif head_position < 0:
                # insert at the beginning
                tape.insert(0, write_symbol)
                # still have to move to the front
                head_position = 0

            # update the current state
            current_state = next_state

            # update the head position
            if direction == 'R':
                head_position += 1
            elif direction == 'L':
                head_position -= 1

            if current_state in final_states:
                break


        # Ensure head_position is within bounds
        if head_position < len(tape):
            output = ''.join(tape[head_position:])
        else:
            output = ''
            
        result.append(output)

    return result



# main loop
def main():
    # must be of 3 arguments
    # tm_simulator tm_definition tm_input
    if len(sys.argv) != 3:
        print("Usage: tm_simulator tm_definition tm_input")
        return

    tm_definition_file = sys.argv[1]
    tm_input_file = sys.argv[2]

    # parse the definition
    tm_definition = parse_tm_definition(tm_definition_file)

    # open the input file
    with open(tm_input_file, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    
    # line 0 is the type
    tm_type = lines[0].lower()
    # line 1 and beyond are the inputs
    # note: already breaks into a list
    tm_input = lines[1:]

    if tm_type == "recognizer":
        results = run_recognizer(tm_definition, tm_input)
    elif tm_type == "transducer":
        results = run_transducer(tm_definition, tm_input)
    else:
        # type not inputted correctly
        print(f"Unknown TM type: {tm_type}")
        return

    # output the results
    for result in results:
        print(result)
    

if __name__ == "__main__":
    main()
