import operator

from Lesson import Lesson
from Room import Room
from Flow import Graph

# Valores constantes
roomsFileName = "SIDS/Rooms.txt"
lessonsFileInputName = "SIDS/Lessons.txt"
lessonsFileOutputName = "Output/Lessons.txt"
#Indexação de 1 até x, logo coloco x+1
weekLength = 7
hourLength = 18
dataDefaultLen = 14
percentagePrecison = 0.30 # Aumentar se necessário
defaultPriorityWeight = int(-100)

def calculateCost(room, lesson):
	weight = (lesson.priori * defaultPriorityWeight) + abs(room.cap - lesson.vacan)
	return weight


# Essa função recebe um conjunto de salas(Rooms) e aulas(Lessons)
# já separadas por dia e horários, cria aresta entre os dois se os 
# argumentos batem, com um peso definido pela função calculateCost
# O parametro finalLessons são as aulas que já foram alocadas.
def assignLessonsToRoom(Rooms, Lessons, finalLessons):
	edges = []
	startOfRooms = len(Lessons)
	totalSize = len(Lessons) + len(Rooms) + 2
	destiny = totalSize - 1
	source = 0
	roomCount = 1

	for room in Rooms:
		edges.append([startOfRooms + roomCount, destiny, 0, 1])
		for lesson in Lessons:
			minCapacity = (int) (room.cap - room.cap * percentagePrecison)
			maxCapacity = (int) (room.cap + room.cap * percentagePrecison)
			if(int(room.bld) == int(lesson.bld) and int(room.roomType) == int(lesson.roomType) 
				and minCapacity <= lesson.vacan and maxCapacity >= lesson.vacan):
				cost = calculateCost(room, lesson)
				edges.append([lesson.tmpId, startOfRooms + roomCount, cost, 1])

		roomCount += 1
	for lesson in Lessons:
		edges.append([source, lesson.tmpId, 0, 1])
	graph = Graph(totalSize)
	flow = graph.minCostFlow(source, destiny, edges)

	for lesson in Lessons:
		result = graph.flowPathFromVertex(lesson.tmpId)
		if(result != -1):
			roomIdx = result-startOfRooms
			lesson.setRoom(Rooms[roomIdx].uniqueId)
			finalLessons.append(lesson)
		else:
			lesson.setRoom(-1)
			finalLessons.append(lesson)

# Separa as aulas por horarios e dias
def alocarPorHorarios():
	rooms = readRoomsFromArchive()
	allLessons = readLessonsFromArchive()
	finalLessons = []

	for day in range(1,weekLength):
		for hour in range(1, hourLength):
			currentLessons = []
			lessonCount = 1
			for lesson in allLessons:
				if(int(lesson.day) == day and int(lesson.hour) == hour):
					lesson.tmpId = lessonCount
					lessonCount += 1
					currentLessons.append(lesson)

			assignLessonsToRoom(rooms, currentLessons, finalLessons)

	writeAllocationToArchive(finalLessons)

# Importante que o arquivo esteja definido como:
# ID Bld Cap Type Special Name
# Pois é acessado diretamente por índice
def readRoomsFromArchive():
	file = open(roomsFileName)
	rooms = []
	# Não precisa ler a primeira linha, apenas definições
	file.readline()
	for currentLine in file:
		data = currentLine.split()
		# Junta o nome, caso o de cima separe.
		name = " ".join(data[5:])
		room = Room(data[0], data[1], data[2], data[3], data[4], name)
		rooms.append(room)
	file.close()
	return rooms


# Importante que o arquivo esteja definido como:
# ID Group Solicit Course Entity Day Hour Bld Type Room Vacan Matric Priori Special
# Pois é acessado diretamente por índice
def readLessonsFromArchive():
	file = open(lessonsFileInputName)
	lessons = []
	# Não precisa ler a primeira linha, apenas definições
	file.readline()
	for currentLine in file:
		data = currentLine.split()
		# Se estiver faltando um costuma ser room, adiciono ela
		if(len(data) != dataDefaultLen):
			data.insert(9, 0)
		# Se o tamanho não estiver correto ainda, está mal formatado
		# logo não adiciono.
		# TODO: Adicionar logging dos pedidos que estão falhos.
		if(len(data) != dataDefaultLen):
			continue
		# Placeholder
		data[9] = -1
		lesson = Lesson(data[0], data[1], data[2], data[3], data[4],
				 data[5], data[6], data[7], data[8], data[9], data[10],
				 data[11], data[12], data[13])
		lessons.append(lesson)
	file.close()
	return lessons

def writeAllocationToArchive(finalLessons):
	# Abre pra pegar emprestado o header
	file = open(lessonsFileInputName)
	header = file.readline()
	file.close()

	file = open(lessonsFileOutputName, "w")
	file.write(header)
	finalLessons.sort(key=operator.attrgetter('uniqueId'))
	count = 0
	for lesson in finalLessons:
		count = count + 1 if lesson.room == -1 else count
		memberList = [lesson.uniqueId, lesson.group, lesson.solicit,
					 lesson.course, lesson.entity, lesson.day, lesson.hour,
					 lesson.bld, lesson.roomType, lesson.room, lesson.vacan,
					 lesson.matric, lesson.priori, lesson.special, "\n"]
		line = " ".join(map(str, memberList))
		file.write(line)
	print(count)
alocarPorHorarios()