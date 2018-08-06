

code = ''
initial = True
while True:
	line = input('>>> ') if initial else input('... ')
	if line.strip() != '':
		code += line + '\n'
		initial = False
	elif line.strip() == 'quit' or line.strip() == 'exit':
		break
	else:
		print(code)
		code = ''
		initial = True
