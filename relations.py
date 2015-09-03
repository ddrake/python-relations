from collections import defaultdict

class Relation(defaultdict):
	"""A class representing a relation on a set"""
	"""Initializer takes a set and an optional string 'all' or 'identity'"""
	"""Alternatively it can be constructed from a list of pairs"""
	def __init__(self, s, func=None):
		super(Relation, self).__init__(set)
		self.s = s
		if func: 
			f = getattr(self, "_" + func)
			f()

	def _identity(self):
		for x in self.s:
			self[x].add(x)

	def _all(self):
		for x in self.s:
			self[x] = self.s

	@staticmethod
	def fromPairs(pairs):
		s = set()
		for p in pairs:
			for x in p:
				s.add(x)
		rel = Relation(s)
		for x, y in pairs:
			rel.add(x, y)
		return rel

	def toPairs(self):
		return [(x, y) for x, ys in self.items() for y in ys]

	def add(self, k, v):
		self[k].add(v)

	def remove(self, k, v):
		self[k].remove(v)

	def inverse(self):
		inv = Relation(self.s)
		for k, v in self.items():
			for x in v:
				inv[x].add(k)
		return inv

	def intersect(self, other):
		isect = Relation(self.s)
		s = set(self.keys()).intersection(set(other.keys()))
		for k in s:
			isect[k] = self[k].intersection(other[k])
		return isect

	def subset(self, other):
		if not set(self.keys()).issubset(set(other.keys())): return False
		for k,v in self.items():
			if not v.issubset(other[k]): return False
		return True

	def contains(self, k, v):
		return k in self and v in self[k]

	def compose(self, other):
		comp = Relation(self.s)
		for k, v in other.items():
			for x in v:
				for y in self[x]:
					comp[k].add(y)
		return comp

	def reflexive(self):
		i = Relation(self.s, "identity")
		return i.subset(self)

	def symmetric(self):
		inv = self.inverse()
		return self.subset(inv)

	def transitive(self):
		return self.compose(self).subset(self)

	def antisymmetric(self):
		i = Relation(self.s, "identity")
		return self.intersect(self.inverse()).subset(i)


def powerset(s):
	if len(s) == 0: return [[]]
	x = s[0]
	ss = s[1:]
	ps = powerset(ss)
	ps2 = [y + [x] for y in ps]
	return ps + ps2

""" example usage:
s = ['a','b','c']
r = Relation(s,"all")
prs = r.toPairs()
powerprs = powerset(prs)
contents = ["%r\n" % (rel) for rel in powerprs]
open("rels.txt", "w").writelines(contents)
powerrels = [Relation.fromPairs(rel) for rel in powerprs]
contents = ["%r, %r, %r, %r\n" % (rel.reflexive(), rel.symmetric(), rel.transitive(), rel.antisymmetric()) for rel in powerrels]
open("flags.txt", "w").writelines(contents)
"""
