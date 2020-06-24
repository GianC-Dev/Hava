"""
	Author: GianC-Dev <gianegekck@gmail.com>
					  _    _
					 | |  | |
					 | |__| | __ ___   ____ _
					 |  __  |/ _` \ \ / / _` |
					 | |  | | (_| |\ V / (_| |
					 |_|  |_|\__,_| \_/ \__,_|
      
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.
"""

from .sly import Parser
from .sly import Lexer


class HavaLexer(Lexer):
	tokens = {IN, PRINT, NAME, NUMBER, STRING, IF, ELSE, FOR, FUN, EQEQ, EQ, START_PREFIX, FINISH_PREFIX, PLUSEQ,
	          MINUSEQ}
	ignore = '\t '
	
	"""
	Değer verilmeyen işaretler
	
	:type HashMap
	:return None
	"""
	literals = {'+', '-', '/', '*', '(', ')', ',', ';'}
	
	IF = r'eğer'
	START_PREFIX = r'::'
	FINISH_PREFIX = r':'
	ELSE = r'değilse'
	FOR = r'döngü'
	FUN = r'fonksiyon'
	IN = r'icinde'
	PRINT = r'yaz'
	PLUSEQ = r'\+='
	MINUSEQ = r'-='
	EQEQ = r'=='
	EQ = r'='
	NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
	STRING = r'\".*?"'
	
	"""
	Number Tokenini Tanımlıyoruz
	%d ASCII alfabesinde rakama denk geldiği için %d kullanıyoruz.
	
	:return int
	"""
	
	@_(r'\d+')
	def NUMBER(self, t):
		t.value = int(t.value)
		return t
	
	"""
	Komut satırını algılayıp, geçmesini sağlıyor.
	
	:return None
	"""
	
	@_(r'#.*')
	def COMMENT(self, t):
		pass
	
	@_(r'##.*##')
	def COMMENT(self, t):
		pass
	
	
	"""
	Hata verildiği zaman yapılacak methodlar
	
	:return None
	"""


