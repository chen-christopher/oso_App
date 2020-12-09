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


five(lis, v) if count(lis, _, 4, v);

four(lis, v) if count(lis, _, 3, v);

three(lis, v) if count(lis, _, 2, v);

pair(lis, v) if count(lis, _, 1, v);

count([], 0, _, _) if false;
#count([], _, _, _);


count([head, *tail], i, n, do_not_count_list, v) if (kind(tail, head, i) and i = n and (not (head in do_not_count_list)) and v = head and cut) or 
								  count(tail, i, n, do_not_count_list, v);


count([head, *tail], i, n, v) if (kind(tail, head, i) and i = n and v = head and cut) or 
								  count(tail, i, n, v);

kind([], _face, 0);

kind([face, *tail], face, n+1) if kind(tail, face, n);
kind([first, *tail], face, n) if first != face and kind(tail, face, n); # kind(tail, face, i, n);


#max(lis, comp) if forall(x in lis, (comp >= x and ((check_sequence(lis, x)))));

straight(lis1, lis2, top) if straight_util(lis1, lis2, top);

straight_util(lis, [head], top) if check_sequence(lis, head) and top = head;

straight_util(lis, [head, *tail], top) if (check_sequence(lis, head) and top = head and print(top) and cut)
															or straight_util(lis, tail, top);

#check_sequence(lis, 13) if ((4 in lis) and (3 in lis) and (2 in lis) and (1 in lis)) or ((12 in lis) and (11 in lis) and (10 in lis) and (1 in lis));

check_sequence(lis, comp) if (a = comp - 1 and a in lis) and 
								(b = comp - 2 and b in lis) and 
								(c = comp - 3 and c in lis) and 
								(d = comp - 4 and d in lis) and (e = comp + 1 and (not (e in lis)));


#samp(lis, v) if v = lis.sort();
#max(lis, comp) if forall(x in lis, comp > x);

same([], _, _, _) if false;

# Rule returns the next card with the same number, but different suit
same([head, *tail], v, card, list_of_seen_cards_suits) if  
					((v = head.number) and 
					(not (head.suit in list_of_seen_cards_suits)) and 
					(card = head.suit) and cut) or
					same(tail, v, card, list_of_seen_cards_suits);
					
					
# ((not (head.number in list_of_seen_cards_faces)) and 
max_of_remaining_cards([], _, _, _);				
max_of_remaining_cards(list_of_all_faces, [head, *tail], list_of_seen_cards_faces, card_num, card_suit) if 
					((not (head.number in list_of_seen_cards_faces)) and
					(max_util(head, list_of_all_faces, list_of_seen_cards_faces, card_num, card_suit) and cut)) or 
					(max_of_remaining_cards(list_of_all_faces, tail, list_of_seen_cards_faces, card_num, card_suit));
					
					
max_util(card_check, list_for_checking, seen_faces, card_num, card_suit) if
					forall(((x in list_for_checking) and (not (x in seen_faces))), card_check.number >= x) 
					and card_num = card_check.number
					and card_suit = card_check.suit;
				    #forall(((x in list) and 
					#	   (not (x.suit in seen_suits))), card_check.suit > x.suit) and card = card_check;
					
same_suit_diff_num([], _, _, _) if false;

# Rule returns the next card with the same suit, but different number
same_suit_diff_num([head, *tail], v, card, list_of_seen_cards_num) if 
					((v = head.suit) and 
					(not (head.number in list_of_seen_cards_num)) and 
					(card = head.number) and cut) or
					same_suit_diff_num(tail, v, card, list_of_seen_cards_num);


max_of_three(v1, v2, v3, lis) if
	(v1 > v2 and v1 > v3 and v2 > v3 and lis = [v1, v2, v3] and cut) or
	(v1 > v2 and v1 > v3 and v3 > v2 and lis = [v1, v3, v2] and cut) or
	(v2 > v1 and v2 > v3 and v1 > v3 and lis = [v2, v1, v3] and cut) or
	(v2 > v1 and v2 > v3 and v3 > v1 and lis = [v2, v3, v1] and cut) or
	(v3 > v1 and v3 > v2 and v1 > v2 and lis = [v3, v1, v2] and cut) or
	(v3 > v1 and v3 > v2 and v2 > v1 and lis = [v3, v2, v1] and cut);
	
										
