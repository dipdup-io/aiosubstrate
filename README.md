# Python Substrate Interface

[![Build Status](https://img.shields.io/github/actions/workflow/status/dipdup-io/aiosubstrate/unittests.yml?branch=master)](https://github.com/dipdup-io/aiosubstrate/actions?query=workflow%3A%22Run+unit+tests%22)
[![Latest Version](https://img.shields.io/pypi/v/aiosubstrate.svg)](https://pypi.org/project/aiosubstrate/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/aiosubstrate.svg)](https://pypi.org/project/aiosubstrate/)
[![License](https://img.shields.io/pypi/l/aiosubstrate.svg)](https://github.com/dipdup-io/aiosubstrate/blob/master/LICENSE)


## Description
This library specializes in interfacing with a [Substrate](https://substrate.io/) node; querying storage, composing extrinsics, 
SCALE encoding/decoding and providing additional convenience methods to deal with the features and metadata of 
the Substrate runtime.

## Documentation

* [Library documentation](https://polkascan.github.io/aiosubstrate/)
* [Metadata documentation for Polkadot and Kusama ecosystem runtimes](https://polkascan.github.io/py-substrate-metadata-docs/)

## Installation
```bash
pip install aiosubstrate
```

## Initialization

```python
substrate = SubstrateInterface(url="ws://127.0.0.1:9944")
```

After connecting certain properties like `ss58_format` will be determined automatically by querying the RPC node. At 
the moment this will work for most `MetadataV14` and above runtimes like Polkadot, Kusama, Acala, Moonbeam. For 
older or runtimes under development the `ss58_format` (default 42) and other properties should be set manually. 

## Quick usage

### Balance information of an account
```python
result = await substrate.query('System', 'Account', ['F4xQKRUagnSGjFqafyhajLs94e7Vvzvr8ebwYJceKpr8R7T'])
print(result.value['data']['free']) # 635278638077956496
```
### Create balance transfer extrinsic

```python
call = await substrate.compose_call(
    call_module='Balances',
    call_function='transfer',
    call_params={
        'dest': '5E9oDs9PjpsBbxXxRE9uMaZZhnBAV38n2ouLB28oecBDdeQo',
        'value': 1 * 10**12
    }
)

keypair = Keypair.create_from_uri('//Alice')
extrinsic = await substrate.create_signed_extrinsic(call=call, keypair=keypair)

receipt = await substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)

print(f"Extrinsic '{receipt.extrinsic_hash}' sent and included in block '{receipt.block_hash}'")
```

## Contact and Support 

For questions, please see the [Substrate StackExchange](https://substrate.stackexchange.com/questions/tagged/python), [Github Discussions](https://github.com/dipdup-io/aiosubstrate/discussions) or 
reach out to us on our [matrix](http://matrix.org) chat group: [Polkascan Technical](https://matrix.to/#/#polkascan:matrix.org).

## License
https://github.com/dipdup-io/aiosubstrate/blob/master/LICENSE
