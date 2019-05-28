
bar_top = '┬'
bar_con = '│'
bar_mid = '├'
bar_crs = '┼'
bar_end = '└'


def lister(l, level=0):
	tabs = bar_con * level
	#if level == 1:
	#    tabs = bar_mid + tabs[1:]

	for i in l:
		if isinstance(i, list):
			if len(i) > 0:
				lister(i, level=level+1)

		else:
			# Top
			if l.index(i) == 0:
				tabn = tabs
				if level == 1:
					tabn = bar_mid + tabs[1:]
				elif level > 1:
					tabn = bar_mid + bar_crs * (level - 1)
				
				print(tabn + bar_top, i)

			# Middle
			elif l.index(i) < len(l) - 1:
				print(tabs + bar_mid, i)

			# End
			elif l.index(i) == len(l) - 1:
				print(tabs + bar_end, i)

ll = [
	'One',
	['Two', 'Two Point Five'],
	'Three',
	[1, 2],
	[5, 4, 3, [2, 1, 1]],
	'asdf',
	[
		['Pebaz', 'Age: 23', 'Eyes: Purple'],
		['Yelbu', 'Age: 22', 'Eyes: Pink'],
		['Protodip', 'Age: 26', 'Eyes: Blue']
	],
	'Mowr',
	1, 2, 3, 4, 5, 6, 7
]


lister(ll)