# v is the card number that gets repeated 2 times
three_of_a_kind(list_of_all_cards, list_of_all_faces, result) if 
	(three(list_of_all_faces, v)) and                                       
	same(list_of_all_cards, v, card1_suit, []) and
	same(list_of_all_cards, v, card2_suit, [card1_suit]) and
	same(list_of_all_cards, v, card3_suit, [card1_suit, card2_suit]) and 
	max_of_remaining_cards(list_of_all_faces, list_of_all_cards, [v, v, v], card4_number, card4_suit) and
	max_of_remaining_cards(list_of_all_faces, list_of_all_cards, [v, v, v, card4_number], card5_number, card5_suit) and
	result = [Pattern.Trio, new Card(v, card1_suit), new Card(v, card2_suit), new Card(v, card3_suit), new Card(card4_number, card4_suit), new Card(card5_number, card5_suit)];
	
four_of_a_kind(list_of_all_cards, list_of_all_faces, result) if 
	(four(list_of_all_faces, v)) and                                       
	same(list_of_all_cards, v, card1_suit, []) and
	same(list_of_all_cards, v, card2_suit, [card1_suit]) and
	same(list_of_all_cards, v, card3_suit, [card1_suit, card2_suit]) and 
	same(list_of_all_cards, v, card4_suit, [card1_suit, card2_suit, card3_suit]) and 
	max_of_remaining_cards(list_of_all_faces, list_of_all_cards, [v, v, v, v], card5_number, card5_suit) and
	result = [Pattern.Poker, new Card(v, card1_suit), new Card(v, card2_suit), new Card(v, card3_suit), new Card(v, card4_suit), new Card(card5_number, card5_suit)];
	
flush(list_of_all_cards, list_of_all_suits, result) if print("in flush") and
	count(list_of_all_suits, _, 4, v) and
	same_suit_diff_num(list_of_all_cards, v, card1_num, []) and
	same_suit_diff_num(list_of_all_cards, v, card2_num, [card1_num]) and
	same_suit_diff_num(list_of_all_cards, v, card3_num, [card1_num, card2_num]) and 
	same_suit_diff_num(list_of_all_cards, v, card4_num, [card1_num, card2_num, card3_num]) and 
	same_suit_diff_num(list_of_all_cards, v, card5_num, [card1_num, card2_num, card3_num, card4_num]) and 
	result = [Pattern.Flush, new Card(card1_num, v), new Card(card2_num, v), new Card(card3_num, v), new Card(card4_num, v), new Card(card5_num, v)];

straight_hand(list_of_all_cards, list_of_all_faces, duplicate_list_of_all_faces, result) if print("straight_hand") and
	straight(list_of_all_faces, duplicate_list_of_all_faces, top) and print(top) and 
	same(list_of_all_cards, top, card1_suit, []) and
	same(list_of_all_cards, top - 1, card2_suit, []) and
	same(list_of_all_cards, top - 2, card3_suit, []) and
	same(list_of_all_cards, top - 3, card4_suit, []) and
	same(list_of_all_cards, top - 4, card5_suit, []) and
	result = [Pattern.Straight, new Card(top, card1_suit), new Card(top - 1, card2_suit), new Card(top - 2, card3_suit), new Card(top - 3, card4_suit), new Card(top - 4, card5_suit)];
	

straight_flush(list_of_all_cards, list_of_all_faces, duplicate_list_of_all_faces, result) if print("straight_flush") and
	straight(list_of_all_faces, duplicate_list_of_all_faces, top) and 
	same(list_of_all_cards, top, card1_suit, []) and
	same(list_of_all_cards, top - 1, card2_suit, []) and
	same(list_of_all_cards, top - 2, card3_suit, []) and
	same(list_of_all_cards, top - 3, card4_suit, []) and
	same(list_of_all_cards, top - 4, card5_suit, []) and
	(card1_suit == card2_suit) and (card2_suit == card3_suit) and (card3_suit == card4_suit) and (card4_suit == card5_suit) and
	result = [Pattern.StraightFlush, new Card(top, card1_suit), new Card(top - 1, card2_suit), new Card(top - 2, card3_suit), new Card(top - 3, card4_suit), new Card(top - 4, card5_suit)];
 


