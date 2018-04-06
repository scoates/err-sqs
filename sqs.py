from errbot import BotPlugin, botcmd
import boto3


sqs = boto3.resource('sqs')

class Sqs(BotPlugin):
    """
    Listens to SQS, relays to chat.
    """

    queue = None

    def _get_queue(self):
        if self.config is not None:
            self.log.debug('Getting SQS queue.')
            if self.config['SQS_QUEUE'] is not None:
                self.queue = sqs.get_queue_by_name(QueueName=self.config['SQS_QUEUE'])

    def _sqs_callback(self):
        self.log.debug('Checking SQS queue.')
        if self.queue is None:
            self._get_queue()
        if self.queue is None:
            return
        for message in self.queue.receive_messages(
                WaitTimeSeconds=0,
                MessageAttributeNames=['channel'],
                MaxNumberOfMessages=10):
            self.log.debug("GOT MESSAGE:")

            if message.message_attributes is not None:
                channel = message.message_attributes.get('channel').get('StringValue')
            else:
                channel = None

            if channel:
                self.log.debug("Message for: {}".format(channel))
                self.log.debug("Message: {}".format(message.body))

                self.send(
                    self.build_identifier(channel),
                    message.body)

            else:
                self.log.debug("No channel; discarding.")

            message.delete()


    def activate(self):
        """
        Triggers on plugin activation

        You should delete it if you're not using it to override any default behaviour
        """
        super(Sqs, self).activate()
        self._get_queue()
        self.start_poller(10, self._sqs_callback)

    def get_configuration_template(self):
        """
        Defines the configuration structure this plugin supports
        """
        return {'SQS_QUEUE': "errbot.fifo"}

    def check_configuration(self, configuration):
        """
        Triggers when the configuration is checked, shortly before activation
        """
        super(Sqs, self).check_configuration(configuration)
        self.log.debug("SQS: checking configuration SQS_QUEUE")
        if 'SQS_QUEUE' not in configuration:
            raise errbot.ValidationException('No SQS_QUEUE configured.')

    # def callback_connect(self):
    #     """
    #     Triggers when bot is connected

    #     You should delete it if you're not using it to override any default behaviour
    #     """
    #     pass

    # def callback_message(self, message):
    #     """
    #     Triggered for every received message that isn't coming from the bot itself

    #     You should delete it if you're not using it to override any default behaviour
    #     """
    #     pass

    # def callback_botmessage(self, message):
    #     """
    #     Triggered for every message that comes from the bot itself

    #     You should delete it if you're not using it to override any default behaviour
    #     """
    #     pass

