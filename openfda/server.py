import http.server
import socketserver
import urllib.parse

from openfda import OpenFDA

CLIENT_PAGE = 'openfda.html'
HTTP_NOT_FOUND = 404
HTTP_OK = 200
PORT = 8000

class OpenFDAHandler(http.server.BaseHTTPRequestHandler):
    """
        Implements the OpenFDA HTTP API:
        - openFDA client
        - searchDrug
        - listDrug
        - searchCompany
        - listCompanies
    """

    API_actions = ["/", "/searchDrug", "/listDrugs", "/searchCompany",
                   "/listCompanies"]

    def send_client(self, status, message):
        self.send_response(status)
        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        # Send message back to client
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))

    def do_GET(self):
        action = self.path.split("?")[0]  # remove the params
        if action not in self.API_actions:
            # The action is not supported in the API
            self.send_client(HTTP_NOT_FOUND, "%s not found" % action)
            return

        openfda = OpenFDA()

        if action == '/':
            # Return the HTML web page for the client
            with open(CLIENT_PAGE) as f:
                html = f.read()
                self.send_client(HTTP_OK, html)
        elif action == '/searchDrug':
            drug_param = self.path.split("?")[1]
            drug_param = urllib.parse.unquote(drug_param)
            drug = drug_param.split("=")[1]
            drug_search = openfda.search_drug(drug)
            self.send_client(HTTP_OK, "Results for %s: %s" % (drug, drug_search))
        elif action == '/listDrugs':
            list_drugs = openfda.list_drugs()
            self.send_client(HTTP_OK, "Results for drugs listing: %s" % list_drugs)
        elif action == '/searchCompany':
            company_param = self.path.split("?")[1]
            company_param = urllib.parse.unquote(company_param)
            company = company_param.split("=")[1]
            company_search = openfda.search_company(company)
            self.send_client(HTTP_OK, "Results for %s: %s" % (company, company_search))
        elif action == '/listCompanies':
            list_companies = openfda.list_companies()
            self.send_client(HTTP_OK, "Results for companies listing: %s" % list_companies)
        return

Handler = OpenFDAHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