# count([head, *tail], i, n, do_not_count_list, v)
full_house_first_condition(list_of_all_cards, list_of_all_faces, result) if print("full_house_first_condition") and
	(three(list_of_all_faces, v_1)) and count(list_of_all_faces, _, 2, [v_1], v_2) and print(v_1) and print(v_2) and 
	same(list_of_all_cards, v_1, card1_suit, []) and print(card1_suit) and 
	same(list_of_all_cards, v_1, card2_suit, [card1_suit]) and print(card2_suit) and
	same(list_of_all_cards, v_1, card3_suit, [card1_suit, card2_suit]) and print(card2_suit) and print(card3_suit) and
	same(list_of_all_cards, v_2, card4_suit, []) and
	same(list_of_all_cards, v_2, card5_suit, [card4_suit]) and print(card4_suit) and
	same(list_of_all_cards, v_2, card6_suit, [card4_suit, card5_suit]) and print(card4_suit) and print(card5_suit) and
	(
		(v_1 > v_2) and result = [Pattern.FullHouse, new Card(v_1, card1_suit), new Card(v_1, card2_suit), new Card(v_1, card3_suit), new Card(v_2, card4_suit), new Card(v_2, card5_suit)] 
		and cut
	) 
	or
	(
		(v_1 < v_2) and result = [Pattern.FullHouse, new Card(v_2, card4_suit), new Card(v_2, card5_suit), new Card(v_2, card6_suit), new Card(v_1, card1_suit), new Card(v_1, card2_suit)]
	);
	
full_house_second_condition(list_of_all_cards, list_of_all_faces, result) if print("in second condition") and
	(three(list_of_all_faces, v_1)) and count(list_of_all_faces, _, 1, [v_1], v_2) and print(v_1) and print(v_2) and 
	same(list_of_all_cards, v_1, card1_suit, []) and 
	same(list_of_all_cards, v_1, card2_suit, [card1_suit]) and
	same(list_of_all_cards, v_1, card3_suit, [card1_suit, card2_suit]) and
	same(list_of_all_cards, v_2, card4_suit, []) and 
	same(list_of_all_cards, v_2, card5_suit, [card4_suit]) and
	(
		(
		
			count(list_of_all_faces, _, 1, [v_1, v_2], v_3) and  
		  
			(
				(v_3 > v_2) and print("v_3 > v_2") and 
				same(list_of_all_cards, v_3, card6_suit, []) and 
				same(list_of_all_cards, v_3, card7_suit, [card6_suit]) and
				result = [Pattern.FullHouse, new Card(v_1, card1_suit), new Card(v_1, card2_suit), new Card(v_1, card3_suit), new Card(v_3, card6_suit), new Card(v_3, card7_suit)] and print(result)
				and cut
			)
			

		 )	
		  
		  or
			(
				result = [Pattern.FullHouse, new Card(v_1, card1_suit), new Card(v_1, card2_suit), new Card(v_1, card3_suit), new Card(v_2, card4_suit), new Card(v_2, card5_suit)]
			)
			
				
		
		
		
	); 
	#or print("in the or right here ") and 
	#(result = [Pattern.FullHouse, new Card(v_1, card1_suit), new Card(v_1, card2_suit), new Card(v_1, card3_suit), new Card(v_2, card4_suit), new Card(v_2, card5_suit)]);
	

	
one_pair(list_of_all_cards, list_of_all_faces, result) if
	pair(list_of_all_faces, v) and 
	same(list_of_all_cards, v, card1_suit, []) and
	same(list_of_all_cards, v, card2_suit, [card1_suit]) and
	max_of_remaining_cards(list_of_all_faces, list_of_all_cards, [v, v], card3_number, card3_suit) and
	max_of_remaining_cards(list_of_all_faces, list_of_all_cards, [v, v, card3_number], card4_number, card4_suit) and
	max_of_remaining_cards(list_of_all_faces, list_of_all_cards, [v, v, card3_number, card4_number], card5_number, card5_suit) and
	result = [Pattern.Pair, new Card(v, card1_suit), new Card(v, card2_suit), new Card(card3_number, card3_suit), new Card(card4_number, card4_suit), new Card(card5_number, card5_suit)];
	
