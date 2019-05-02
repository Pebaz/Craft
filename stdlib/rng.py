import random

def craft_random():
	return random.random()

__craft__ = {
	'rng' : {
		'byval' : [{ 'random' : craft_random }]
	}
}