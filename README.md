手順
1. https://java-skill.com/pip-versionup/ 参照
2. https://java-skill.com/aws-pip-error/ 参照
2. git clone
kawamurakosuke:~/environment $ git clone https://github.com/BitMEX/sample-market-maker.git
Cloning into 'sample-market-maker'...
remote: Enumerating objects: 819, done.
remote: Total 819 (delta 0), reused 0 (delta 0), pack-reused 819
Receiving objects: 100% (819/819), 285.78 KiB | 1.03 MiB/s, done.
Resolving deltas: 100% (477/477), done.
3. set up
Create a Testnet BitMEX Account and deposit some TBTC.
Install: sudo pip install bitmex-market-maker. It is strongly recommeded to use a virtualenv.
Create a marketmaker project: run marketmaker setup
This will create settings.py and market_maker/ in the working directory.
Modify settings.py to tune parameters.
Edit settings.py to add your BitMEX API Key and Secret and change bot parameters.
Note that user/password authentication is not supported.
Run with DRY_RUN=True to test cost and spread.
Run it: marketmaker [symbol]
Satisfied with your bot's performance? Create a live API Key for your BitMEX account, set the BASE_URL and start trading!