lessonsFileName = "Output/Lessons.txt"
buildingsFileName = "SIDS/Buildings.txt"
hoursFileName = "SIDS/Hours.txt"
reservationsFileName = "SIDS/Reservations.txt"
roomsFileName = "SIDS/Rooms.txt"
outputCsv = "Output/Rooms.csv"

diasDaSemana = "Segunda,Terca,Quarta,Quinta,Sexta,Sabado,Domingo\n"
hours = []
hourCount = 17

def readRooms():
	file = open(roomsFileName)
	file.readline()
	rooms = {}
	for currentLine in file:
		data = currentLine.split()
		if len(data) != 6:
			data.append("Sem nome") 
		room = [data[5], data[1]]
		rooms[data[0]] = room
	return rooms

def readLessons():
	file = open(lessonsFileName)
	file.readline()
	lessons = {}
	for currentLine in file:
		data = currentLine.split()
		itemList = [data[5], data[6], data[9], data[1]]
		lessons[data[0]] = itemList
	return lessons

def readBuildings():
	file = open(buildingsFileName)
	file.readline()
	buildings = {}
	for currentLine in file:
		data = currentLine.split()
		buildings[data[0]] = data[2]
	return buildings

def readHours():
	file = open(hoursFileName)
	file.readline()
	for currentLine in file:
		data = currentLine.split()
		line = [data[1], "-", data[2]]
		hour = " ".join(line)
		hours.append(hour)

def readReservations():
	file = open(reservationsFileName)
	file.readline()
	reservations = {}
	for currentLine in file:
		data = currentLine.split()
		while(len(data) < 8):
			data.insert(6, "-1")
		name = " ".join(data[7:])
		reservations[data[1]] = name
	return reservations	

def outputToCsv(rooms, lessons, buildings, reservations):
	file = open(outputCsv, "w")
	for room in rooms:
		data = rooms[room]
		header = ["Sala:", data[0], ",", "Prédio:", buildings[data[1]], ",", diasDaSemana]
		file.write(" ".join(header))
		currentHour = 1
		for hour in hours:
			line = [hour]
			for currentDay in range(1, 7):
				line.append(",")
				for lesson in lessons:
					lessonData = lessons[lesson]
					# print(lessonData)
					if(int(lessonData[0]) == int(currentDay) and int(lessonData[1]) == int(currentHour) and
						int(lessonData[2]) == int(room)):
						line.append(reservations[lessonData[3]])
						break
			line.append("\n")
			file.write(" ".join(line))
			currentHour = currentHour + 1


rooms = readRooms()
lessons = readLessons()
buildings = readBuildings()
reservations = readReservations()
readHours()
outputToCsv(rooms, lessons, buildings, reservations)