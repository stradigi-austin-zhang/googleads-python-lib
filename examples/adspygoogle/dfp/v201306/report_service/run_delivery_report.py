#!/usr/bin/python
#
# Copyright 2013 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This code example runs a report similar to the "Orders report" on the DFP
website with additional attributes and can filter to include just one order. To
download the report run download_report.py."""

__author__ = ('Jeff Sham',
              'Vincent Tsao')

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))
import time

# Import appropriate classes from the client library.
from adspygoogle import DfpClient


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))

# Initialize appropriate service.
report_service = client.GetService('ReportService', version='v201306')

order_id = 'INSERT_ORDER_ID_HERE'

# Create statement object to filter for an order.
values = [{
    'key': 'id',
    'value': {
        'xsi_type': 'NumberValue',
        'value': order_id
    }
}]
filter_statement = {'query': 'WHERE ORDER_ID = :id',
                    'values': values}

# Create report job.
report_job = {
    'reportQuery': {
        'dimensions': ['ORDER_ID', 'ORDER_NAME'],
        'dimensionAttributes': ['ORDER_TRAFFICKER', 'ORDER_START_DATE_TIME',
                                'ORDER_END_DATE_TIME'],
        'statement': filter_statement,
        'columns': ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS',
                    'AD_SERVER_CTR', 'AD_SERVER_CPM_AND_CPC_REVENUE',
                    'AD_SERVER_WITHOUT_CPD_AVERAGE_ECPM'],
        'dateRangeType': 'LAST_MONTH'
    }
}

# Run report.
report_job = report_service.RunReportJob(report_job)[0]

# Wait for report to complete.
status = report_job['reportJobStatus']
while status != 'COMPLETED' and status != 'FAILED':
  print 'Report job with \'%s\' id is still running.' % report_job['id']
  time.sleep(30)
  status = report_service.GetReportJob(report_job['id'])[0]['reportJobStatus']

if status == 'FAILED':
  print ('Report job with id \'%s\' failed to complete successfully.'
         % report_job['id'])
else:
  print 'Report job with id \'%s\' completed successfully.' % report_job['id']
