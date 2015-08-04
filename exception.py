def index_out_of_range(cls):
	return IndexError("%s index out of range" % cls.__name__)