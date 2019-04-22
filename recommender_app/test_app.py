from recommender.controller import Controller


def test_cntlr():
    contr = Controller()
    return contr.get_id('c@northeastern.edu')


print(test_cntlr())
