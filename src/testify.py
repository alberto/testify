from nose.plugins import Plugin
import logging
import pynotify
import os

log = logging.getLogger('nose.plugins')


class SimpleNotifier(object):
	BASE_TITLE = 'Testify'
	TIMEOUT = 1000
	dir_path = os.path.dirname(__file__)
	SUCCESS_IMG = os.path.abspath(dir_path + '/../imgs/success.png')
	UNSTABLE_IMG = os.path.abspath(dir_path + '/../imgs/unstable.png')
	FAILURE_IMG = os.path.abspath(dir_path + '/../imgs/failure.png')

	statuses = {
		'success' : [ '"%s"', SUCCESS_IMG, pynotify.URGENCY_LOW],
		'failure' : [ '"Ooops. %s"', FAILURE_IMG, pynotify.URGENCY_CRITICAL]
	}

	def __init__(self):
		pynotify.init('Testify')

	def __notify(self, status, message, big_message):
		status_values = self.statuses[status]
		n = pynotify.Notification(
			self.BASE_TITLE,
			status_values[0] % message + big_message,
			status_values[1])
		n.set_urgency(status_values[2])
		n.set_timeout(self.TIMEOUT)
		n.show()

	def success(self, message):
		self.__notify("success", message, "")

	def fail(self, message, big_message):
		self.__notify("failure", message, big_message)

class Testify(Plugin):
	"""
	Enable libnotify notifications
	"""
	name = 'testify'

	def begin(self):
		self.__notifier = SimpleNotifier()

	def finalize(self, result = None):
		"""
		Clean up any created database and schema.
		"""
		self.__notifier = SimpleNotifier()
		fail_msg = '\n'.join(["Failed: %s" % name for name, ex in result.failures])
		err_msg = '\n'.join(["Error: %s" % name for name, ex in result.errors])

		big_msg = '\n'.join([fail_msg, err_msg])

		if result.wasSuccessful():
			self.__notifier.success("%s tests run ok" % result.testsRun)
		else:
			self.__notifier.fail("%s tests. %s failed. %s errors." % (result.testsRun, len(result.failures), len(result.errors)), big_msg)
