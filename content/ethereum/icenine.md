Title: Icenine - A graphical Ethereum cold wallet
Date: 2017-08-17 23:31:34
Category: Ethereum
Tags: cryptocurrency, ethereum, wallet
Slug: icenine-graphical-ethereum-cold-wallet
Authors: Mike Shultz
Summary: The cold wallet options for Ethereum were sorely lacking, in my opinion and needed something that would function properly on an air-gapped machine and didn't have the worst UX ever.  So I made Icenine!

### [Check out Icenine on GitHub](https://github.com/mikeshultz/icenine)

I needed a secure place to put my *favorite Ether*.  Every hardware wallet is sold out and not shipping again until the fall, at least.  So that leaves an air-gapped computer, and for that, the only options are [MyEtherWallet(MEW)](https://www.myetherwallet.com/) and [Icebox](https://github.com/ConsenSys/icebox).  

MEW barely works at all when on an offline computer, and you're likely to have to use the provided Web3 provider in the JavaScript console to get everything you want.  Last time I tried it, I wasn't even able to see the account addresses for the accounts I created.  This wasn't really acceptable.

Next I tried Icebox.  It's functional, but requires users to run a Web page and has probably the worst UX ever.  Icebox also doesn't really handle multiple accounts or any kind of storage.

![Icebox Screenshot](http://i.imgur.com/EslcytB.png)

So, in order for me to securely store my *favorite Ether*, I decided to write my own wallet.  I used a couple of pieces from [pyethereum](https://github.com/ethereum/pyethereum/) (Thanks!), and modded it, built a good API around it, and created a slightly less gross Qt5 interface for it.  It's not the prettiest thing, but I think the usability and general user experience are a lot better than Icebox.

![Icenine Main Window](http://i.imgur.com/hMpe0jm.png)

In the main window, a user can select an account on the left hand side and create a transaction with that account on the right.  Icenine keeps track of the `nonce`, previous `gasprice`, and `startgas`, which are used to try and automatically fill the form in.  When you click 'Create Transaction', it will ask for your unlock password(to decrypt the account) if the account has not already been unlocked.  Then it will display the full raw transaction you can copy and save to a thumbdrive to transfer to an Internet connected machine.

The best part is that you can send the transaction on untrusted nodes and as far as I know, there is no way to tamper with it.

![Icenine Alias Window](http://i.imgur.com/FjY022J.png)

Icenine also allows you to manage address aliases.  You can set names for accounts to make them easier to remember.  These aliases are easily backed up using the Import/Export functionality found in the main window.

![Icenine Transaction Window](http://i.imgur.com/F8X3zh2.png)

The wallet also keeps track of all previously saved transactions.  This allows it to keep up to date with the account's nonce and automagically fill in previous gas values.  And, it can be a handy reference, even though etherscan may be a better option.

Icenine is also compatbile with the pseudo-standard [Web3 Secret Storage Definition](https://github.com/ethereum/wiki/wiki/Web3-Secret-Storage-Definition).  This should make it compatible with any accounts created with [go-ethereum(geth)](https://github.com/ethereum/go-ethereum) and other clients.  

Though, the security conscious should generate your accounts using Icenine on an air-gapped machine so those key files can never be exposed to the Internet.  For the best security, a completely random private key can be generated. Alternatively, you can also generate your private key using random seed words or seed words that you provide yourself.  Seed words, which slightly less secure than something completely random, allow you to write them down so you can recover the private key should you lose your digital copies.  These are compatible with the parity pseudo-standard, but it's not clear if that will always be compatible.

Anyway, the first Alpha, [0.1.0a2 was released today](https://pypi.python.org/pypi/icenine) and I hope to make many improvements in the future.  See the [Icenine GitHub page](https://github.com/mikeshultz/icenine) for more information or to get the most up to date build.  If you're feeling daring, please test it out and submit any issues on the GitHub page.