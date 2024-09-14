import sys; args = sys.argv[1:]
from time import perf_counter


global STATS
STATS = {}

with open(args[0]) as f:
  lst = [list(line.strip()) for line in f]
  
def setGlobals(num):
  global rowConstraintSet, colConstraintSet, subBlockConstraintSet, nbrs, totalConstraints, overlapBlocks, symbolSet, dreiCS
  pzlSize = len(lst[num])
  constraintSize = int(pzlSize ** .5)
  subBlockHeight = -1
  k = int(constraintSize ** .5)
  while k < constraintSize and subBlockHeight == -1:
    if constraintSize % k == 0:
      subBlockHeight = k
    k += 1
  subBlockWidth = constraintSize // subBlockHeight
  #g=input()
  #print(subBlockWidth, subBlockHeight, constraintSize)
  symbols = set("123456789ABCDEFGHIJKLMNOPQRSTUVQXYZ")
  symbolSet = set()
  for x in lst[num]:
    if x!=".":
      symbolSet.add(x)
  xor = sorted(symbols - symbolSet)
  while len(symbolSet)<constraintSize:
    toAdd = xor.pop(0)
    symbolSet.add(toAdd)
  #list(symbolSet).sort()
  #symbolSet = set(symbols[:constraintSize])
  rowConstraintSet = [frozenset({i for i in range(r * constraintSize, (r + 1) * constraintSize)}) for r in range(constraintSize)]
  colConstraintSet = [frozenset({i for i in range(c, c + pzlSize - subBlockWidth * subBlockHeight + 1, subBlockWidth * subBlockHeight)}) for c in range(constraintSize)]
  subBlockConstraintSet = [frozenset({bR + bCO + r * constraintSize + c for r in range(subBlockHeight) for c in range(subBlockWidth)}) for bR in
                           range(0, pzlSize, subBlockHeight * constraintSize) for bCO in range(0, constraintSize, subBlockWidth)]
  totalConstraints = rowConstraintSet + colConstraintSet + subBlockConstraintSet
  nbrs = [set().union(*[cs for cs in totalConstraints if d in cs]) - {d} for d in range(pzlSize)]
  # parallelRows = [(a, b) for idx, a in enumerate(rowConstraintSet) for b in rowConstraintSet[idx + 1:]]
  # parallelCols = [(x, y) for idx, x in enumerate(colConstraintSet) for y in colConstraintSet[idx + 1:]]
  #print(subBlockConstraintSet)
  '''
  dreiCS = {i:[] for i in range(pzlSize)}
  for i in dreiCS:
    dreiCS[i].append(rowConstraintSet[i//constraintSize])
    dreiCS[i].append(colConstraintSet[i%constraintSize])
  for j in subBlockConstraintSet:
    for w in j:
      dreiCS[w].append(j) '''
  overlapBlocks = {cs: [(bs, inters) for bs in subBlockConstraintSet if len(inters := cs.intersection(bs)) == 3] for cs
                   in rowConstraintSet + colConstraintSet}


#setGlobals(0)


def forward_looking(board):
  solved_indices = [i for i in board if len(board[i]) == 1]
  #else: solved_indices = [k for i in dreiCS[idx] for k in i if len(board[k]) == 1]
  
  for k in solved_indices:
    # updateStats(f"choice ct{len(board[k])}")
    for n in nbrs[k]:
      board[n] = board[n].replace(board[k], "")
      if len(board[n]) == 1:
        if n not in solved_indices:
          solved_indices.append(n)
      if len(board[n]) == 0: return None
  return board


def squares1Optimization(cs, board):
  squares = set()
  dupSqrs = set()
  length = 0
  for j in cs:
    if len(board[j]) == 2:
      squares.add(board[j])
      if len(squares) == length:
        dupSqrs.add(board[j])
      else:
        length += 1
  for sq in dupSqrs:
    for k in cs:
      if board[k] != sq:
        for ch in sq:
          board[k] = board[k].replace(ch, "")
  return board


