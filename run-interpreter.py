from yorumlayici import parser as yorumlayici
from yorumlayici.sly.lex import LexError
lexer = yorumlayici.HavaLexer()
parser = yorumlayici.HavaParser()
env = {}
while True:
	try:
		text = input('Hava > ')
		tree = parser.parse(lexer.tokenize(text))
		yorumlayici.HavaExecute(tree, env)
	except LexError:
		continue
	except EOFError:
		continue

