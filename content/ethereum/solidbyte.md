Title: Solidbyte Smart Contract Framework
Date: 2019-01-30 00:12:36
Category: Ethereum
Tags: cryptocurrency, ethereum
Slug: solidbyte-intro
Authors: Mike Shultz
Summary: Solidbyte is an Ethereum smart contract development framework that supports Solidity and Vyper.  Tests and deployment scripts are written in Python for maximum fun.

### [Check out Solidbyte on GitHub](https://github.com/mikeshultz/solidbyte)

**NOTE**: Solidbyte is still early Alpha.  While things mostly work, there may be some bugs and changes may occur quickly.

## What is Solidbyte

Solidbyte is a smart contract development framework, similar to the much loved <a href="/home/mike/.nvm/versions/node/v8.11.1/bin/lessc">Truffle framework</a>.  It provides a framework for contract compilation, unit testing, deployment, and various tools to help with that process.

## Why?

Well, personal preference mostly.  I spent a lot of time working with Truffle, and tried out others like Populus.  There are a lot of things they were missing that I liked to have and keeping a second collection of little scripts around was getting annoying.  And while Truffle has bee mostly great, with a little hair pulling here and there, I was getting increasingly sick of JavaScript.  I wanted to go back to Python.  I want to write my tests and deployment scripts in Python.  It's entirely personal preference, but it makes me warm and fuzzy inside.  So, if you prefer JavaScript, I'd suggest stucking with Truffle.

## Why not?

Well, if you don't like Python or having fun, use something else.

## What makes Solidbyte different?

Right now, Solidbyte has a few features that aren't included in other frameworks:

- Local account support! It's 2019, why is anyone using `personal_unlock` over the network?!?
- Support for both Solidity and Vyper (and both together)
- A Python interactive console
- A function and event signature dump
- EthPM Support (okay, it's in progress...)
- "Projcet templates" that allow you to standup a project structure with common patterns quickly. (ERC20 tokens, for instance)
- [eth_tester](https://github.com/ethereum/eth-tester/) support, for superfast testing
- Unit testing with pytest, including commonly used fixtures

## What's to come?

- EthPM Support.  Like actually working, I mean
- Smoothing of rough edges and improvement of the developer experience
- Code coverage integration
- More project templates
- More pytest fixtures
- Vyper and Solidity intermingling. Use of Solidity libraries for vyper, for instance.  Will be tested and smoothed out
- Example projects

Feedback is always appreicated.  Hit me up at the E-mail address in the header or [open a GitHub issue](https://github.com/mikeshultz/solidbyte/issues/new) and we can discuss further.
