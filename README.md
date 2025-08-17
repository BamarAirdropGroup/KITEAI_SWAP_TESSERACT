# KITEAI_SWAP_TESSERACT




Features:
Swapping Native KITE Token to Native TUSD



Requirements:
- You need KITE token

If you do not have KITE Token, go to the faucet and claim .
Faucet link --->  https://faucet.gokite.ai/ 


#clone the repo

git clone https://github.com/BamarAirdropGroup/KITEAI_SWAP_TESSERACT.git && cd KITEAI_SWAP_TESSERACT && pip install -r requirements.txt

#add  privatekey one key per line (Not add PRIVATE_KEY_1/2/3.. etc , only add privatekey)

nano accounts.txt


#If you want to add proxy (add the proxy like that format http://username:password@ip:port . Some free proxy will undergo error) 


nano proxy.txt


#Running 

python bot.py 


#Select proxy option 

1 for free proxy which will be auto downloaded to proxy.txt
2 for private proxy
3 for direct connection 
