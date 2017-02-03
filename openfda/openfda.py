import datetime

import dateutil.relativedelta
import requests

class OpenFDAParser():
    def get_companies(self, events_json):
        companies = []
        for event in events_json:
            for drug in event['patient']['drug']:
                companies += drug['openfda']['manufacturer_name']
        # companies = ['c1', 'c2', 'c3']
        return companies

    def get_drugs(self, events_json):
        drugs = []
        for event in events_json:
            for drug in event['patient']['drug']:
                print(drug.keys())
                drugs.append(drug['medicinal_product'])
        # drugs = ['d1', 'd2', 'd3']
        return drugs

class OpenFDA():
    def __init__(self):
        self.fda = OpenFDAClient()
        self.fda_parser = OpenFDAParser()

    def search_drug(self, name):
        msg = self.__class__.__name__ + " searchining for drug " + name
        print(msg)
        return self.fda.search("drug", name)

    def list_drugs(self):
        print(self.__class__.__name__," listing drugs")
        fda = OpenFDAClient()
        events_list = fda.list()
        # Extract the drugs
        return self.fda_parser.get_drugs(events_list)

    def search_company(self, name):
        print(self.__class__.__name__," searchining for drug ", name)
        return self.fda.search("company", name)

    def list_companies(self):
        print(self.__class__.__name__," listing companies")
        events_list = self.fda.list()
        # Extract the companies
        return self.fda_parser.get_companies(events_list)

class OpenFDAClient():
    #  HOWTO use the API: https://open.fda.gov/api/
    # ITEMS_PER_PAGE = 100 # Max items per page in OpenFDA API
    ITEMS_PER_PAGE = 5 # Max items per page in OpenFDA API
    OPENFDA_API_URL = "https://api.fda.gov/drug/event.json"

    SEARCH_KINDS = ['company', 'drug']

    def __call(self, params=None):
        print ("OpenFDA query: %s %s" % (self.OPENFDA_API_URL, params))

        res_json = {}

        try:
            req = requests.get(self.OPENFDA_API_URL, params=params)
            res_json = req.json()
        except requests.exceptions.ConnectionError:
            print("Can not connect to %s" % self.OPENFDA_API_URL)

        return res_json

    def list(self, months=6):
        # Return a list of ITEMS_PER_PAGE from the last months

        print ("Listing drug events for last %i months" % months)
        found = []

        end_date = datetime.datetime.now()
        start_date = end_date - dateutil.relativedelta.relativedelta(months=months)
        start = start_date.strftime("%Y%m%d")
        end = end_date.strftime("%Y%m%d")
        search = "search=receivedate:[%s+TO+%s]" % (start, end)

        # Always work with just the first 100 items
        params = "limit=%i" % (self.ITEMS_PER_PAGE)
        params += "&" + search
        res = self.__call(params)
        if 'results' in res:
            found = self.__call(params)['results']
        return found

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
        res = self.__call(params)
        if 'results' in res:
            found = res['results']

        return found
