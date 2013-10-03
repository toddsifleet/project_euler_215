from itertools import combinations, product
import sys

#project euler problem 215

#define block widths
a_width = 2
b_width = 3


def flatten(sub_list, depth):
  #a simple function to flatten a list of list to a set depth
  if depth == 0: return sub_list
  output = []
  for i in sub_list:
    output.extend(flatten(i, depth - 1))
  return output


def find_counts(width):
  '''
  each row of the structure consists of a set number of "a_blocks" = a
  and "b_blocks" = b.  This generator yields all combinations
  of a and b such that a*a_width + b*b_width = width.
  '''
  for a in range(width / a_width + 1):
    if not (width - a_width * a) % b_width:
      b = (width - a_width * a) / b_width
      yield (a, b)


def find_permutations(block_counts):
  '''
  given an iterator containing tuples (a1,b1), (a2, b2)... this function
  returns  a list of all possible permutations in the form:
  [<integer of seams>, <compatible list>,  <count>, <old_count>]
  '''
  perms = (([],[]),([],[]))
  for block_count in block_counts:
    blocks = range(sum(block_count))
    #loop through each combination of a_block locations
    for a_blocks in combinations(blocks, block_count[0]):
      length = 0 
      seams = 0 #a large integer where each bit represents a seam
      #loop through and find the seam locations, ignore the final seam
      for i in blocks[0:-1]:
        length += a_width if i in a_blocks else b_width
        seams |= 1 << length
      #we seperate the combos based on their first and last blocks
      first = 0 if 0 in a_blocks else 1
      last = 0 if len(blocks)-1 in a_blocks else 1
      last ^= first
      perms[first][last].append([seams, [], 1, 0])
      
  find_compatible(perms)
  return flatten(perms, 2)


def find_compatible(perms):
  '''
  given 4 unique lists [[[A/A],[A/B]],[[B/B],[B/A]]] containing all
  permutations this function loops through each viable pair
  (different first and last blocks) to see if they are compatible,
  if they are each one is added to the others compatible list
  '''
  for sub_sets in zip(*perms):
    #compare to perms that have different first and last blocks
    for p1, p2 in product(*sub_sets):
      #not (seams1 & seams2) => the combos do not share any seams
      if not (p1[0] & p2[0]):
        #add them to each others compatible list
        p1[1].append(p2)
        p2[1].append(p1)
    

def find_count(perms, level):
  '''
  given the number of levels and all possible block permutations this function
  returns the total number of satisfactory combinations
  '''
  if level == 1: return sum([perm[2] for perm in perms])
  #loop through each perm and store the old count, reset the new count
  for perm in perms:
    perm[2:3] = [0, perm[2]]
  
  for perm in perms:
    #loop through each combos compatible list
    for partner in perm[1]:
      #add old_count to each compatible combo's count
      partner[2] += perm[3]
      
  return find_count(perms, level - 1)
  

def calculate(w, h):
  if float(w) % 1: raise(ValueError)
  #we multiply by two to get rid of floats
  width = int(w)
  levels = int(h)
  #find all possible combinations that satisfy a*a_width + b*b_width = width
  block_counts = find_counts(width)
  #find all permutations that satisfy the block counts
  permutations = find_permutations(block_counts)
  #find the number of combinations that can be built 
  return find_count(permutations, levels)


if __name__=='__main__':
  from timeit import Timer
  #average runtime over 10 runs
  t = Timer("print calculate(*sys.argv[1::])", "from __main__ import calculate")
  print t.timeit(number= 10)/10.

