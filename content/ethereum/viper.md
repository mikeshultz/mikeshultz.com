Title: Deploying an Ethereum Viper Smart Contract
Date: 2017-05-21 20:17:34
Modified: 2017-11-15 19:21:32
Category: Ethereum
Tags: cryptocurrency, ethereum, viper, smart contract
Slug: deploying-ethereum-viper-smart-contract
Authors: Mike Shultz
Summary: Viper is missing a lot of documentation.  It took a lot of trial and error to finally figure out how to deploy a contract to an Ethereum blockchain.  Here's how I created a smart contract in Viper and deployed it via Geth(go-ethereum).

Viper is missing a lot of documentation(though it has gotten better).  It took a lot of trial and error to finally figure out how to deploy a contract to an Ethereum blockchain.  This information may not be very useful for people who have deployed compiled smart contracts before.  This is more geared towards people who are using Viper as their first language to create Ethereum smart contracts but are familiar with common Python development practices, and their local system.

I'd recommend using [this docker container](https://github.com/mikeshultz/ethereum-geth-dev).  I updated it slightly from the original and doesn't match what's in Docker Hub.  Alternatively, [testrpc](https://github.com/ethereumjs/testrpc) is easier to setup, but has on occasion had me chasing bugs for too long(YMMV).  Either way, it's a lot better to test things out before real money is at stake on the main net.  Alternatively, you could setup a full node on a test network, but the test networks are not always completely functional, so probably not the best choice for quick dev.

In this article, I'm going to be deploying the contract using geth([go-ethereum](https://github.com/ethereum/go-ethereum)), but the geth commands should be loosely similar to any web3 interface or library.  I may add information on how to use Mist and other Web3 browsers/wallets to deploy contracts later, but for now I haven't needed or wanted it.

## Get Familiar With Viper

