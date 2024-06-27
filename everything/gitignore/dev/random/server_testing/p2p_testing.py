import pip
pip.main(['install', 'p2pd'])
print('------------------------')

import p2pd as p2p

async def load_nat():
    # Start the default interface.
    i = await p2p.Interface().start()
    #
    # Load additional NAT details.
    # Restrict, random port NAT assumed by default.
    await i.load_nat()
    #
    # Show the interface details.
    #repr(i)
    return i

async def get_interfaces():
    ifs = await p2p.load_interfaces()
    return ifs



import asyncio
print(asyncio.run(load_nat()))
print('------------------------')
print(asyncio.run(get_interfaces()))

# https://github.com/robertsdotpm/p2pd
# https://p2pd.readthedocs.io/en/latest/
# https://p2pd.readthedocs.io/en/latest/python/basics.html
# https://p2pd.readthedocs.io/en/latest/built/turn.html