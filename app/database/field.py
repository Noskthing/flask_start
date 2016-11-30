class Field(object):
	"""docstring for Field"""
	def __init__(self, name , column_type):
		self.name = name
		self.column_type = column_type

	def __str__(self):
		return '<%s : %s>' %( self.__class__.__name__,self.name)


class StringField(Field):
	"""docstnameg for StringField"""
	def __init__(self, name):
		super(StringField, self).__init__(name,'varchar(100)')


class  IntegerField(Field):
	"""docstring for  IntegerField"""
	def __init__(self, name):
		super(IntegerField, self).__init__(name,'bigint')