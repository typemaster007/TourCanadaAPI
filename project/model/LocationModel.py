__author__ = "Daksh Patel"
from project.model import dynamodb, scan_table
import copy
from boto3.dynamodb.conditions import Key


class Location:
    def __init__(self):
        self.dynamodb = dynamodb

    def getLocations(self):
        response = scan_table(table_name='locations').get('Items')
        return response

    def getDestinations(self, location):
        response = scan_table(
            table_name='key_destinations',
            filter_key="location",
            filter_value=location).get('Items')
        return response


if __name__ == '__main__':
    loc = Location()
    print(loc.getDestinations('Dubai'))
