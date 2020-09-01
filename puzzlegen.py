import random
def generate_puzzle():
    lst = [0,1,2,3,4,5,6,7,8]
    solvable = False
    while not solvable:
        random.shuffle(lst)
        solvable = check_solvable(lst)

    pzl = []
    for i in range(3):
        row = []
        row.append(lst.pop())
        row.append(lst.pop())
        row.append(lst.pop())
        pzl.append(row)
        
    return pzl

def getInvCount(arr, n): 
    inv_count = 0
    for i in range(n): 
        for j in range(i + 1, n): 
            if (arr[i] > arr[j]): 
                inv_count += 1
  
    return inv_count 

def check_solvable(puzzle):
    return getInvCount(puzzle,len(puzzle)) % 2 == 0


# s = generate_puzzle()
# print(s)