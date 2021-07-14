import africastalking
class AT:
    def __init__(self, config):
        self.config = config
        self.sms = None
        self.intialize_at()
        

    def intialize_at(self):
        africastalking.initialize(self.config.get('AFRICASTALKING_USERNAME'), self.config.get('AFRICASTALKING_API'))
        self.sms = africastalking.SMS

    def send_message(self, message, receipients):
            try:
                response = self.sms.send(message, receipients)
                fail = []
                success = []
            
                for recipient in response['SMSMessageData']['Recipients']:
                    if recipient['statusCode'] == 101:
                        success.append(recipient)
                    else:
                        fail.append(recipient)
                        
                if len(success) > 0:
                    data = {
                        'status': 'success',
                        'sent': success,
                        'failed': fail
                    }
                    return data
                else:
                    data = {
                        'status': 'fail',
                        'failed': fail
                    }
                    return data

            except Exception as e:
                data = {
                    'status': 'crash',
                    'message': e
                }
                return data
