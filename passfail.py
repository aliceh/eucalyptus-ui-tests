import base64
import httplib
import json

class SauceRest(object):
    """
    """

    def __init__(self, username, password, host="saucelabs.com", api="/rest/v1"):
        """

        Arguments:
        - `username`:
        - `password`:
        """
        self._username = username
        self._password = password
        self._host = host
        self._api = api
        self._base_url = 'https://%s/%s' % (host, api)

        self.base64string = base64.encodestring('%s:%s' % (username, password))[:-1]

    def report_pass_fail(self,id,data):
        return self.rest(
            url="/%s/jobs/%s" % (self._username, id),
            method='PUT',
            data=data
            )

    def rest(self, url, method='GET', data=None):
        ret= False
        connection =  httplib.HTTPSConnection(self._host)

        if (data != None):
            data = json.dumps(data)

        headers = {"Authorization": "Basic %s" % self.base64string,
                   "Content-type": "application/json"}

        connection.request(method, self._api + url, data, headers)
        res = connection.getresponse()

        if (res.status / 100 == 2):
            try:
                ret = json.loads(res.read())
            except Exception as e:
                ret = (False, e)
        else:
            ret = (False, res.status, res.reason)

        connection.close()

        return ret

#sauce = SauceRest(
#        username="iamfuzz",
#        password="1d29d9b7-8970-4d8f-acce-20c6e0bac8b9",
#        )
