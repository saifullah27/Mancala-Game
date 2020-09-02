#this class represent the game state and provides helper function such as print state, evalutate state and winning conditions
class State:
    def __init__(self, state):
        self.state = state  # game state
        self.player1_store = 6   # left side
        self.player2_store = 13  # right side

    def copy(self, newstate):
        for i in range(0,14):
            self.state[i] = newstate.getState()[i]

    def getState(self):
        return self.state

    def at(self, i):
        return self.state[i]

    def set(self,index,value):
        self.state[index] = value

    def getPlayer1(self):
        s = ""
        for i in range(0, 6):
            s = s + str(self.state[i]) + " "
        print("Player1|Store:" + str(self.state[6]) + "|" + s)

    def getPlayer2(self):
        s = ""
        i = 12
        while i > 6:
            s = s + str(self.state[i]) + " "
            i= i - 1
        print("Player2|Store:" + str(self.state[13]) + "|" + s)

    def getPlayer1StoreIndex(self):
        return self.player1_store

    def getPlayer2StoreIndex(self):
        return self.player2_store

    def getPlayer1Store(self):
        return self.state[self.player1_store]

    def getPlayer2Store(self):
        return self.state[self.player2_store]

    def show(self):
        print("_____________________________________")
        self.getPlayer2()
        self.getPlayer1()
        print("_____________________________________")

    def is_humanvsagent(self):
        print("Game Over")
        if self.state[6] > self.state[13]:
            print("Agent wins!")
        elif self.state[13] > self.state[6]:
            print("Human wins.")
        else:
            print("Draw")

    def is_agentvsagent(self):
        print("Game Over")
        if self.state[6] > self.state[13]:
            print("Agent1 wins!")
        elif self.state[13] > self.state[6]:
            print("Agent2 wins.")
        else:
            print("Draw")

    # this function counts stones in left side pits
    def count_left_side_stones(self):
        count = 0
        for i in range(0,6):
            count = count + self.at(i)
        return count

    # this function counts stones in right side pits
    def count_right_side_stones(self):
        count = 0
        for i in range(7,13):
            count = count + self.at(i)
        return count

    def eval_left_side(self):  # human side
        stones =  self.count_left_side_stones()
        store = (self.at(6))
        total = stones + store
        return total

    def eval_right_side(self):  # agent side
        stones = self.count_right_side_stones()
        store = (self.at(13))
        total = stones + store
        return total

    # retunn store index of current player
    def whoplaying(self,turn):
        if 1 == turn:  # comp playing
            return 6# human
        return 13# agent
