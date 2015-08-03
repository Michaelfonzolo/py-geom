
_modules = { }

def require(module_name):
	return _modules.get(module_name)


def _try_import(name):
	try:
		module = __import__(name)
		_modules[name] = module
	except ImportError:
		pass

_try_import("numpy")
_try_import("scipy")