def squares2Optimization(cs, board):
  counts = {}
  symbLocs = {}
  for idx in cs:
    for symb in board[idx]:
      if symb in counts:
        counts[symb] += 1
        symbLocs[symb].add(idx)
      else:
        counts[symb] = 1
        symbLocs[symb] = {idx}
  locs = [symbLocs[c] for c in counts if counts[c] == 2]
  cFetch = [c for c in counts if counts[c] == 2]
  for i, loc in enumerate(locs):
    firstSymb = cFetch[i]
    secondSymb = cFetch[locs.index(loc)]
    if firstSymb != secondSymb:
      board[loc.pop()] = f'{firstSymb}{secondSymb}'
      board[loc.pop()] = f'{firstSymb}{secondSymb}'
  return board


def overlapOptimization(cs, board):
  # for cSet in rowConstraintSet+colConstraintSet:
  for bSet in overlapBlocks[cs]:
    overlap = bSet[1]
    # if len(overlap)==3:
    for sym in symbolSet:
      overlapCheck = [sym in board[o] for o in overlap].count(True) > 0
      if overlapCheck and all([sym not in board[h] for h in bSet[0] - overlap]):
        for v in cs - overlap:
          board[v] = board[v].replace(sym, "")
      if overlapCheck and all([sym not in board[h] for h in cs - overlap]):
        for w in bSet[0] - overlap:
          board[w] = board[w].replace(sym, "")
  return board


def get_most_constrained_idx(board):
  lst = []
  for i in board:
    if len(board[i]) == 2:
      return i
    if len(board[i]) > 1:
      lst.append((len(board[i]), i))
  
  return min(lst)[1]
  # return min([(len(board[i]), i) for i in board if len(board[i]) > 1])[1]


def constraint_propagation(board,idx):
  for cs in totalConstraints:
    board = squares1Optimization(cs, board)
    board = squares2Optimization(cs, board)
    board = overlapOptimization(cs, board) if cs not in subBlockConstraintSet else board
    for symbol in symbolSet:
      # updateStats(f"choice ct{len(board[int(symbol)])}")
      val_indices = [index for index in cs if symbol in board[index]]
      if len(val_indices) == 1: board[val_indices[0]] = symbol
    # count+=1
  return board


def updateStats(toUpdate):
  if toUpdate in STATS:
    STATS[toUpdate] += 1
  else:
    STATS[toUpdate] = 1

def solveOP(pzl,index):
  count = 0
  for i in pzl:
    if len(pzl[i]) > 1: break
    count += 1
  if count == 81: return pzl
  # if all([len(pzl[i])==1 for i in pzl]): return pzl
  pzl = constraint_propagation(pzl,index)
  # pzl = overlap2Opt(pzl)
  # if all([len(pzl[i])==1 for i in pzl]): return pzl
  
  try:
    idx = get_most_constrained_idx(pzl)
  except:
    return pzl
  for val in pzl[idx]:
    new_pzl = pzl.copy()
    new_pzl[idx] = val
    # checked_board = constraint_propagation(new_pzl)
    checked_board = forward_looking(new_pzl)
    
    if checked_board is not None:
      result = solveOP(checked_board,idx)
      if result is not None: return result
  return None


#checkSum = lambda pzl: sum([ord(i) - 49 for i in pzl])
checkSum = lambda pzl: sum([ord(c) for c in pzl]) - len(pzl)*ord(min(pzl))
start = perf_counter()
conStart = perf_counter()



for n in range(len(lst)):
  line1 = str(n + 1) + "  : " + ''.join(lst[n])
  indx = line1.find(':') + 2
  line2 = ''.join([' ' for i in range(indx)])
  pDict = {}
  setGlobals(n)
  for i, item in enumerate(lst[n]):
    if item == '.':
      pDict[i] = ''.join(symbolSet)
    else:
      pDict[i] = item
  pDict = forward_looking(pDict)
  sPzl = solveOP(pDict,-1)
  end = perf_counter()
  tmpEnd = perf_counter()
  tim = f"{end - start:.4g}s"
  sPzlJoin = ''
  for i in sPzl:
    sPzlJoin += sPzl[i]
  line2 += sPzlJoin + " " + str(checkSum(sPzlJoin)) + " " + tim
  start = tmpEnd
  print(line1)
  print(line2)

end = perf_counter()
print(f"Total time: {end - conStart:.3g}s")

# print(STATS)
