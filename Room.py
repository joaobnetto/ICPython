# Define uma classe para Sala, que sera utilizado pelo algoritmo.
# Tem como membro os mesmos parametros usado pelo Room.txt fornecido pelo Sids
# e recebe os mesmos no construtor
class Room:
	def __init__(self, uniqueId, bld, cap, roomType, special, name):
		self.uniqueId = uniqueId
		self.bld = bld
		self.cap = cap
		self.roomType = roomType
		self.special = special
		self.name = name
