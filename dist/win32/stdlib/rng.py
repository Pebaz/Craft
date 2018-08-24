import random

def wing_random():
	return random.random()

__wing__ = {
	'rng' : {
		'byval' : [{ 'random' : wing_random }]
	}
}