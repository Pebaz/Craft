
print('Wing Programming Language')
print('Version: 0.1.0\n')
print('Press <enter> twice for running single commands.')
print('Type "quit" or press CTCL > C to leave the program.\n')

code = ''
initial = True
while True:
	line = input('>>> ') if initial else input('... ')

	if line.strip() != '':
		code += line + '\n'
		initial = False
	else:
		if code.strip() == '':
			continue

		# Run the code

		# Print the output even if it's None
		for i in code.split('\n'):
			if i.strip() != '':
				print(f' -> {i}')
				

		if code.strip().replace('\n', '') == 'quit':
			break

		initial = True
		code = ''
		
			


