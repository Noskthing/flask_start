from field import *
from engine import *

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
		spl.append()

class DatabaseModelMetaclass(type):
	"""docstring for ModelMetaclass"""
	def __new__(cls,name,bases,attrs):
		if name == 'DatabaseModel':
			return type.__new__(cls,name,bases,attrs)

		mappings = dict()
		primary_key = None

		for k,v in attrs.iteritems():
			print('Found mapping: %s==>%s' % (k, v))
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
				primary_key = v.primary_key

			mappings[k] = v

		if not primary_key:
			raise TypeError('primary_key not define in class %s',name)

		for k in mappings.iterkeys():
			attrs.pop(k)

		if not attrs['__table__']:
			attrs['__table__'] = name.lower()

		attrs['__mappings__'] = mappings
		attrs['__primary_key__'] = primary_key
		attrs['__sql__'] = lambda self : _gen_sql(attrs['__table__'],mappings)

		for trigger in _triggers:
            if not trigger in attrs:
                attrs[trigger] = None

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