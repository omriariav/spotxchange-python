__author__ = 'omriariav'
from spotClass import *
from pprint import pprint


if __name__ == "__main__":
    worker = spotXChangeClass()
    worker.login({
        "username":"USERNAME",
        "password":'PASSWORD'
    })
    revenue_query = {
        "date_range": "yesterday",
        "publisher_id": "98033",
    }
    revenueReport = worker.revenueReport(**revenue_query)
    adverReport = worker.advertisersReport(**revenue_query)
    pprint(adverReport)
    pprint(revenueReport)

