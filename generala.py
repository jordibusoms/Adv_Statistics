import random

def dec2hex(num):
    try:
        num=int(num)
    except:
        print("expecting an integer, obtained", num, "in function dec2hex")
    if num == 0:
        return "0"
    ans = ""
    while num > 0:
        ans = str(num%6) + ans
        num //= 6
    return (ans)

class lnk_chose_path:
    """Its a linked structure in wich, from any position (n dice 
    combination), you can "choose path" (choose the next posible output)
    Basically a tree."""
    def __init__(self, data, childs=list()):
        self.data = data
        self.childs = childs

class dice_pres(lnk_chose_path):
    """A lnk_chose_path aplied to the possible results for a dice
    The number of childs for each node must be either 6 or 0 for the model
    to have sense"""
    
    def build_n_layers(self,n):
        self.childs = [] # if there were already childs, remove them
        if n>0:
            for res in range(6):
                self.childs.append(dice_pres(res+1))
                self.childs[-1].build_n_layers(n-1)
            
    def __getitem__(self, key, n= 5):
        """Converts the key/index into base 6, then uses each digit to 
        chose the path, does not include root data"""
        current_pos = self
        convination = []
        key = dec2hex(key)
        while len(key)<n:
            key = "0"+key
        for digit in key:
            current_pos=current_pos.childs[int(digit)]
            convination.append(current_pos.data)
        return(convination)

    
    
def get_posible_outcomes(n=5):
    """Exercises 1 and 2; since exercice 2 is a generalitzation of 
    exercise 1, the soluton includes the solution to exercise 1"""
    pos_outcomes = dice_pres(0)
    pos_outcomes.build_n_layers(n)
    return pos_outcomes # It is not a list as I gess it was expected but
    # a tree. This alternative representation can be acces and traversed
    # like a list while will be slighly slower to do so. On the other 
    # hand, should be kiquer to create and more space eficient.
    # It also probides an intuitive way to locate the possible final 
    # outcomes for those cases with giben partial results.


def asses_generala_result(res):
    """Assumes it is giben a list with 5 numbers from the dice results"""
    setres = set(res)
    if len(setres)==5:
        return("Stright")
    if len(setres)==1:
        return("Generala")
    if len(setres)==2:
        if res.count(res[0]) in {1,5}:
            return("Poker")
        if res.count(res[0]) in {2,3}:
            return("Full")
    return("Not interesting for this exercise")

def generala_round(prev=[False]*5, keep=[False]*5):
    for dice in range(len(prev)):
        if not keep[dice]:
            prev[dice]= random.randint(1,6)
    return prev

def interactive_generala():
    """Just for fun/ to see everything is working properly"""
    print("rolling dices")
    round_results = generala_round()
    for i in range(2):
        print("This are your results\n"+str(round_results)+"\nWhat dices you want to keep?")
        keeping=input("Enter dice index (starting from 1) seperated by spaces ")
        to_keep=[False]*5
        for index in keeping.split():
            try:
                to_keep[int(index)-1]=True
            except:
                print(index, "is not a valid index, it will be ommited.")
        round_results = generala_round(round_results, to_keep)
    print("This are your final results\n"+str(round_results))
    print(asses_generala_result(round_results))

interactive_generala()
