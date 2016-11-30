from field import *


class DatabaseModelMetaclass(type):
	"""docstring for ModelMetaclass"""
	def __new__(cls,name,bases,attrs):
		if name == 'DatabaseModel':
			return type.__new__(cls,name,bases,attrs)

		mappings = dict()
		for k,v in attrs.iteritems():
			if isinstance(v, Field):
				mappings[k] = v
				# print('Found mapping: %s==>%s' % (k, v))
		for k in mappings.iterkeys():
			attrs.pop(k)

		attrs['__mappings__'] = mappings
		return type.__new__(cls,name,bases,attrs)


class DatabaseModel(dict):
	
	__metaclass__ = DatabaseModelMetaclass

	def __init__(self, **kw):
		super(DatabaseModel, self).__init__(**kw)
		
	def __getattr__(self,key):
		try:
			return self[key]
		except Exception, e:
			raise AttributeError(r"'Model' object has no attribute '%s'" % key)
	
	def __setattr__(self,key,value):
		self[key] = value

	def save(self):
		fields = []
		params = []
		args = []

		for k,v in self.__mappings__.iteritems():
			print k,v

			fields.append(v.name)
			params.append(str(self[k]))
			args.append(getattr(self, k,None))

		sql = 'insert into %s (%s) values(%s)' %(self.__table__,','.join(fields),','.join(params))
		print ('SQL: %s' %sql)
		print args

class User(DatabaseModel):
    
    __table__ = 'table'

    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')


if __name__ == '__main__':
	
	u = User(id=12345, name='Michael', email='test@orm.org', password='my-pwd')
	u.save()