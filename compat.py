from functools import wraps

_modules = { }

class RequirementException(Exception):
	pass

def require(module_name):
	if (module_name in _modules):
		return _modules[module_name]
	raise ImportError("This library requires '%s'." % module_name)

def requires(module_name):
	def decorator(func):
		@wraps(func)
		def _wrapped(*args, **kwargs):
			if (not _modules.contains(module_name)):
				raise RequirementException(
					"Function/method '%s' requires module '%s'." % (func.__name__, module_name)
					)
			return func(*args, **kwargs)
		return _wrapped
	return decorator


def try_import(module_name):
	return _modules.get(module_name)


def _try_import(name):
	try:
		module = __import__(name)
		_modules[name] = module
	except ImportError:
		pass

_try_import("numpy")
_try_import("scipy")
