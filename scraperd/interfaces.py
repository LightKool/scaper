from zope.interface import Interface


class IPoller(Interface):
	"""A component that polls for crawl jobs that need to run"""

	def poll():
		"""Called periodically to poll for crawl jobs"""

	def next():
		"""Return the next message.

		It should return a Deferred which will get fired when there is a new
		project that needs to run, or already fired if there was a project
		waiting to run already.

		The message is a dict containing (at least):
		* the name of the spider to be run in the '_spider' key
		* a unique identifier for this run in the `_job` key
		This message will be passed later to IEnvironment.get_environment().
		"""


class ISpiderQueue(Interface):

	def add(name, **spider_args):
		"""Add a spider to the queue given its name a some spider arguments.

		This method can return a deferred. """

	def pop():
		"""Pop the next mesasge from the queue. The messages is a dict
		conaining a key 'name' with the spider name and other keys as spider
		attributes.

		This method can return a deferred. """

	def count():
		"""Return the number of spiders in the queue.

		This method can return a deferred. """


class IEnvironment(Interface):
	"""A component to generate the environment of crawler processes"""

	def get_environment(message, slot):
		"""Return the environment variables to use for running the process.

		`message` is the message received from the IPoller.next() method
		`slot` is the Launcher slot where the process will be running.
		"""
