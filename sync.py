#!/bin/env python3
"""
Syncs the to_sort directory with the remote directory without stopping and removing the SD card.
Two parameters are required:
- the IP address of the remote server
- the number of days to sync 
"""
import datetime, os
import requests
import sys 
from bs4 import BeautifulSoup


if __name__ == '__main__':
    ip = sys.argv[1]
    last_n_days = int(sys.argv[2])
    for i in range(last_n_days):
        date = datetime.datetime.now() - datetime.timedelta(days=i)
        date = date.strftime('%Y%m%d')
        for i in range(20):
            url = f'http://{ip}/fileserver/log/digit/{date}/{i:02d}/'
            print(url)
            response = requests.get(url, verify=False)
            soup = BeautifulSoup(response.text)
            for link in soup.findAll('a'):
                if link['href'].endswith('.jpg'):
                    pic_url = f'http://{ip}{link["href"]}'
                    print(pic_url)
                    response = requests.get(pic_url, verify=False)
                    filename = os.path.join("to_sort/", link["href"].split('/')[-1])
                    with open(filename, 'bw') as f:
                        f.write(response.content)