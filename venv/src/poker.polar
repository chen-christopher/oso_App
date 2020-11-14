# unique - takes in a list, and returns all unique elements of the list
unique([head, *tail], elem) if
   head = elem
   and not (elem in tail);

unique([_head, *tail], elem) if
   unique(tail, elem);

count(list, elem, count) if
   unique(list, elem) and
   count_elems(list, elem, count);

# count number of elements in the list

## Base case: N=0
count_elems([], _elem, 0);

## Next case: N=1
# count_elems([elem], elem, 1);
# count_elems([other], elem, 0) if not (elem = other);

## General case: N=k
count_elems([elem, *tail], elem, count + 1) if
   ## recursively call count_elems
   ## on the tail of k-1 elements
   count_elems(tail, elem, count)
   and cut;

count_elems([_other, *tail], elem, count) if
   count_elems(tail, elem, count);


## Alternate approach using Python builtins
# alt_count_elems(list, elem, count) if
#    count = list.count(elem);





straight(lis1, lis2, top) if straight_util(lis1, lis2, top);

straight_util(lis, [head], top) if check_sequence(lis, head) and top = head;

straight_util(lis, [head, *tail], top) if (check_sequence(lis, head) and top = head and cut) or straight_util(lis, tail, top);

#check_sequence(lis, 13) if ((4 in lis) and (3 in lis) and (2 in lis) and (1 in lis)) or ((12 in lis) and (11 in lis) and (10 in lis) and (1 in lis));

check_sequence(lis, comp) if (a = comp - 1 and a in lis) and (b = comp - 2 and b in lis) and (c = comp - 3 and c in lis) and (d = comp - 4 and d in lis);


 
