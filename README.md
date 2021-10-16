# steam-inventory-manager
Watches your Steam inventory and trades your junk skins to alternate account(s).<br/>

Currently, only CS:GO is supported because of 3rd party pricing data.<br/>
If you ever want to see more popular games supported, please refer me to where I can get accurate pricing information.


***(NOTE: this requires a shared_secret for each account and an identity secret for the main account)***

## Installation & Setup
1. clone with `git clone https://github.com/Hexiro/steam-inventory-manager`
2. rename `config.example.yaml` to `config.yaml` and setup (use comments for reference)
3. start script with `python -m steam-inventory-manager`

## FAQ

***Q: Why not just use Storage Units?***<br/>
*A: For the overwhelming majority of people, a Storage Unit will be enough to store your junk.
The benefit of using steam-inventory-manager comes in with automation. 
This script can move your items automatically, and without having to pay for a storage unit.*

***Q: Do I need CS:GO or Steam installed?***<br/>
*A: Nope. Any OS that runs python 3.8+ should be just fine.*
