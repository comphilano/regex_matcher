class State:
    def __init__(self, is_accepted):
        self.is_accepted = is_accepted
        self.transitions = {}
        self.epsilon_transitions = []

    def AddEpsilonTransition(self, to):
        self.epsilon_transitions.append(to)

    def AddTransition(self, to, symbol):
        self.transitions[symbol] = to

    def NextStates(self, symbol):
        results = []
        if symbol == '':
            for next in self.epsilon_transitions:
                results.append(next)
                results.extend(next.NextStates(''))
        else:
            if symbol in self.transitions:
                to = self.transitions[symbol]
                results.append(to)
                results.extend(to.NextStates(''))
        return results


class NFA:
    def __init__(self, symbol):
        self.start = State(False)
        self.end = State(True)
        self.current_states = []
        self.next_states = []
        if symbol == '':
            self.start.AddEpsilonTransition(self.end)
        else:
            self.start.AddTransition(self.end, symbol)

    def Concat(self, other):
        self.end.AddEpsilonTransition(other.start)
        self.end.is_accepted = False
        other.is_accepted = True
        self.end = other.end

    def Union(self, other):
        start = State(False)
        start.AddEpsilonTransition(self.start)
        start.AddEpsilonTransition(other.start)

        end = State(True)
        self.end.AddEpsilonTransition(end)
        self.end.is_accepted = False
        other.end.AddEpsilonTransition(end)
        other.end.is_accepted = False

        self.start = start
        self.end = end

    def Closure(self):
        start = State(False)
        end = State(True)

        start.AddEpsilonTransition(end)
        start.AddEpsilonTransition(self.start)

        self.end.AddEpsilonTransition(end)
        self.end.AddEpsilonTransition(self.start)
        self.end.is_accepted = False

        self.start = start
        self.end = end

    def NextStates(self, symbol):
        results = []
        for state in self.current_states:
            results.extend(state.NextStates(symbol))
        results = list(set(results))
        return results

    def Search(self, word):
        self.current_states.append(self.start)
        self.current_states.extend(self.start.NextStates(''))
        for c in word:
            self.current_states = self.NextStates(c)
        for state in self.current_states:
            if state.is_accepted:
                return True
        return False
