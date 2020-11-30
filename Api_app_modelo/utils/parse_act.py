def parseAct (week_result):
	parsed_acts = [] # lista de diccionarios
	day_count = 0
	week_day = ""
	for day in week_result:
		if day_count == 0:
			week_day = "Lunes"
		elif day_count == 1:
			week_day = "Martes"
		elif day_count == 2:
			week_day = "Miércoles"
		elif day_count == 3:
			week_day = "Jueves"
		elif day_count == 4:
			week_day = "Viernes"
		elif day_count == 5:
			week_day = "Sábado"
		elif day_count == 6:
			week_day = "Domingo"

		act_count = 1
		for act in day:
			begin, end ,act = act
			if act.name is not None:
				print("name", act.name)

				init_am_pm = "p. m"
				init_hours = str(begin).split()[1][0:2]
				init_hours = int(init_hours)
				if init_hours > 12:
					init_hours = init_hours -12
				else:
					init_am_pm = "a. m"
				init_hours = str(init_hours)
				init_mins = str(begin).split()[1][3:5]

				final_am_pm = "p. m"
				final_hours = str(end).split()[1][0:2]
				final_hours = int(final_hours)
				if final_hours > 12:
					final_hours = final_hours -12
				else:
					final_am_pm = "a. m"
				final_hours = str(final_hours)
				final_mins = str(end).split()[1][3:5]

				new_act = {
				"order": str(act_count),
				"label" : act.name,
				"date" : str(begin).split()[0].split("-")[2] + "/" + str(begin).split()[0].split("-")[1],  # no se usa
				"init_time" : init_hours + ":" + init_mins + " " + init_am_pm,
				"end_time" : final_hours + ":" + final_mins + " " + final_am_pm, 
				"week_day": week_day
				}

				parsed_acts.append(new_act)

				act_count += 1

		day_count += 1

	return parsed_acts	