First and foremost, [read the documentation they have](https://viper.readthedocs.io/en/latest/index.html).  It's the only authoritative information about the language there is, so it's a good(only) goto for reference. For people familiar with some of the newer concepts of Python 3, it should be mostly straight forward.  It utilizes type hinting a lot.  Though of course there are some significant differences.  I won't be going into that in depth here but I will point out some differences that were important when writing my first contract.

Viper does **not** use all the same types as Python.  There's special types for Ethereum-useful data like `address` and `wei-value` which you'll likely use a lot.  The one that will likely trip you up the most is that `float` and `int` are not really a thing in Viper.  Instead, Viper uses `num` and `decimal`.  They can almost be thought of the same, except that they do have fixed lengths.  See the [Types section of the documentation](https://viper.readthedocs.io/en/latest/types.html) for more detailed information.

<s>The grammar has some unexpected gotchas as well. When in doubt see the [Grammar section of the README](https://github.com/ethereum/viper#grammar).  It can be a little annoying to parse at first, but you'll get the hang of it.</s> [This grammar does not appear to be available anymore at the time of this update.]  

Declaration of globally assigned variables is also a departure from Python but is something you'll need to be familiar with.  There's not a whole lot of information to go on except [the code examples in their repository](https://github.com/ethereum/viper/tree/master/examples). They are declared in the "header" of the file, and any globals that you might want defined at the time of deploy should be set in the constructor of the contract. These are referenced through `self` and unlike python, `self` does not need to be an argument in the functions.  For instance, say you were creating a contact that needed to reach a goal before distributing funds, you could define the goal value at the top of the Viper contract like this: 

    goal: wei_value

## Install Viper

You may need various encryption dependencies for your system.  It can vary on how and what you might need depending on your distro, so I'm going to leave that to you to figure out along the way.  Assuming system libraries are already installed, we can go ahead and setup the virtualenv for Viper and install.  **You will need Python 3.6** and git installed for these steps.

    # python3.6 -m venv ~/venvs/viper && . ~/venvs/viper/bin/activate
    # mkdir -p ~/dev/viper && cd ~/dev/viper && git clone https://github.com/ethereum/viper.git . && python setup.py install

That should get you setup with a base install of Viper and the command `viper` should now be available to you.

## Write Your Contract

Let's start out with a simple contract that will accept deposits and distribute the balance to a specified address when triggered.  Nothing really sexy about it, but it should show a basic set of features to get you started.  We're going to create the file `example.vy`:

    owner: address

    def __init__(_owner: address):
        self.owner = _owner

    def check_balance() -> wei_value:
        return self.balance

    def distribute():
        assert self.balance > 0
        send(self.owner, self.balance)

    @payable
    def deposit() -> bool:
        # Deposit value in the contract and record the sender and value.
        # Direct transfers can also be made to the contract, but wanted to leave
        # this here because likely, your contract has more logic for deposits
        assert(msg.value > 0)

This is incredibly simple and there's a lot more you can do with Viper but that's a bit out of scope here.

## Compile Your Contract

Now we're going to compile it to the bytecode that will actually be deployed to the blockchain.

    # viper example.vy

It should spit out a long hex string(e.g. `0x600035601c52740100000000000...`) which is the compiled bytecode of our contract.  Save this for later, we'll need it.

## Generate Your ABI

[An ABI, for those unfamiliar](https://en.wikipedia.org/wiki/Application_binary_interface) is basically a human and machine readable reference that tells the Ethereum client what functions and variables are defined in the contract(and to reference their location in the EVM).  We no longer have to write our own ABIs!  But it's still a pretty good idea to read up on [Ethereum smart contract ABIs in JSON](https://github.com/ethereum/wiki/wiki/Ethereum-Contract-ABI#json) because it can be pretty useful to know what these mean for future troubleshooting. 

So now, let's use viper to generate our ABI: 

    viper -f abi example.vy

Here's a formatted example the ABI for `example.vy`:

    [
        {
            'name': '__init__(address)', 
            'outputs': [], 
            'inputs': [
                {
                    'type': 'address', 
                    'name': '_owner'
                }
            ], 
            'constant': False, 
            'payable': False, 
            'type': 'constructor'
        }, 
        {
            'name': 'check_balance()', 
            'outputs': [
                {
                    'type': 'int128', 
                    'name': 'out'
                }
            ], 
            'inputs': [], 
            'constant': True, 
            'payable': False, 
            'type': 'function'
        }, 
        {
            'name': 'distribute()', 
            'outputs': [], 
            'inputs': [], 
            'constant': False, 
            'payable': False, 
            'type': 'function'
        }, 
        {
            'name': 'deposit()', 
            'outputs': [
                {
                    'type': 'bool', 
                    'name': 'out'
                }
            ], 
            'inputs': [], 
            'constant': False, 
            'payable': True, 
            'type': 'function'
        }
    ]

The concept is pretty straight forward enough, with a couple of exceptions.  `constant` tells the EVM whether or not the function makes any alterations to the blockchain.  If you're sending ether, or altering data, or doing any kind of transaction, your function is **not constant**.  Anything that can be run locally on whatever node you make the RPC/IPC call on, is constant.  Data types used in the ABI are [Solidity types](https://github.com/ethereum/wiki/wiki/Ethereum-Contract-ABI#types) and **not Viper types**, so keep that in mind.  For instance, `num` and `decimal` are not a thing here and instead you may want to use `int`.  And __decimal/floats are not a thing outside of Viper and should be avoided for return values.__

## Deploy Your Contract Using Geth

So I'm assuming you have a running `geth` instance already(ideally on a private chain).  If not [go get this docker container](https://github.com/mikeshultz/ethereum-geth-dev) or setup [testrpc](https://github.com/ethereumjs/testrpc).  I'll wait.

![Still waiting](http://i.imgur.com/hniy4My.jpg)

Okay, good.  Now attach to your running geth instance from another terminal.  You can technically run your main instance as a console, but you'll have block notices cluttering up your interface.

    # geth attach

Realistically if you're running a private chain on your local machine, it might be a little more complex, like this: 

    # geth attach --datadir "/data/ethereum/testchain0" ipc:/data/ethereum/testchain0/geth.ipc

**NOTE** that the IPC path here is not documented in the command's `--help` output.

Now that you have a geth console, we can deploy our contract directly from here.  First we're going to define the recipient address of the ether.  This is the address that `distribute` will send the contract's funds to when called.

    > var owner = eth.accounts[0]

We will need the JSON ABI definition we created earlier.  It's best to remove newlines here or `geth` will wig out.

    > var abi = [{'name': '__init__(address)', 'outputs': [], 'inputs': [{'type': 'address', 'name': '_owner'}], 'constant': False, 'payable': False, 'type': 'constructor'}, {'name': 'check_balance()', 'outputs': [{'type': 'int128', 'name': 'out'}], 'inputs': [], 'constant': True, 'payable': False, 'type': 'function'}, {'name': 'distribute()', 'outputs': [], 'inputs': [], 'constant': False, 'payable': False, 'type': 'function'}, {'name': 'deposit()', 'outputs': [{'type': 'bool', 'name': 'out'}], 'inputs': [], 'constant': False, 'payable': True, 'type': 'function'}]

We'll also need the bytecode hex string we compiled from Viper.

    > var bytecode = "0x600035601c52740100000000000000000000000000000000000000006020526fffffffffffffffffffffffffffffffff6040527fffffffffffffffffffffffffffffffff000000000000000000000000000000016060527402540be3fffffffffffffffffffffffffdabf41c006080527ffffffffffffffffffffffffdabf41c00000000000000000000000002540be40060a0526020610223610140393415155857602061022360c03960c05160205181101558575061014051600055600160025561020b56600035601c52740100000000000000000000000000000000000000006020526fffffffffffffffffffffffffffffffff6040527fffffffffffffffffffffffffffffffff000000000000000000000000000000016060527402540be3fffffffffffffffffffffffffdabf41c006080527ffffffffffffffffffffffffdabf41c00000000000000000000000002540be40060a0526398ba1d4660005114156100b2573415155857303160005260206000f3005b63e4fc6b6d60005114156100e05734151558576000303113155857600060006000600030316000546000f150005b63d0e30db06000511415610144576000341315585733600160c05260c06020200154156101295733600160c05260c06020200134815401815550600160005260206000f3610142565b3433600160c05260c06020200155600160005260206000f35b005b5b6100c661020b036100c66000396100c661020b036000f3"

Now we create a contract instance using the ABI.  We can deploy instances of our contract from this and it can be reused.

    > my_awesome_contract = eth.contract(abi)

Unlock your account so you can actually make transactions from it.

    > personal.unlockAccount(eth.accounts[0])

And using this contract factory, we can deploy the contract.  The arguments here match the constructor `__init__` from your `example.vy` file except for the last argument which is [a transaction object](https://github.com/ethereum/wiki/wiki/JavaScript-API#web3ethgettransaction).

    > var deployed_contract = my_awesome_contract.new(owner, {from: eth.accounts[0], data: bytecode, gas: 4000000})

The final argument(the JavaScript object) defines some important values for this contract instance.  `data` of course contains the compiled `bytecode` we got from the output of `viper`.  `from` is required as it's the account creating the contract.  It will be responsible for paying any fees for deploying the contract.  Usually this would be your `geth` primary account(`eth.accounts[0]`), but it could be any account you have unlocked on this `geth` instance.

And finally, [`gas`](https://ethereum.gitbooks.io/frontier-guide/content/costs.html), which should be the expected amount of gas used by your contract.  The viper compiler does not do gas estimation, so you may to have to do a bit of trial and error to get the right gas limit.  Or just set it high if you don't mind paying for errors.  The number above is just an approximate amount of wei that has seemed to work in testing.

You can check whether the transaction has been processed and included in a block using `transactionHash` in `deployed_contract`.

    > eth.getTransactionReceipt(deployed_contract.transactionHash)
    {
      blockHash: "0x7cac3415a2da551c47255424f51942ad52e7b69044167a568f22f677e561555a",
      blockNumber: 17682,
      contractAddress: null,
      cumulativeGasUsed: 21133,
      from: "0x75c4a4656baa10c225eaa45ab25df8f9e9025638",
      gasUsed: 21133,
      logs: [],
      logsBloom: "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
      root: "0x5f9598082339f0a1d322a44e77ab78c5ecf70754780019300cbb3c170ef454ff",
      to: "0xfdead766ea8d64f46979f0d8551d2eb923809a69",
      transactionHash: "0x4257a95885397fbda3c3962a8635d77903f744296b893abf05cfcc21ed509c5c",
      transactionIndex: 0
    }

Once the transaction is confirmed and included in a block(up to 15 minutes on the public chain with a reasonable gas price), `deployed_contract` should now have an address available.

    > var contract_address = deployed_contract.address
    "0xdeadbeefe28a3e8358ba34aef0c03ef0e2b26ea6"

You will need this address later to make any calls or deposits to your contract, so keep it safe.  Though if you do lose it, you may be able to find it by looking up your primary account on [etherscan.io](https://etherscan.io/).

## Use Your Contract

Now, let's mess around with our new fancy contract.  If you're on the same console, you won't have to redefine your ABI and contract, but for the sake of reference I'm going to do it here anyway.

    var abi =[{'name': '__init__(address)', 'outputs': [], 'inputs': [{'type': 'address', 'name': '_owner'}], 'constant': False, 'payable': False, 'type': 'constructor'}, {'name': 'check_balance()', 'outputs': [{'type': 'int128', 'name': 'out'}], 'inputs': [], 'constant': True, 'payable': False, 'type': 'function'}, {'name': 'distribute()', 'outputs': [], 'inputs': [], 'constant': False, 'payable': False, 'type': 'function'}, {'name': 'deposit()', 'outputs': [{'type': 'bool', 'name': 'out'}], 'inputs': [], 'constant': False, 'payable': True, 'type': 'function'}]
    contract_address = "0xdeadbeefe28a3e8358ba34aef0c03ef0e2b26ea6"
    deployed_contract = eth.contract(abi).at("0xdeadbeefe28a3e8358ba34aef0c03ef0e2b26ea6")

And from this, we can make calls/transactions to the contract.  Let's check the balance, which is probably zero unless someone generous already sent your contract ether.

    > deployed_contract.check_balance()
    0

Zero, as expected.  Now, let's add .5 ether to it to make the contract useful.  

**NOTE** that contracts only deal with the smallest denomination in Ethereum: wei.  But the web3 library has some handy converters should you want to not count zeros until your eyes bleed.

    > personal.unlockAccount(eth.accounts[0])
    > var transaction = deployed_contract.deposit({from:eth.accounts[0], value: web3.toWei(0.5, "ether")})

**NOTE**: Notice we have defined `from` and `value` in a transaction object here.  Any function calls that are not `constant` will need to have a sending account set or you will get an `Error: invalid address`.  Alternatively, you could set a default account like this: `eth.defaultAccount = eth.accounts[0]` and that should last for your entire session.

Again, after confirmation and inclusion in a block, the contract should have a balance, as we can see here: 

    > deployed_contract.check_balance()
    500000000000000000

Now at any time you(or anyone else) can `distribute` this ether to the owner address you defined when deploying the contract.

    > deployed_contract.distribute({from:eth.accounts[0]})

## Congratulations

You have written and deployed your first Ethereum Viper contract.  Whenever you're ready for prime-time, you can use the same steps to deploy your contract to the live Ethereum chain.  Just make sure your `geth` instance is not the private network you created.

If you find any errors or omissions here, [please let me know](mailto:mike@mikeshultz.com).