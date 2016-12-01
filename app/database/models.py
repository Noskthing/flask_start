from field import *
from engine import *

class DatabaseModelMetaclass(type):
	"""docstring for ModelMetaclass"""
	def __new__(cls,name,bases,attrs):
		if name == 'DatabaseModel':
			return type.__new__(cls,name,bases,attrs)

		mappings = dict()
		for k,v in attrs.iteritems():
			print('Found mapping: %s==>%s' % (k, v))
			if isinstance(v, Field):
				mappings[k] = v
				
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
			params.append('?')
			args.append(getattr(self, k,None))

		sql = 'insert into %s (%s) values (%s)' %(self.__table__,','.join(fields),','.join(params))
		print ('SQL: %s' %sql)
		return update(sql,*args)

class User(DatabaseModel):
    
    __table__ = 'user'

    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')


if __name__ == '__main__':
	
	# if not engine:
	# 	create_databaseengine('root', 'lee', 'lee', '127.0.0.1')

	u = User(id=3, name='lee', email='test@orm.org', password='my-pwd')
	# print u.save()