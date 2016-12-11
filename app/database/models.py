from field import IntegerField,StringField,Field
import engine as db

import logging

_triggers = frozenset(['pre_insert', 'pre_update', 'pre_delete'])

def _gen_sql(table_name,mappings):
	
	pk = None
	sql = ['-- generating SQL for %s' % table_name , 'create table %s (' % table_name]
	for f in sorted(mappings.values(),lambda x,y : cmp(x._order,y._order)):
		if not hasattr(f,'ddl'):
			raise StandardError('no ddl in field "%s" !',f)

		ddl = f.ddl
		nullable = f.nullable

		if f.primary_key:
			pk = f.name
		sql.append('%s %s ,' %(f.name,ddl) if nullable else ' %s %s not null,' %(f.name,ddl))
	sql.append(' primary key( %s )' %pk)
	sql.append(');')

	return '\n'.join(sql)

class DatabaseModelMetaclass(type):
	"""docstring for ModelMetaclass"""
	def __new__(cls,name,bases,attrs):
		if name == 'DatabaseModel':
			return type.__new__(cls,name,bases,attrs)

		mappings = dict()
		primary_key = None

		for k,v in attrs.iteritems():
			# print('Found mapping: %s==>%s' % (k, v))
			if isinstance(v, Field):
				v.name = k

				if v.primary_key:
					if primary_key:
						raise TypeError('Cannot define more than 1 primary_key in class %s',name)
					if v.updateable:
						logging.warning('Note: change primary_key to non-updateable')
						v.updateable = False
					if v.nullable:
						logging.warning('Note: change primary_key to non-nullable')
					v.nullable = False
					primary_key = v

				mappings[k] = v

		if not primary_key:
			raise TypeError('primary_key not define in class %s',name)

		for k in mappings.iterkeys():
			attrs.pop(k)

		if not attrs['__table__']:
			attrs['__table__'] = name.lower()

		attrs['__mappings__'] = mappings
		attrs['__primary_key__'] = primary_key
		attrs['__sql__'] = _gen_sql(attrs['__table__'],mappings)

		# for trigger in _triggers:
  #           if not trigger in attrs:
  #               attrs[trigger] = None

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

	@classmethod
	def get(cls,pk):
		d = db.select('select * from %s where %s = ?' %(cls.__table__,cls.__primary_key__.name),pk)
		return cls(**d) if d else None

	@classmethod
	def find_all(cls,*args):
		L = db.select('select * from %s' %cls.__table__)
		return [cls(**d) for d in L]

	@classmethod
	def find_by(cls,where,*args):
		L = db.select('select * from %s where %s' %(cls.__table__,where),*args)
		return [cls(**d) for d in L]



	def insert(self):

		fields = []
		params = []
		args = []

		for k,v in self.__mappings__.iteritems():
			if v.insertable:
				fields.append(v.name)
				params.append('?')
				args.append(getattr(self, k,v.default))

		sql = 'insert into %s (%s) values (%s)' %(self.__table__,','.join(fields),','.join(params))
		return db.insert(sql, *args)

	def update(self):
		
		pk = self.__primary_key__.name

		L = []
		args = []

		for k,v in self.__mappings__.iteritems():
			if v.updateable:
				L.append(' %s = ?' %k)
				args.append(getattr(self,k,v.default))

		args.append(getattr(self,pk))
		sql = 'update %s set %s where %s = ?' %(self.__table__,','.join(L),pk)
		
		return db.update(sql,*args)

 	def delete(self):
 		pk = self.__primary_key__.name
 		args = (getattr(self,pk))

 		sql = 'delete from %s where %s = ?' %(self.__table__,pk)

 		return db.update(sql,args)

 	def select(self,condition):
 		
 		sql = 'select * from %s where %s' %(self.__table__,condition)

 		return db.select(sql)

class User(DatabaseModel):
    
    __table__ = 'user'

    id = IntegerField(name = 'id',primary_key = True)
    username = StringField(name = 'username')
    email = StringField(name = 'email')
    password = StringField(name = 'password')


if __name__ == '__main__':
	
	if not db.engine:
		db.create_databaseengine('root', 'momoyao1993', 'lee', '127.0.0.1')

	u = User(id=5, username='l', email='aaa', password='my-pwd')
	# u.insert()
	print u.select('username = "l" and email = "aaa"')[0]
	