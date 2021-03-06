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

"""Adds a Shared Bidding Strategy and uses it to construct a campaign.

Tags: BiddingStrategyService.mutate
Tags: BudgetService.mutate, CampaignService.mutate
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import AdWordsClient
from adspygoogle.common import Utils


# Enter a shared budget ID to re-use an existing budget or leave as None to
# create a new one.
BUDGET_ID = None


def main(client, budget_id):
  bidding_strategy = CreateBiddingStrategy(client)

  if budget_id is None:
    budget = CreateSharedBudget(client)
    budget_id = budget['budgetId']

  CreateCampaignWithBiddingStrategy(client, bidding_strategy['id'], budget_id)


def CreateBiddingStrategy(client):
  """Creates a bidding strategy object.

  Args:
    client: AdWordsClient the client to run the example with.

  Returns:
    dict An object representing a bidding strategy.
  """
  # Initialize appropriate service.
  bidding_strategy_service = client.GetBiddingStrategyService(version='v201309')

  # Create a shared bidding strategy.
  shared_bidding_strategy = {
      'name': 'Maximize Clicks %s' % Utils.GetUniqueName(),
      'biddingScheme': {
          'xsi_type': 'TargetSpendBiddingScheme',
          # Optionally set additional bidding scheme parameters.
          'bidCeiling': {
              'microAmount': '2000000'
          }
      }
  }

  # Create operation.
  operation = {
      'operator': 'ADD',
      'operand': shared_bidding_strategy
  }

  response = bidding_strategy_service.mutate([operation])[0]
  new_bidding_strategy = response['value'][0]

  print ('Shared bidding strategy with name \'%s\' and ID \'%s\' of type \'%s\''
         'was created.' %
         (new_bidding_strategy['name'], new_bidding_strategy['id'],
          new_bidding_strategy['biddingScheme']['BiddingScheme_Type']))

  return new_bidding_strategy


def CreateSharedBudget(client):
  """Creates an explicit budget to be used only to create the Campaign.

  Args:
    client: AdWordsClient the client to run the example with.

  Returns:
    dict An object representing a shared budget.
  """
  # Initialize appropriate service.
  budget_service = client.GetBudgetService(version='v201309')

  # Create a shared budget
  budget = {
      'name': 'Shared Interplanetary Budget #%s' % Utils.GetUniqueName(),
      'period': 'DAILY',
      'amount': {
          'microAmount': '2000000'
      },
      'deliveryMethod': 'STANDARD',
      'isExplicitlyShared': 'true'
  }

    # Create operation.
  operation = {
      'operator': 'ADD',
      'operand': budget
  }

  response = budget_service.mutate([operation])[0]
  return response['value'][0]


def CreateCampaignWithBiddingStrategy(client, bidding_strategy_id, budget_id):
  """ Create a Campaign with a Shared Bidding Strategy.

  Args:
    client: AdWordsClient the client to run the example with.
    bidding_strategy_id: string the bidding strategy ID to use.
    shared_budget_id: string the shared budget ID to use.

  Returns:
    dict An object representing a campaign.
  """
  # Initialize appropriate service.
  campaign_service = client.GetCampaignService(version='v201309')

  # Create campaign.
  campaign = {
      'name': 'Interplanetary Cruise #%s' % Utils.GetUniqueName(),
      'budget': {
          'budgetId': budget_id
      },
      'biddingStrategyConfiguration': {
          'biddingStrategyId': bidding_strategy_id
      },
      'settings': [{
          'xsi_type': 'KeywordMatchSetting',
          'optIn': 'true'
      }],
      'networkSetting': {
          'targetGoogleSearch': 'true',
          'targetSearchNetwork': 'true',
          'targetContentNetwork': 'true'
      }
  }

  # Create operation.
  operation = {
      'operator': 'ADD',
      'operand': campaign
  }

  response = campaign_service.mutate([operation])[0]
  new_campaign = response['value'][0]

  print ('Campaign with name \'%s\', ID \'%s\' and bidding scheme ID \'%s\' '
         'was created.' %
         (new_campaign['name'], new_campaign['id'],
          new_campaign['biddingStrategyConfiguration']['biddingStrategyId']))

  return new_campaign


if __name__ == '__main__':
  # Initialize client object.
  client_ = AdWordsClient(path=os.path.join('..', '..', '..', '..', '..'))

  main(client_, BUDGET_ID)
