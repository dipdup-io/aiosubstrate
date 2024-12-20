# Python Substrate Interface Library
#
# Copyright 2018-2023 Stichting Polkascan (Polkascan Foundation).
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

import asyncio
from aiosubstrate import SubstrateInterface, Keypair
from aiosubstrate.exceptions import SubstrateRequestException

# import logging
# logging.basicConfig(level=logging.DEBUG)

async def main():
    substrate = SubstrateInterface(
        url="ws://127.0.0.1:9944"
    )

    substrate = SubstrateInterface(url="ws://127.0.0.1:9944")
    keypair_alice = Keypair.create_from_uri('//Alice', ss58_format=substrate.ss58_format)
    print(keypair_alice.ss58_address)

    keypair = Keypair.create_from_uri('//Alice')

    call = await substrate.compose_call(
        call_module='Balances',
        call_function='transfer_keep_alive',
        call_params={
            'dest': '5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty',
            'value': 1 * 10**15
        }
    )

    print(call.data.to_hex())

    extrinsic = await substrate.create_signed_extrinsic(
        call=call,
        keypair=keypair,
        era={'period': 64}
    )

    try:
        receipt = await substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)

        print('Extrinsic "{}" included in block "{}"'.format(
            receipt.extrinsic_hash, receipt.block_hash
        ))

        if receipt.is_success:

            print('✅ Success, triggered events:')
            for event in (await receipt.triggered_events()):
                print(f'* {event.value}')

        else:
            print('⚠️ Extrinsic Failed: ', receipt.error_message)


    except SubstrateRequestException as e:
        print("Failed to send: {}".format(e))

if __name__ == "__main__":
    asyncio.run(main())