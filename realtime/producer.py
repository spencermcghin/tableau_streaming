# Imports
from __future__ import print_function

import sys
import threading
from pandas import DataFrame
from satori.rtm.client import make_client, SubscriptionMode

# Local Imports
from create_table import engine

# Satori Variables
channel = "live-cyber-attack-threat-map"
endpoint = "wss://open-data.api.satori.com"
appkey = "b43E7E3B430f1aA491787f2bdC690898"

# Local Variables
table = 'hack_attacks'


def main():

    with make_client(
            endpoint=endpoint, appkey=appkey) as client:

        print('Connected!')

        mailbox = []
        got_message_event = threading.Event()

        class SubscriptionObserver(object):
            def on_subscription_data(self, data):
                for message in data['messages']:
                    mailbox.append(message)
                got_message_event.set()

        subscription_observer = SubscriptionObserver()
        client.subscribe(
            channel,
            SubscriptionMode.SIMPLE,
            subscription_observer)

        if not got_message_event.wait(30):
            print("Timeout while waiting for a message")
            sys.exit(1)

        for message in mailbox:
                # Create dataframe
                data = DataFrame([message],
                                 columns=['attack_type', 'attacker_ip', 'attack_port',
                                          'latitude2', 'longitude2', 'longitude',
                                          'city_target', 'country_target', 'attack_subtype',
                                          'latitude', 'city_origin', 'country_origin'])
                # Insert records to table
                try:
                    data.to_sql(table, engine, if_exists='append')

                except Exception as e:
                    print('Error inserting row: ', message)

if __name__ == '__main__':
    main()






