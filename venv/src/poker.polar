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