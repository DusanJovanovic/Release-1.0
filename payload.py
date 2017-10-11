# -*- coding: utf-8 -*-


class Payload:
    """
    payload is a dict that contains all search criteria which we can
    change by changing values in this dict.
    This dict is sent to http://www.urbanhome.ch/Search/DoSearch as POST.
    I implemented just 3 methods. It should be implemented more, one for every
    search criteria we have interest to change.
    """

    def __init__(self):
        self.payload = {"settings": {
                                    "MainTypeGroup": "1",
                                    "Category": "1",
                                    "AdvancedSearchOpen": "false",
                                    "MailID": "",
                                    "PayType": "1",
                                    "Type": "1",
                                    "RoomsMin": "0",
                                    "RoomsMax": "0",
                                    "PriceMin": "0",
                                    "PriceMax": "0",
                                    "Regions": [""],
                                    "SubTypes": ["0"],
                                    "SizeMin": "0",
                                    "SizeMax": "0",
                                    "Available": "",
                                    "NoAgreement": "false",
                                    "FloorRange": "0",
                                    "RentalPeriod": "0",
                                    "equipmentgroups": [],
                                    "Email": "",
                                    "Interval": "0",
                                    "SubscriptionType1": "true",
                                    "SubscriptionType2": "true",
                                    "SubscriptionType4": "true",
                                    "SubscriptionType8": "true",
                                    "SubscriptionType128": "true",
                                    "SubscriptionType512": "true",
                                    "Sort": "0"
                                    },
                        "manual": False,
                        "skip": 0,
                        "reset": False,
                        # max items per one search that can be displayed is 200
                        "position": 200,
                        "iframe": 0,
                        "defaultTitle": True,
                        "saveSettings": False}

    def change_region(self, *args):
        """
        Serch can contain multiple regions and cities
        """
        self.payload["settings"]["Regions"] = list(args)

    def change_pay_type(self, pay_type):
        """
        pay_type must be a string, 1 or 2
        1 is for renting real estate
        2 is for buying real estate
        """
        self.payload["settings"]["PayType"] = pay_type

    def change_type(self, estate_type):
        """
        estate_type must be a string; 1, 2, 4, 8, 128 or 512
        """
        self.payload["settings"]["Type"] = estate_type
