def get_in_bases(attr, bases):
	for base in bases:
		if (hasattr(base, attr)):
			return getattr(base, attr)
	return None