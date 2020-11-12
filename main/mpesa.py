from django.conf import settings

from portalsdk import APIContext, APIMethodType, APIRequest

BASE_URL = settings.MPESA['BASE_URL']
get_session_url = settings.MPESA['get_session_url']
c2bPayment_url = settings.MPESA['c2bPayment_url']
reversal_url = settings.MPESA['reversal_url']
b2cPayment_url = settings.MPESA['b2cPayment_url']
b2bPayment_url = settings.MPESA['b2bPayment_url']
transaction_status_url = settings.MPESA['transaction_status_url']


class MPESA:

    def __init__(self, api_key, public_key, ssl=True):
        """
        Generate context with API to request a Session ID.
        """
        self.context = APIContext(
            api_key, public_key, ssl=ssl, address=BASE_URL, port=443)
        self.context.add_header('Origin', '*')

    def get_encrypted_api_key(self):
        """
        Return encrypted API key.
        """
        return APIRequest(self.context).create_bearer_token()

    def get_session_id(self, path=get_session_url):
        """
        Return a valid Session ID needed to transact on M-Pesa using
        OpenAPI.
        """
        self.context.update({'path': path})

        result = None

        try:
            result = APIRequest(self.context).execute()
        except Exception as e:
            print('Call Failed: ', e)

        if result is None:
            raise Exception(
                'SessionKey call failed to get result. Please check.')
        else:
            return result.body['output_SessionID']

    def _get_api_results(self, context):
        """
        Return results from API call.
        """
        results = None
        try:
            results = APIRequest(context).execute()
        except Exception as e:
            print('Call Failed: ', e)

        if results is None:
            raise Exception('API call failed to get result. Please check.')
        else:
            return results

    def c2b(self, parameters: dict, path=c2bPayment_url):
        """
        A standard customer-to-business transaction

        parameters = {
            'input_Amount': 10,
            'input_Country': 'TZN',
            'input_Currency': 'TZS',
            'input_CustomerMSISDN': '000000000001',
            'input_ServiceProviderCode': '000000',
            'input_ThirdPartyConversationID':
                'asv02e5958774f7ba228d83d0d689761',
            'input_TransactionReference': 'T1234C',
            'input_PurchasedItemsDesc': 'Shoes',
        }
        """

        self.context.update({
            'api_key': self.get_session_id(),
            'method_type': APIMethodType.POST,
            'path': path,
            'parameters': {k: v for k, v in parameters.items()}
        })

        results = self._get_api_results(self.context)
        return results

    def reversal(self, path, reversal_parameters: dict):
        """
        Reverse a successful transaction.

        reversal_parameters = {
            'input_ReversalAmount': '25',
            'input_Country': 'TZN',
            'input_ServiceProviderCode': '000000',
            'input_ThirdPartyConversationID':
                'asv02e5958774f7ba228d83d0d689761',
            'input_TransactionID': '0000000000001',
        }
        """
        self.context.update({
            'api_key': self.get_session_id(),
            'method_type': APIMethodType.PUT,
            'path': path,
            'parameters': {k: v for k, v in reversal_parameters.items()}
        })

        results = self._get_api_results(self.context)
        return results

    def b2c(self, parameters: dict, path=b2cPayment_url):
        """
        A standard customer-to-business transaction.

        parameters = {
            'input_Amount': '10',
            'input_Country': 'TZN',
            'input_Currency': 'TZS',
            'input_CustomerMSISDN': '000000000001',
            'input_ServiceProviderCode': '000000',
            'input_ThirdPartyConversationID':
            'asv02e5958774f7ba228d83d0d689761',
            'input_TransactionReference': 'T1234C',
            'input_PaymentItemsDesc': 'Salary payment',
        }
        """
        self.context.update({
            'api_key': self.get_session_id(),
            'method_type': APIMethodType.POST,
            'path': path,
            'parameters': {k: v for k, v in parameters.items()}
        })

        results = self._get_api_results(self.context)
        return results

    def b2b(self, parameters: dict, path=b2bPayment_url):
        """
        Business-to-business transactions (Single Stage).

        parameters = {
            'input_Amount': '10',
            'input_Country': 'TZN',
            'input_Currency': 'TZS',
            'input_CustomerMSISDN': '000000000001',
            'input_ServiceProviderCode': '000000',
            'input_ThirdPartyConversationID':'asv02e5958774f7ba228d83d0d689761',
            'input_TransactionReference': 'T1234C',
            'input_PaymentItemsDesc': 'Salary payment',
            }
        """
        self.context.update({
            'api_key': self.get_session_id(),
            'method_type': APIMethodType.POST,
            'path': path,
            'parameters': {k: v for k, v in parameters.items()}
        })

        results = None
        try:
            results = APIRequest(self.context).execute()
        except Exception as e:
            print('Call Failed: ', e)

        if results is None:
            raise Exception('API call failed to get result. Please check.')
        else:
            return results

    def query_transaction_status(self, parameters: dict,
                                 path=transaction_status_url):
        """
        Query the status of the transaction that has been initiated.

        parameters = {
            'input_QueryReference': '000000000000000000001',
            'input_ServiceProviderCode': '000000',
            'input_ThirdPartyConversationID':'asv02e5958774f7ba228d83d0d689761',
            'input_Country': 'TZN',
        }
        """
        self.context.update({
            'api_key': self.get_session_id(),
            'method_type': APIMethodType.GET,
            'path': path,
            'parameters': {k: v for k, v in parameters.items()}
        })

        results = self._get_api_results(self.context)
        return results
