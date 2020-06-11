#ID	Group	Solicit	Course	Entity	Day	Hour	Bld	Type	Room
class Lesson:
	def __init__(self, uniqueId, group, solicit, course, entity, day, hour, bld, roomType, cap):
		self.uniqueId = int(uniqueId)
		self.group = group
		self.solicit = solicit
		self.course = course
		self.entity = entity
		self.day = day
		self.hour = hour
		self.bld = bld
		self.roomType = roomType
		self.cap = cap
		self.room = ""

	def setRoom(self, room):
		self.room = room