class HavaParser(Parser):
	"""
	Tokenler lexer kodundan alınarak burada da kullanılıyor.
	
	:return HashMap
	"""
	
	tokens = HavaLexer.tokens
	
	precedence = (
		('left', '+', '-'),
		('left', '*', '/'),
		('right', 'UMINUS'),
	)
	
	"""
	Enviroment başka yerler de kullanılmaya ayarlanıyor.
	
	:return None
	"""
	
	def __init__(self):
		self.env = {}
	
	"""
	Yeni ext ayarlanıyor (İsmi: statement)
	
	:return None
	"""
	
	@_('')
	def statement(self, p):
		pass
	
	"""
	Döngü Syntaxı Ayarlanıyor.
	
	Syntax: döngü 'değişken' içinde 'sayı' sonra 'fonksiyon' :
	
	:return str
	"""
	
	@_('FOR NAME IN expr START_PREFIX statement FINISH_PREFIX')
	def statement(self, p):
		return 'for_loop', ('for_loop_setup', p.NAME, p.expr), p.statement
	
	"""
	Koşul - Aksi Halde Fonksiyonu ayarlanıyor.

	Syntax: eğer 'koşul' :: 'fonksiyon' değilse 'fonksiyon' :

	:return None
	"""
	
	@_('IF condition START_PREFIX statement ELSE START_PREFIX statement FINISH_PREFIX')
	def statement(self, p):
		return 'if_stmt_else', p.condition, ('branch', p.statement0, p.statement1)
	
	"""
	Koşul Fonksiyonu ayarlanıyor.
	
	Syntax: eğer 'koşul' :: 'fonksiyon' :
	
	:return None
	"""
	
	@_('IF condition START_PREFIX statement FINISH_PREFIX')
	def statement(self, p):
		return 'if_stmt', p.condition, ('branch', p.statement)
	
	"""
	Fonksiyon oluşturma methodu
	
	Syntax: fonksiyon 'fonksiyon_ismi'() :: 'fonksiyon' :
	
	:return None
	"""
	
	@_('FUN NAME "(" ")" START_PREFIX statement FINISH_PREFIX')
	def statement(self, p):
		return 'fun_def', p.NAME, p.statement
	
	"""
	Yazdırma fonksiyonu
	
	Syntax: yaz('yazı'):
	
	:return None
	
	"""
	
	@_('PRINT "(" STRING ")" FINISH_PREFIX')
	def expr(self, p):
		return 'print', p.STRING
	
	"""
	Fonksiyon çağırma methodu
	
	Syntax: 'fonksiyon_ismi'():
	
	"""
	
	@_('NAME "(" ")" FINISH_PREFIX')
	def statement(self, p):
		return 'fun_call', p.NAME
	
	"""
	Bir tür koşul.

	Syntax: 'değişken' == 'yazı':

	:returns True, False

	"""
	
	@_('NAME EQEQ STRING FINISH_PREFIX')
	def condition(self, p):
		return 'condition_eqeq_var_str', p.NAME, p.STRING
	
	"""
	Bir tür koşul.
	
	Syntax: 'sayı' == 'sayı':
	
	:returns True, False
	
	"""
	
	@_('expr EQEQ expr FINISH_PREFIX')
	def condition(self, p):
		return 'condition_eqeq', p.expr0, p.expr1
	
	"""
	Bir tür koşul.
	
	Syntax: 'değişken' == 'sayı':
	
	:returns True, False
	
	"""
	
	@_('NAME EQEQ expr FINISH_PREFIX')
	def condition(self, p):
		return 'condition_eqeq_var_int', p.NAME, p.expr
	
	"""
	Bir tür koşul.
	
	Syntax: 'yazı' == 'sayı':
	
	:returns True, False
	
	"""
	
	@_('STRING EQEQ expr FINISH_PREFIX')
	def condition(self, p):
		return 'condition_eqeq', p.STRING, p.expr
	
	"""
	Bir tür koşul.
	
	Syntax: 'yazı' == 'yazı':
	
	:returns True, False
	
	"""
	
	@_('STRING EQEQ STRING FINISH_PREFIX')
	def condition(self, p):
		return 'condition_eqeq', p.STRING0, p.STRING1
	
	"""
	Yeni bir ext ayarlanıyor. (İsmi: var_assign)
	
	:return None
	"""
	
	@_('var_assign')
	def statement(self, p):
		return p.var_assign
	
	"""
	Yeni bir değişken ayarlamaya yarayan method. (Sayı için)
	
	Syntax: 'değişken ismi' = 'sayı':
	"""
	
	@_('NAME EQ expr FINISH_PREFIX')
	def var_assign(self, p):
		return 'var_assign', p.NAME, p.expr
	
	"""
	Yeni bir değişken ayarlamaya yarayan method. (String için)

	Syntax: 'değişken ismi' = '"yazi"':
	"""
	
	@_('NAME EQ STRING FINISH_PREFIX')
	def var_assign(self, p):
		return 'var_assign', p.NAME, p.STRING
	
	"""
	Yeni bir ext ayarlanıyor. (İsmi: expr)

	:return None
	"""
	
	@_('expr')
	def statement(self, p):
		return p.expr
	
	"""
	Sayıları toplamaya yarayan method.
	
	Syntax: 'sayı' + 'sayı':
	
	:return int
	"""
	
	@_('expr "+" expr FINISH_PREFIX')
	def expr(self, p):
		return 'add', p.expr0, p.expr1
	
	"""
	Sayıları çıkarmaya yarayan method.

	Syntax: 'sayı' - 'sayı':

	:return int
	"""
	
	@_('expr "-" expr FINISH_PREFIX')
	def expr(self, p):
		return 'sub', p.expr0, p.expr1
	
	"""
	Sayıları çarpmaya yarayan method.

	Syntax: 'sayı' * 'sayı':

	:return int
	"""
	
	@_('expr "*" expr FINISH_PREFIX')
	def expr(self, p):
		return 'mul', p.expr0, p.expr1
	
	"""
	Sayıları bölmeye yarayan method.

	Syntax: 'sayı' / 'sayı':

	:return int
	"""
	
	@_('expr "/" expr FINISH_PREFIX')
	def expr(self, p):
		return 'div', p.expr0, p.expr1
	
	"""
	Sayıları arttırmaya yarayan method.

	Syntax: 'değişken' += 'sayı':

	:return int
	"""
	
	@_('NAME PLUSEQ expr FINISH_PREFIX')
	def expr(self, p):
		return 'plus_eq', p.NAME, p.expr
	
	"""
	Yazıları arttırmaya yarayan method.

	Syntax: 'değişken' += 'yazı':

	:return int
	"""
	
	@_('NAME PLUSEQ STRING FINISH_PREFIX')
	def expr(self, p):
		return 'plus_eq', p.NAME, p.STRING
	
	"""
	Sayıları azaltmaya yarayan method.

	Syntax: 'değişken' -= 'sayı':

	:return int
	"""
	
	@_('NAME MINUSEQ expr FINISH_PREFIX')
	def expr(self, p):
		return 'minus_eq', p.NAME, p.expr
	
	"""
	UMINUS ayarlayan method.

	:return None
	"""
	
	@_('"-" expr %prec UMINUS')
	def expr(self, p):
		return p.expr
	
	"""
	NAME ayarlayan method.

	:return None
	"""
	
	@_('NAME')
	def expr(self, p):
		return 'var', p.NAME
	
	"""
	NUMBER ayarlayan method.

	:return None
	"""
	
	@_('NUMBER')
	def expr(self, p):
		return 'num', p.NUMBER


