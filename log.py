
# On va se servir de l'utilitaire Logger de kivy, qui a pas l'air si mal!
from kivy.logger import Logger

def info(title, text):
	Logger.info(title + ' : ' + text)

def warn(title, text):
	Logger.warning(title + ' : ' + text)

def err(title, text):
	Logger.error(title + ' : ' + text)

def crit(title, text):
	Logger.critical(title + ' : ' + text)

def ex(title, text):
	Logger.exception(text)
