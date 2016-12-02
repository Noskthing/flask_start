class Field(object):
	
	_count = 0
	def __init__(self, **kw):
		self.name = kw.get('name',None)
		self._default = kw.get('default',None)
		self.primary_key = kw.get('primary_key', False)
		self.nullable = kw.get('nullable',False)
		self.updateable = kw.get('updateable',True)
		self.insertable = kw.get('insertable',True)
		self.ddl = kw.get('ddl','')
		self._order = Field._count

		Field._count += 1

	@property
	def default(self):
		
		return self._default() if callable(self._default) else self._default

	def __str__(self):

		res = ['<%s:%s,%s,default(%s),' %(self.__class__.__name__,self.name,self.ddl,self._default)]

		self.nullable and res.append('N')
		self.insertable and res.append('I')
		self.updateable and res.append('U')

		res.append('>')
		return ''.join(res)


class StringField(Field):
	"""
	save string type property
	"""

	def __init__(self, **kw):
		if 'default' not in kw:
			kw['default'] = ''
		if 'ddl' not in kw:
			kw['ddl'] = 'varchar(255)'
		super(StringField,self).__init__(**kw)


class  IntegerField(Field):
	"""
	save integer type property
	"""

	def __init__(self, **kw):
		if 'default' not in kw:
			kw['default'] = 0
		if 'ddl' not in kw:
			kw['ddl'] = 'bigint'
		super(IntegerField,self).__init__(**kw)

class FloatField(Field):
	"""
	save float type property
	"""

	def __init__(self, **kw):
		if 'default' not in kw:
			kw['default'] = 0.0
		if 'ddl' not in kw:
			kw['ddl'] = 'real'
		super(FloatField,self).__init__(**kw)
		
class TextField(Field):
	"""
	save text type property
	"""

	def __init__(self, **kw):
		if 'default' not in kw:
			kw['default'] = ''
		if 'ddl' not in kw:
			kw['ddl'] = 'text'
		super(TextField,self).__init__(**kw)

class BlobField(Field):
	"""
	save blob type property
	"""

	def __init__(self, **kw):
		if 'default' not in kw:
			kw['default'] = ''
		if 'ddl' not in kw:
			kw['ddl'] = 'blob'
		super(BlobField,self).__init__(**kw)

class VersionField(Field):
	"""
	save version type property
	"""

	def __init__(self, **kw):
		super(BlobField,self).__init__(name = name ,default = 0, ddl = 'bigint')