class HavaExecute:
	
	def __init__(self, tree, env):
		self.env = env
		result = self.walkTree(tree)
		if result is not None and isinstance(result, int):
			print(result)
		if isinstance(result, str) and result[0] == '"':
			print(result.replace("\"", ""))
	
	def walkTree(self, node):
		
		if isinstance(node, int):
			return node
		if isinstance(node, str):
			return node
		
		if node is None:
			return None
		
		"""
		Yazı yazdırmayı tamamlamaya yarayan method.
		
		:return str
		"""
		if node[0] == 'print':
			return self.walkTree(node[1])
		
		if node[0] == 'program':
			if node[1] is None:
				self.walkTree(node[2])
			else:
				self.walkTree(node[1])
				self.walkTree(node[2])
		
		"""
		Sayı döndüren method.

		:return int
		"""
		if node[0] == 'num':
			return node[1]
		
		"""
		Yazı döndüren method

		:return str
		"""
		if node[0] == 'str':
			return node[1]
		
		"""
		Koşul - Aksi halde işlemini tamamlayan method

		:returns True, False
		"""
		if node[0] == 'if_stmt':
			result = self.walkTree(node[1])
			if result:
				return self.walkTree(node[2][1])
			return None
		
		if node[0] == 'if_stmt_else':
			result = self.walkTree(node[1])
			if result:
				return self.walkTree(node[2][1])
			return self.walkTree(node[2][2])
		
		"""
		Sayıların eşit olup olmadıklarını kontrol eden method

		:returns True, False
		"""
		if node[0] == 'condition_eqeq':
			try:
				return self.walkTree(node[1]) == self.walkTree(node[2])
			except KeyError:
				return False
		
		if node[0] == 'condition_eqeq_var_str':
			try:
				return self.walkTree(self.env[node[1]]) == self.walkTree(node[2])
			except Exception:
				return False
		
		if node[0] == 'condition_eqeq_var_int':
			try:
				return self.walkTree(self.env[node[1]]) == self.walkTree(node[2])
			except Exception:
				return False
		
		"""
		Fonksiyon oluşturan method

		:return None
		"""
		if node[0] == 'fun_def':
			self.env[node[1]] = node[2]
		
		"""
		Fonksiyon çağıran method

		:return None
		"""
		if node[0] == 'fun_call':
			try:
				return self.walkTree(self.env[node[1]])
			except LookupError:
				print("Bilinmeyen Fonksiyon: %s" % node[1])
				return None
		
		"""
		Sayı toplayan-çıkaran-bölen-çarpan method.

		:return int
		"""
		if node[0] == 'add':
			return self.walkTree(node[1]) + self.walkTree(node[2])
		elif node[0] == 'sub':
			return self.walkTree(node[1]) - self.walkTree(node[2])
		elif node[0] == 'mul':
			return self.walkTree(node[1]) * self.walkTree(node[2])
		elif node[0] == 'div':
			return self.walkTree(node[1]) / self.walkTree(node[2])
		
		"""
		Değişken oluşturan method

		:return None
		"""
		if node[0] == 'var_assign':
			self.env[node[1]] = self.walkTree(node[2])
			return node[1]
		
		"""
		Sayıyı yükselten method

		:return int
		"""
		if node[0] == 'plus_eq':
			self.env[node[1]] += self.walkTree(node[2])
			return None
		
		"""
		Sayıyı azaltan method

		:return int
		"""
		if node[0] == 'minus_eq':
			self.env[node[1]] -= self.walkTree(node[2])
			return 0
		
		"""
		Değişken döndüren method

		:return None
		"""
		if node[0] == 'var':
			try:
				return self.env[node[1]]
			except LookupError:
				print("Bilinmeyen Değişken: " + node[1])
				return None
		
		"""
		Döngüyü tamamlayan method

		:return None
		"""
		if node[0] == 'for_loop':
			if node[1][0] == 'for_loop_setup':
				loop_setup = self.walkTree(node[1])
				
				loop_count = self.env[loop_setup[0]]
				loop_limit = loop_setup[1]
				
				for i in range(loop_count + 1, loop_limit + 1):
					res = self.walkTree(node[2])
					if res is not None:
						print(res)
					self.env[loop_setup[0]] = i
				del self.env[loop_setup[0]]
		
		"""
		Döngüyü tamamlayan method (ekstra)

		:return None
		"""
		if node[0] == 'for_loop_setup':
			return self.walkTree(node[1]), self.walkTree(node[2])


if __name__ == '__main__':
	lexer = HavaLexer()
	parser = HavaParser()
	env = {}
	while True:
		try:
			text = input('Hava > ')
		except Exception:
			continue
		if text:
			tree = parser.parse(lexer.tokenize(text))
			HavaExecute(tree, env)
