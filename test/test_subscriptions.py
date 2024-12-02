# Python Substrate Interface Library
#
# Copyright 2018-2021 Stichting Polkascan (Polkascan Foundation).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from aiosubstrate import SubstrateInterface
from test import settings


class SubscriptionsTestCase(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(cls):
        cls.substrate = SubstrateInterface(
            url=settings.POLKADOT_NODE_URL
        )

    async def test_query_subscription(self):

        async def subscription_handler(obj, update_nr, subscription_id):

            return {'update_nr': update_nr, 'subscription_id': subscription_id}

        result = await self.substrate.query("System", "Events", [], subscription_handler=subscription_handler)

        self.assertIsNotNone(result['subscription_id'])

    async def test_subscribe_storage_multi(self):

        async def subscription_handler(storage_key, updated_obj, update_nr, subscription_id):
            return {'update_nr': update_nr, 'subscription_id': subscription_id}

        storage_keys = [
            await self.substrate.create_storage_key(
                "System", "Account", ["5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"]
            ),
            await self.substrate.create_storage_key(
                "System", "Account", ["5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty"]
            )
        ]

        result = await self.substrate.subscribe_storage(
            storage_keys=storage_keys, subscription_handler=subscription_handler
        )

        self.assertIsNotNone(result['subscription_id'])

    async def test_subscribe_new_heads(self):

        async def block_subscription_handler(obj, update_nr, subscription_id):
            return obj['header']['number']

        result = await self.substrate.subscribe_block_headers(block_subscription_handler, finalized_only=True)

        self.assertGreater(result, 0)


if __name__ == '__main__':
    unittest.main()
