# aiosubstrate

[![Twitter](https://badgen.net/badge/icon/dipdup_io?icon=twitter&label=)](https://twitter.com/dipdup_io)
[![Monthly downloads](https://static.pepy.tech/badge/aiosubstrate/month)](https://pepy.tech/project/dipdup)
[![GitHub stars](https://img.shields.io/github/stars/dipdup-io/aiosubstrate?color=2c2c2c&style=plain)](https://github.com/dipdup-io/aiosubstrate)
[![Python Version](https://img.shields.io/pypi/pyversions/dipdup?color=2c2c2c)](https://www.python.org)
[![License: Apache](https://img.shields.io/github/license/dipdup-io/aiosubstrate?color=2c2c2c)](https://github.com/dipdup-io/aiosubstrate/blob/next/LICENSE)
<br>
[![Latest stable release](https://img.shields.io/github/v/release/dipdup-io/aiosubstrate?label=stable%20release&color=2c2c2c)](https://github.com/dipdup-io/aiosubstrate/releases)
[![Latest pre-release](https://img.shields.io/github/v/release/dipdup-io/aiosubstrate?include_prereleases&label=latest%20release&color=2c2c2c)](https://github.com/dipdup-io/aiosubstrate/releases)
[![GitHub issues](https://img.shields.io/github/issues/dipdup-io/aiosubstrate?color=2c2c2c)](https://github.com/dipdup-io/aiosubstrate/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/dipdup-io/aiosubstrate?color=2c2c2c)](https://github.com/dipdup-io/aiosubstrate/pulls)

> ⚠️ This project is not related to the PolkaScan team! Please, do not send them aiosubstrate bug reports!

> ⚠️ This project is currently in the beta stage. Use with caution.

A library for interacting with Substrate node, an unofficial fork of [py-substrate-interface](https://github.com/polkascan/py-substrate-interface) with primary goal to achieve compatibility with Python asyncio.

## Description

This library specializes in interfacing with a [Substrate](https://substrate.io/) node; querying storage, composing extrinsics, SCALE encoding/decoding and providing additional convenience methods to deal with the features and metadata of the Substrate runtime.

## Documentation

TBD.

- [Upstream library documentation](https://polkascan.github.io/py-substrate-interface/)
- [Upstream metadata documentation for Polkadot and Kusama ecosystem runtimes](https://polkascan.github.io/py-substrate-metadata-docs/)

## Installation

```shell
pip install aiosubstrate

# with additional crypto libraries
pip install aiosubstrate[full]
```

## Initialization

```python
substrate = SubstrateInterface(url="ws://127.0.0.1:9944")
```

After connecting certain properties like `ss58_format` will be determined automatically by querying the RPC node. At the moment this will work for most `MetadataV14` and above runtimes like Polkadot, Kusama, Acala, Moonbeam. For older or runtimes under development the `ss58_format` (default 42) and other properties should be set manually.

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

> ⚠️ This project is not related to the PolkaScan team! Please, do not send them aiosubstrate bug reports!

For questions, please see the [Substrate StackExchange](https://substrate.stackexchange.com/questions/tagged/python), [upstream GitHub Discussions](https://github.com/polkascan/py-substrate-interface/discussions).

## License

[Apache 2.0](https://github.com/dipdup-io/aiosubstrate/blob/master/LICENSE)
