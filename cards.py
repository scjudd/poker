class Card(object):
    RANKS = (None,'2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace')
    SUITS = {'d':'Diamonds','c':'Clubs','s':'Spades','h':'Hearts'}

    def __init__(self, rank, suite):
        self.rank = self.RANKS[rank]
        self.value = rank
        self.suit = self.SUITS[suite]

    def __str__(self):
        return "{0} of {1}".format(self.rank, self.suit)

    def __repr__(self):
        return "{0}({1},'{2}')".format(self.__class__.__name__, self.value, self.suit.lower()[0])

    def __eq__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        return self.value > other.value

class Deck(list):
    def __init__(self, card_class=Card):
        list.__init__(self, [card_class(v,s) for v in xrange(1,14) for s in 'dcsh'])
        self.shuffle()

    def shuffle(self):
        import random; random.shuffle(self)
        return self

    def draw(self, n):
        return [self.pop(0) for i in xrange(0,n)]

class Hand(list):
    def __init__(self, deck):
        self.deck = deck
        list.__init__(self, self.deck.draw(5))
        self.sort()

    def discard(self, indexes):
        deck.append([self.pop(i) for i in indexes])
        return self

    @property
    def score(self):
        vals = [x.value for x in self]
        s = set(vals)
        counts = sorted(zip(map(vals.count,s),s))
        pairs = [self[n:n+2] for n in xrange(0,len(self)-1)]

        def score_tree(root):
            return [root] + [counts[-x][1] for x in xrange(1,len(counts)+1)]

        # this hand is actually an A-5 straight/ sflush
        if counts == [(1,1),(1,2),(1,3),(1,4),(1,14)]:
            if all([c.suit == self[0].suit for c in self[1:]]):
                return score_tree(8) # straight flush
            return score_tree(4) # straight

        # normal hand logic
        if all([c2.value == c1.value+1 for c1, c2 in pairs]):
            if all([c.suit == self[0].suit for c in self[1:]]):
                return score_tree(8) # straight flush
        if counts[-1][0]==4:
            return score_tree(7) # four of a kind
        if counts[-1][0]==3:
            if counts[0][0]==2:
                return score_tree(6) # full house
        if all([c.suit == self[0].suit for c in self[1:]]):
            return score_tree(5)
        if all([c2.value == c1.value+1 for c1, c2 in pairs]):
            return score_tree(4) # straight
        if counts[-1][0]==3:
            return score_tree(3) # three of a kind
        if counts[-1][0]==2:
            if counts[1][0]==2:
                return score_tree(2) # two pair
            return score_tree(1) # one pair
        return score_tree(0) # high card

    def __eq__(self, other):
        return self.score == other.score

    def __gt__(self, other):
        return self.score > other.score
        


if __name__ == '__main__':
    deck = Deck()
    print [str(card) for card in deck]
    print

    h1, h2, h3 = Hand(deck), Hand(deck), Hand(deck)
    print "Hand 1: {0:<100} Score: {1}".format([str(card) for card in h1], h1.score)
    print "Hand 2: {0:<100} Score: {1}".format([str(card) for card in h2], h2.score)
    print "Hand 3: {0:<100} Score: {1}".format([str(card) for card in h3], h3.score)
    print

    hands = [h1, h2, h3]
    hands.sort()

    print "Winning Hand: {0:<94} Score: {1}".format([str(card) for card in hands[-1]], hands[-1].score)
