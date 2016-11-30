class sss(object):

	def __getattr__(self,key):
		return 'aa'


aaa = sss()
print(aaa.lee)