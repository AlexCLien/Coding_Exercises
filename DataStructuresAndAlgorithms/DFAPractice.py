"""
Substring search using a deterministic finite automaton.

Goal:
Determine whether a string contains the substring "cat"
by manually defining DFA states and transitions.
"""
documents = [
    "The cat sleeps on the chair",
    "The dog runs through the park",
    "The cat runs after the dog",
    "A bird sits on the tree"
]
test = "thecat"
test2 = 'ccat'
test3 = 'cacat'
test4 = 'thecatsran'
test5 = 'dog'
test6 = 'ca'
letters = [char.lower() for sentence in documents for char in sentence if char.isalpha()]
print(letters)
class DFA:
    def __init__(self, states, alphabet, transitions, initial_state, final_state):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_state = final_state

    def accepts(self, input_string):
        current_state = self.initial_state
        for symbol in input_string:
            
            if symbol not in self.alphabet:
                return False
            try:
                print(f"reading {symbol}: {current_state}", end=" -> ")

                current_state = self.transitions[current_state][symbol]

                print(current_state)

            except KeyError:
                return False
    
        if current_state in self.final_state:
            return True

states = {'q0','q1','q2','q3'}
alphabet = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'}
initial_state = 'q0'
accepting_state = {'q3'}
transitions = {
    'q0': {
        symbol: 'q1' if symbol == 'c' else 'q0'
        for symbol in alphabet
            },
    'q1': {
        symbol: 'q2' if symbol == 'a' else 'q1' if symbol == 'c' else 'q0'
        for symbol in alphabet
            },
    'q2': {
        symbol: 'q3' if symbol == 't' else 'q1' if symbol == 'c' else 'q0'
        for symbol in alphabet
            },
    'q3': {
        symbol: 'q3'
        for symbol in alphabet
        }
}
fsa = DFA(states, alphabet, transitions, initial_state, accepting_state)
print(fsa.accepts(test))
print(fsa.accepts(test2))
print(fsa.accepts(test3))
print(fsa.accepts(test4))
print(fsa.accepts(test5))
print(fsa.accepts(test6))