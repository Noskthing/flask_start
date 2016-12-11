import threading
import functools

#Tools Class
class Dict(dict):
   
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

# about DatabaseEngine
class _DatabaseEngine(object):

	def __init__(self, connect):
		self.connect = connect

	def connect(self):
		return self.connect()

class DBError(Exception):
    pass
    
engine = None

def create_databaseengine(user = 'root',password = 'lee',database = 'lee',host = '127.0.0.1',port = '3306',**kw):

	import mysql.connector

	global engine    
	if engine:
		raise DBError('_DatabaseEngine is already initialized !')

	params = dict(user = user,password = password,database = database,host = host,port = port)
	defaults = dict(use_unicode=True, charset='utf8', collation='utf8_general_ci', autocommit=False)
	for k,v in defaults.iteritems():
		params[k] = kw.pop(k,v)
	params.update(kw)
	params['buffered'] = True

	engine = _DatabaseEngine(lambda: mysql.connector.connect(**params))

	print 'Init mysql engine <%s> success !' %hex(id(engine))

# about Database connection
class _LasyConnection(object):
	
	def __init__(self):
		self.connection = None

	def cursor(self):
		if not self.connection:
			_connection = engine.connect()
			self.connection = _connection
		return self.connection.cursor()

	def commit(self):
		self.connection.commit()

	def rollback(self):
		self.connection.rollback()

	def cleanup(self):
		if self.connection:
			_connection = self.connection
			self.connection = None
			_connection.close()
		

class _DatabaseContext(threading.local):

	def __init__(self):
		self.connection = None
		self.transactions = 0

	def is_already(self):
		return not self.connection is None

	def init(self):
		self.connection = _LasyConnection()
		self.transactions = 0

	def  cleanup(self):
		self.connection.cleanup()
		self.connection = None

	def cursor(self):
		return self.connection.cursor()

_db_ctx = _DatabaseContext()

class _ConnectionContext(object):

	def __enter__(self):
		global _db_ctx
		self.should_cleanup = False
		if not _db_ctx.is_already():
			_db_ctx.init()
			self.should_cleanup = True
		return self

	def __exit__(self, exctype, excvalue, traceback):
		global _db_ctx
		if self.should_cleanup:
			_db_ctx.cleanup()



def with_connection(func):
   
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with _ConnectionContext():
            return func(*args, **kw)
    return _wrapper


# about Transaction
class _TransactionCtx(object):
    def __enter__(self):
        global _db_ctx
        self.should_close_conn = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_close_conn = True
        _db_ctx.transactions = _db_ctx.transactions + 1
        return self

    def __exit__(self, exctype, excvalue, traceback):
        global _db_ctx
        _db_ctx.transactions = _db_ctx.transactions - 1
        try:
            if _db_ctx.transactions==0:
                if exctype is None:
                    self.commit()
                else:
                    self.rollback()
        finally:
            if self.should_close_conn:
                _db_ctx.cleanup()

    def commit(self):
        global _db_ctx
        try:
            _db_ctx.connection.commit()
        except:
            _db_ctx.connection.rollback()
            raise

    def rollback(self):
        global _db_ctx
        _db_ctx.connection.rollback()
		

def with_transaction(func):
	
	@functools.wraps(func)
	def _wrapper(*args,**kw):
		with _TransactionCtx():
			func(*args,**kw)
	return _wrapper



# about sql method

#insert method 
@with_connection
def insert(sql,*args):
	return _update(sql, *args)

#update methods
@with_connection
def _update(sql,*args):
	
	global _db_ctx

	cursor = None

	sql = sql.replace('?', '%s')

	try:
		cursor = _db_ctx.connection.cursor()
		cursor.execute(sql,args)
		row = cursor.rowcount
		if _db_ctx.transactions == 0:
			_db_ctx.connection.commit()
		return row
	finally:
		if cursor:
			cursor.close()

def update(sql,*args):
	return _update(sql,*args)

# select method
@with_connection
def _select(sql, first, *args):
 
    global _db_ctx

    cursor = None

    sql = sql.replace('?', '%s')
    
    try:
        cursor = _db_ctx.connection.cursor()
        cursor.execute(sql, args)
        if cursor.description:
            names = [x[0] for x in cursor.description]
        if first:
            values = cursor.fetchone()
            if not values:
                return None
            return Dict(names, values)
        return [Dict(names, x) for x in cursor.fetchall()]
    finally:
        if cursor:
            cursor.close()

def select(sql, *args):
	return _select(sql,False,*args)

def select_one(self,*args):
	return _select(sql,True,*args)