many_pairs(list_of_all_cards, list_of_all_faces, result) if print("many pair") and 
	pair(list_of_all_faces, v_1) and count(list_of_all_faces, _, 1, [v_1], v_2) and count(list_of_all_faces, _, 1, [v_1, v_2], v_3) and print(v_1) and print(v_2) and print(v_3) and
	max_of_three(v_1, v_2, v_3, ordered_list) and
	[a, b, c] = ordered_list and
	same(list_of_all_cards, a, card1_suit, []) and
	same(list_of_all_cards, a, card2_suit, [card1_suit]) and
	same(list_of_all_cards, b, card3_suit, []) and
	same(list_of_all_cards, b, card4_suit, [card3_suit]) and
	same(list_of_all_cards, c, card5_suit, []) and
	result = [Pattern.TwoPair, new Card(a, card1_suit), new Card(a, card2_suit), new Card(b, card3_suit), new Card(b, card4_suit), new Card(c, card5_suit)];
	
	
	
	
two_pairs(list_of_all_cards, list_of_all_faces, result) if print("two pairs") and
	pair(list_of_all_faces, v_1) and count(list_of_all_faces, _, 1, [v_1], v_2) and print(v_1) and print(v_2) and
	same(list_of_all_cards, v_1, card1_suit, []) and
	same(list_of_all_cards, v_1, card2_suit, [card1_suit]) and
	same(list_of_all_cards, v_2, card3_suit, []) and
	same(list_of_all_cards, v_2, card4_suit, [card3_suit]) and
	(
		print("v_1 > v_2") and
		(
		
			(v_1 > v_2) and 
					(
						max_of_remaining_cards(list_of_all_faces, list_of_all_cards, [v_1, v_1, v_2, v_2], card7_number, card7_suit) and
						result = [Pattern.TwoPair, new Card(v_1, card1_suit), new Card(v_1, card2_suit), new Card(v_2, card3_suit), new Card(v_2, card4_suit), new Card(card7_number, card7_suit)]
					) 
			and cut
		
		)
		
		or 
		(
			print("other") and 
			max_of_remaining_cards(list_of_all_faces, list_of_all_cards, [v_1, v_1, v_2, v_2], card8_number, card8_suit) and
			result = [Pattern.TwoPair, new Card(v_2, card3_suit), new Card(v_2, card4_suit), new Card(v_1, card1_suit), new Card(v_1, card2_suit), new Card(card8_number, card8_suit)]
		)
		

	);
	
	
high_card(list_of_all_cards, list_of_all_faces, result) if
	max_of_remaining_cards(list_of_all_faces, list_of_all_cards, [], card1_number, card1_suit) and
	max_of_remaining_cards(list_of_all_faces, list_of_all_cards, [card1_number], card2_number, card2_suit) and
	max_of_remaining_cards(list_of_all_faces, list_of_all_cards, [card1_number, card2_number], card3_number, card3_suit) and
	max_of_remaining_cards(list_of_all_faces, list_of_all_cards, [card1_number, card2_number, card3_number], card4_number, card4_suit) and
	max_of_remaining_cards(list_of_all_faces, list_of_all_cards, [card1_number, card2_number, card3_number, card4_number], card5_number, card5_suit) and
	result = [Pattern.HighCard, new Card(card1_number, card1_suit), new Card(card2_number, card2_suit), new Card(card3_number, card3_suit), new Card(card4_number, card4_suit), new Card(card5_number, card5_suit)];
	

	
	
	
	
hand(list_of_all_cards, list_of_all_faces, duplicate_list_of_all_faces, list_of_all_suits, result) if
	
	(straight_flush(list_of_all_cards, list_of_all_faces, duplicate_list_of_all_faces, result) and cut) or
	(four_of_a_kind(list_of_all_cards, list_of_all_faces, result) and cut) or
	(full_house_first_condition(list_of_all_cards, list_of_all_faces, result) and cut) or
	(full_house_second_condition(list_of_all_cards, list_of_all_faces, result) and print("") and cut) or
	(flush(list_of_all_cards, list_of_all_suits, result) and print("done2") and cut) or
	(straight_hand(list_of_all_cards, list_of_all_faces, duplicate_list_of_all_faces, result) and cut) or
	(three_of_a_kind(list_of_all_cards, list_of_all_faces, result) and cut) or
	(many_pairs(list_of_all_cards, list_of_all_faces, result) and cut) or
	(two_pairs(list_of_all_cards, list_of_all_faces, result) and cut) or
	(one_pair(list_of_all_cards, list_of_all_faces, result) and cut) or
	high_card(list_of_all_cards, list_of_all_faces, result); 
	
	
	
	
	



