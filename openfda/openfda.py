import requests

class OpenFDA():
    def search_drug(self, name):
        fda = OpenFDAClient()
        msg = self.__class__.__name__ + " searchining for drug " + name
        print(msg)
        return fda.search("drug", name)

    def list_drugs(self):
        print(self.__class__.__name__," listing drugs")

    def search_company(self, name):
        fda = OpenFDAClient()
        print(self.__class__.__name__," searchining for drug ", name)
        return fda.search("company", name)

    def list_companies(self):
        print(self.__class__.__name__," listing companies")

class OpenFDAClient():
    #  HOWTO use the API: https://open.fda.gov/api/
    ITEMS_PER_PAGE = 100 # Max items per page in OpenFDA API
    OPENFDA_API_URL = "https://api.fda.gov/drug/event.json"

    SEARCH_KINDS = ['company', 'drug']

    def __call(self, params=None):
        req = requests.get(self.OPENFDA_API_URL, params=params)
        return req.json()

    def search(self, kind, value):

        found = {}

        if kind not in self.SEARCH_KINDS:
            print ("Search not supported %s", kind)
            return found

        print ("Searching for %s %s in OpenFDA", kind, value)

        if kind == 'company':
            # search=patient.drug.openfda.manufacturer_name:"Gilead Sciences, Inc"
            # remove in general the , which makes the query fails
            value = value.split(",")[0]
            search = 'search=patient.drug.openfda.manufacturer_name:"%s"' % value
        elif kind == 'drug':
            # search=patient.drug.openfda.generic_name:"AMBRISENTAN"
            search = 'search=patient.drug.openfda.generic_name:"%s"' % value

        # Always work with just the first 100 items
        params = "limit=%i" % (self.ITEMS_PER_PAGE)
        params += "&" + search
        found = self.__call(params)

        return found
