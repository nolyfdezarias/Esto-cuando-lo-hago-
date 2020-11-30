def convertActToListOfTuples(acts_list):

	# print("aqui" + 50*"$")
	# print("act_list", acts_list)

	entry_list = []

	for act in acts_list:
		date = act["date"].split(",")[1]
		month = int(date.split("/")[1])
		day = int(date.split("/")[0])
		# time = act["time"].strip(" .amp")
		time = act["time"]
		hours = int(time.split(":")[0])
		mins = int(time.split(":")[1])

		
		l = act["label"]
		p = int(act["priority"])
		y = int(act["year"])
		mo = month
		d = day
		h = hours
		m = mins

		act_tuple = (l, p, y, mo, d, h, m) 
		entry_list.append(act_tuple)

	return entry_list

def convertActToTuple(act):

	# print("aqui" + 50*"$")
	print("act", act)

	date = act["date"].split(",")[1]
	month = int(date.split("/")[1])
	day = int(date.split("/")[0])
	# time = act["time"].strip(" .amp")
	time = act["time"]
	hours = int(time.split(":")[0])
	mins = int(time.split(":")[1])

	
	l = act["label"]
	p = int(act["priority"])
	y = int(act["year"])
	mo = month
	d = day
	h = hours
	m = mins

	act_tuple = (l, p, y, mo, d, h, m) 

	return act_tuple

'''

act_list = [
    ("F Nemo" , 1 , 2020 , 10 , 14 , 10,0),
    ("Examen" , 3, 2020, 10,14,10,0),
    ("V Ame" , 3,2020,10,12,13,0),
    ("V Movie" , 1, 2020,10,13,11,0),
    ("I Teatro" , 3, 2020,10,13,11,0),
    ("V Russ", 2, 2020,10,12,13,0),
    ("C Pizza", 2 , 2020,10,13,11,0)
] 

'''