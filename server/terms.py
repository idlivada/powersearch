import httplib2
import urllib


url = 'http://search.yahooapis.com/ContentAnalysisService/V1/termExtraction'
appid = 'YahooDemo'

def get_terms(text):
    http = httplib2.Http()
    params = urllib.urlencode({
    'appid': appid,
    'context': text,
    #'query': query,
    'output': 'json'
    })

    response, content = http.request(url, 'POST', params,
                                     headers={'Content-type': 'application/x-www-form-urlencoded'}
                                     )
    
    return content
