# Python Substrate Interface Library
#
# Copyright 2018-2020 Stichting Polkascan (Polkascan Foundation).
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
from aiosubstrate.exceptions import StorageFunctionNotFound
from test import settings


class QueryTestCase(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(cls):
        cls.kusama_substrate = SubstrateInterface(
            url=settings.KUSAMA_NODE_URL,
            ss58_format=2,
            type_registry_preset='kusama'
        )

        cls.polkadot_substrate = SubstrateInterface(
            url=settings.POLKADOT_NODE_URL,
            ss58_format=0,
            type_registry_preset='polkadot'
        )

    async def test_system_account(self):

        result = await self.kusama_substrate.query(
            module='System',
            storage_function='Account',
            params=['F4xQKRUagnSGjFqafyhajLs94e7Vvzvr8ebwYJceKpr8R7T'],
            block_hash='0xbf787e2f322080e137ed53e763b1cc97d5c5585be1f736914e27d68ac97f5f2c'
        )

        self.assertEqual(67501, result.value['nonce'])
        self.assertEqual(1099945000512, result.value['data']['free'])
        self.assertEqual(result.meta_info['result_found'], True)

    async def test_system_account_non_existing(self):
        result = await self.kusama_substrate.query(
            module='System',
            storage_function='Account',
            params=['GSEX8kR4Kz5UZGhvRUCJG93D5hhTAoVZ5tAe6Zne7V42DSi']
        )

        self.assertEqual(
            {
                'nonce': 0, 'consumers': 0, 'providers': 0, 'sufficients': 0,
                'data': {
                    'free': 0, 'reserved': 0, 'frozen': 0, 'flags': 170141183460469231731687303715884105728
                }
            }, result.value)

    async def test_non_existing_query(self):
        with self.assertRaises(StorageFunctionNotFound) as cm:
            await self.kusama_substrate.query("Unknown", "StorageFunction")

        self.assertEqual('Pallet "Unknown" not found', str(cm.exception))

    async def test_missing_params(self):
        with self.assertRaises(ValueError):
            await self.kusama_substrate.query("System", "Account")

    async def test_modifier_default_result(self):
        result = await self.kusama_substrate.query(
            module='Staking',
            storage_function='HistoryDepth',
            block_hash='0x4b313e72e3a524b98582c31cd3ff6f7f2ef5c38a3c899104a833e468bb1370a2'
        )

        self.assertEqual(84, result.value)
        self.assertEqual(result.meta_info['result_found'], False)

    async def test_modifier_option_result(self):

        result = await self.kusama_substrate.query(
            module='Identity',
            storage_function='IdentityOf',
            params=["DD6kXYJPHbPRbBjeR35s1AR7zDh7W2aE55EBuDyMorQZS2a"],
            block_hash='0x4b313e72e3a524b98582c31cd3ff6f7f2ef5c38a3c899104a833e468bb1370a2'
        )

        self.assertIsNone(result.value)
        self.assertEqual(result.meta_info['result_found'], False)

    async def test_identity_hasher(self):
        result = await self.kusama_substrate.query("Claims", "Claims", ["0x00000a9c44f24e314127af63ae55b864a28d7aee"])
        self.assertEqual(45880000000000, result.value)

    async def test_well_known_keys_result(self):
        result = await self.kusama_substrate.query("Substrate", "Code")
        self.assertIsNotNone(result.value)

    async def test_well_known_keys_default(self):
        result = await self.kusama_substrate.query("Substrate", "HeapPages")
        self.assertEqual(0, result.value)

    async def test_well_known_keys_not_found(self):
        with self.assertRaises(StorageFunctionNotFound):
            await self.kusama_substrate.query("Substrate", "Unknown")

    async def test_well_known_pallet_version(self):

        sf = await self.kusama_substrate.get_metadata_storage_function("Balances", "PalletVersion")
        self.assertEqual(sf.value['name'], ':__STORAGE_VERSION__:')

        result = await self.kusama_substrate.query("Balances", "PalletVersion")
        self.assertGreaterEqual(result.value, 1)

    async def test_query_multi(self):

        storage_keys = [
            await self.kusama_substrate.create_storage_key(
                "System", "Account", ["F4xQKRUagnSGjFqafyhajLs94e7Vvzvr8ebwYJceKpr8R7T"]
            ),
            await self.kusama_substrate.create_storage_key(
                "System", "Account", ["GSEX8kR4Kz5UZGhvRUCJG93D5hhTAoVZ5tAe6Zne7V42DSi"]
            ),
            await self.kusama_substrate.create_storage_key(
                "Staking", "Bonded", ["GSEX8kR4Kz5UZGhvRUCJG93D5hhTAoVZ5tAe6Zne7V42DSi"]
            )
        ]

        result = await self.kusama_substrate.query_multi(storage_keys)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0][0].params[0], "F4xQKRUagnSGjFqafyhajLs94e7Vvzvr8ebwYJceKpr8R7T")
        self.assertGreater(result[0][1].value['nonce'], 0)
        self.assertEqual(result[1][1].value['nonce'], 0)

    async def test_storage_key_unknown(self):
        with self.assertRaises(StorageFunctionNotFound):
            await self.kusama_substrate.create_storage_key("Unknown", "Unknown")

        with self.assertRaises(StorageFunctionNotFound):
            await self.kusama_substrate.create_storage_key("System", "Unknown")


if __name__ == '__main__':
    unittest.main()
