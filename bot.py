from web3 import Web3
from eth_account import Account
from colorama import Fore, Style
from datetime import datetime, timedelta
import pytz, asyncio, json, os, random
import re
import requests

wib = pytz.timezone('Asia/Singapore')

class KiteAi:
    def __init__(self):
        self.KITE_AI = {
            "rpc_url": "https://rpc-testnet.gokite.ai/",
            "explorer": "https://testnet.kitescan.ai/tx/",
            "chain_id": 2368
        }
        self.USDT_CONTRACT_ADDRESS = "0x0fF5393387ad2f9f691FD6Fd28e07E3969e27e63"
        self.WKITE_CONTRACT_ADDRESS = "0x3bC8f037691Ce1d28c0bB224BD33563b49F99dE8"
        self.SWAP_ROUTER_ADDRESS = "0x04CfcA82fDf5F4210BC90f06C44EF25Bf743D556"
        self.ZERO_CONTRACT_ADDRESS = "0x0000000000000000000000000000000000000000"
        self.DEST_BLOCKCHAIN_ID = "0x6715950e0aad8a92efaade30bd427599e88c459c2d8e29ec350fc4bfb371a114"
        self.ERC20_CONTRACT_ABI = json.loads('''[
            {"type":"function","name":"balanceOf","stateMutability":"view","inputs":[{"name":"address","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},
            {"type":"function","name":"allowance","stateMutability":"view","inputs":[{"name":"owner","type":"address"},{"name":"spender","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},
            {"type":"function","name":"approve","stateMutability":"nonpayable","inputs":[{"name":"spender","type":"address"},{"name":"amount","type":"uint256"}],"outputs":[{"name":"","type":"bool"}]},
            {"type":"function","name":"decimals","stateMutability":"view","inputs":[],"outputs":[{"name":"","type":"uint8"}]},
            {"type":"function","name":"send","stateMutability":"nonpayable","inputs":[{"name":"_destChainId","type":"uint256"},{"name":"_recipient","type":"address"},{"name":"_amount","type":"uint256"}],"outputs":[]},
            {
                "type":"function",
                "name":"initiate",
                "stateMutability":"nonpayable",
                "inputs":[
                    {"name":"token","type":"address","internalType":"address"}, 
                    {"name":"amount","type":"uint256","internalType":"uint256"}, 
                    { 
                        "name":"instructions", 
                        "type":"tuple", 
                        "internalType":"struct Instructions",
                        "components":[
                            {"name":"sourceId","type":"uint256","internalType":"uint256"}, 
                            {"name":"receiver","type":"address","internalType":"address"}, 
                            {"name":"payableReceiver","type":"bool","internalType":"bool"}, 
                            {"name":"rollbackReceiver","type":"address","internalType":"address"}, 
                            {"name":"rollbackTeleporterFee","type":"uint256","internalType":"uint256"}, 
                            {"name":"rollbackGasLimit","type":"uint256","internalType":"uint256"}, 
                            {
                                "name":"hops",
                                "type":"tuple[]",
                                "internalType":"struct Hop[]",
                                "components":[
                                    {"name":"action","type":"uint8","internalType":"enum Action"}, 
                                    {"name":"requiredGasLimit","type":"uint256","internalType":"uint256"}, 
                                    {"name":"recipientGasLimit","type":"uint256","internalType":"uint256"}, 
                                    {"name":"trade","type":"bytes","internalType":"bytes"}, 
                                    {
                                        "name":"bridgePath",
                                        "type":"tuple",
                                        "internalType":"struct BridgePath",
                                        "components":[
                                            {"name":"bridgeSourceChain","type":"address","internalType":"address"},
                                            {"name":"sourceBridgeIsNative","type":"bool","internalType":"bool"},
                                            {"name":"bridgeDestinationChain","type":"address","internalType":"address"},
                                            {"name":"cellDestinationChain","type":"address","internalType":"address"},
                                            {"name":"destinationBlockchainID","type":"bytes32","internalType":"bytes32"},
                                            {"name":"teleporterFee","type":"uint256","internalType":"uint256"},
                                            {"name":"secondaryTeleporterFee","type":"uint256","internalType":"uint256"}
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "outputs":[]
            }
        ]''')
        
        self.NATIVE_CONTRACT_ABI = json.loads('''[
            {"type":"function","name":"send","stateMutability":"payable","inputs":[{"name":"_destChainId","type":"uint256"},{"name":"_recipient","type":"address"},{"name":"_amount","type":"uint256"}],"outputs":[]},
            {
                "type":"function",
                "name":"initiate",
                "stateMutability":"payable",
                "inputs":[
                    {"name":"token","type":"address","internalType":"address"}, 
                    {"name":"amount","type":"uint256","internalType":"uint256"}, 
                    { 
                        "name":"instructions", 
                        "type":"tuple", 
                        "internalType":"struct Instructions",
                        "components":[
                            {"name":"sourceId","type":"uint256","internalType":"uint256"}, 
                            {"name":"receiver","type":"address","internalType":"address"}, 
                            {"name":"payableReceiver","type":"bool","internalType":"bool"}, 
                            {"name":"rollbackReceiver","type":"address","internalType":"address"}, 
                            {"name":"rollbackTeleporterFee","type":"uint256","internalType":"uint256"}, 
                            {"name":"rollbackGasLimit","type":"uint256","internalType":"uint256"}, 
                            {
                                "name":"hops",
                                "type":"tuple[]",
                                "internalType":"struct Hop[]",
                                "components":[
                                    {"name":"action","type":"uint8","internalType":"enum Action"}, 
                                    {"name":"requiredGasLimit","type":"uint256","internalType":"uint256"}, 
                                    {"name":"recipientGasLimit","type":"uint256","internalType":"uint256"}, 
                                    {"name":"trade","type":"bytes","internalType":"bytes"}, 
                                    {
                                        "name":"bridgePath",
                                        "type":"tuple",
                                        "internalType":"struct BridgePath",
                                        "components":[
                                            {"name":"bridgeSourceChain","type":"address","internalType":"address"},
                                            {"name":"sourceBridgeIsNative","type":"bool","internalType":"bool"},
                                            {"name":"bridgeDestinationChain","type":"address","internalType":"address"},
                                            {"name":"cellDestinationChain","type":"address","internalType":"address"},
                                            {"name":"destinationBlockchainID","type":"bytes32","internalType":"bytes32"},
                                            {"name":"teleporterFee","type":"uint256","internalType":"uint256"},
                                            {"name":"secondaryTeleporterFee","type":"uint256","internalType":"uint256"}
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "outputs":[]
            }
        ]''')

        self.kite_swap_amount = 0
        self.usdt_swap_amount = 0
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.config_file = "config.json"
        self.rotate_proxy = False

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def parse_proxy(self, proxy_str):
        """Parse proxy string to extract scheme, host, port, username, and password."""
        proxy_regex = r'^(?:(socks[45]|http|https)://)?(?:([^:]+):([^@]+)@)?([^:]+):(\d+)$'
        match = re.match(proxy_regex, proxy_str)
        if not match:
            proxy_str = f"http://{proxy_str}"  
            match = re.match(proxy_regex, proxy_str)
        if match:
            scheme, username, password, host, port = match.groups()
            return {
                "scheme": scheme or "http",
                "host": host,
                "port": int(port),
                "username": username,
                "password": password
            }
        raise ValueError(f"Invalid proxy format: {proxy_str}")

    async def load_proxies(self, use_proxy_choice: int):
        filename = "proxy.txt"
        try:
            if use_proxy_choice == 1:
                response = requests.get("https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies/all.txt", timeout=30)
                response.raise_for_status()
                content = response.text
                with open(filename, 'w') as f:
                    f.write(content)
                self.proxies = [line.strip() for line in content.splitlines() if line.strip()]
            else:
                if not os.path.exists(filename):
                    self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                    return
                with open(filename, 'r') as f:
                    self.proxies = [line.strip() for line in f.read().splitlines() if line.strip()]

            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}No Proxies Found.{Style.RESET_ALL}")
                return

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Proxies Total: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(self.proxies)}{Style.RESET_ALL}"
            )

        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def get_next_proxy_for_account(self, account):
        if account not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.proxies[self.proxy_index]
            self.account_proxies[account] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[account]

    def rotate_proxy_for_account(self, account):
        if not self.proxies:
            return None
        proxy = self.proxies[self.proxy_index]
        self.account_proxies[account] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy

    def get_proxy_settings(self):
        while True:
            try:
                print(f"{Fore.WHITE + Style.BRIGHT}1. Run With Proxyscrape Free Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Run With Private Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}3. Run Without Proxy{Style.RESET_ALL}")
                choose = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2/3] -> {Style.RESET_ALL}").strip())

                if choose in [1, 2, 3]:
                    proxy_type = (
                        "With Proxyscrape Free" if choose == 1 else
                        "With Private" if choose == 2 else
                        "Without"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}Run {proxy_type} Proxy Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")

        rotate = False
        if choose in [1, 2]:
            while True:
                rotate = input(f"{Fore.BLUE + Style.BRIGHT}Rotate Invalid Proxy? [y/n] -> {Style.RESET_ALL}").strip()
                if rotate in ["y", "n"]:
                    rotate = rotate == "y"
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter 'y' or 'n'.{Style.RESET_ALL}")

        return choose, rotate

    async def get_web3_with_check(self, address: str, rpc_url: str, use_proxy: bool, retries=3, timeout=60):
        for attempt in range(retries):
            try:
                proxy = self.get_next_proxy_for_account(address) if use_proxy else None
                session = None

                if use_proxy and proxy:
                    proxy_info = self.parse_proxy(proxy)
                    scheme = proxy_info["scheme"].lower()
                    self.log(f"{Fore.CYAN + Style.BRIGHT}Using proxy: {proxy} (Scheme: {scheme}){Style.RESET_ALL}")
                    proxy_url = f"{scheme}://{proxy_info['host']}:{proxy_info['port']}"
                    if proxy_info["username"] and proxy_info["password"]:
                        proxy_url = f"{scheme}://{proxy_info['username']}:{proxy_info['password']}@{proxy_info['host']}:{proxy_info['port']}"
                    session = requests.Session()
                    session.proxies = {
                        "http": proxy_url if scheme in ["http", "socks4", "socks5"] else None,
                        "https": proxy_url if scheme in ["https", "socks4", "socks5"] else None
                    }
                    session.timeout = timeout
                else:
                    self.log(f"{Fore.CYAN + Style.BRIGHT}Using direct connection (no proxy){Style.RESET_ALL}")
                    session = requests.Session()
                    session.timeout = timeout

                web3 = Web3(Web3.HTTPProvider(rpc_url, session=session))
                await asyncio.to_thread(web3.eth.get_block_number)
                self.log(f"{Fore.GREEN + Style.BRIGHT}Successfully connected to RPC{' via proxy' if use_proxy else ''}{Style.RESET_ALL}")
                return web3
            except Exception as e:
                self.log(f"{Fore.RED + Style.BRIGHT}RPC Connection Attempt {attempt + 1}/{retries} Failed: {str(e)}{Style.RESET_ALL}")
                if use_proxy and self.rotate_proxy:
                    self.rotate_proxy_for_account(address)
                if attempt < retries - 1:
                    await asyncio.sleep(3)
                    continue
                raise Exception(f"Failed to Connect to RPC: {str(e)}")
            finally:
                if session:
                    session.close()

    async def get_token_balance(self, address: str, contract_address: str, token_type: str, use_proxy: bool = True):
        try:
            web3 = await self.get_web3_with_check(address, self.KITE_AI["rpc_url"], use_proxy=True)  # Use proxy
            if token_type == "native":
                balance = await asyncio.to_thread(web3.eth.get_balance, address)
                decimals = 18
            else:
                token_contract = web3.eth.contract(
                    address=web3.to_checksum_address(contract_address),
                    abi=self.ERC20_CONTRACT_ABI
                )
                balance = await asyncio.to_thread(token_contract.functions.balanceOf(address).call)
                decimals = await asyncio.to_thread(token_contract.functions.decimals().call)
            return balance / (10 ** decimals)
        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Balance Check Failed: {str(e)}{Style.RESET_ALL}")
            return None

    async def send_raw_transaction_with_retries(self, account, web3, tx, retries=5):
        for attempt in range(retries):
            try:
                signed_tx = web3.eth.account.sign_transaction(tx, account)
                raw_tx = await asyncio.to_thread(web3.eth.send_raw_transaction, signed_tx.raw_transaction)
                return web3.to_hex(raw_tx)
            except Exception as e:
                self.log(f"{Fore.RED+Style.BRIGHT}Transaction Attempt {attempt + 1}/{retries} Failed: {str(e)}{Style.RESET_ALL}")
                await asyncio.sleep(2 ** attempt)
        raise Exception("Transaction Failed After Retries")

    async def wait_for_receipt_with_retries(self, web3, tx_hash, retries=5):
        for attempt in range(retries):
            try:
                receipt = await asyncio.to_thread(web3.eth.wait_for_transaction_receipt, tx_hash, timeout=300)
                return receipt
            except Exception as e:
                self.log(f"{Fore.RED+Style.BRIGHT}Receipt Attempt {attempt + 1}/{retries} Failed: {str(e)}{Style.RESET_ALL}")
                await asyncio.sleep(2 ** attempt)
        raise Exception("Receipt Not Found After Retries")

    async def approving_token(self, account: str, address: str, spender_address: str, contract_address: str, amount_to_wei: int, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, self.KITE_AI["rpc_url"], use_proxy=True)  # Use proxy
            token_contract = web3.eth.contract(address=web3.to_checksum_address(contract_address), abi=self.ERC20_CONTRACT_ABI)
            allowance = await asyncio.to_thread(token_contract.functions.allowance(address, spender_address).call)
            if allowance < amount_to_wei:
                approve_data = token_contract.functions.approve(spender_address, amount_to_wei)
                estimated_gas = await asyncio.to_thread(approve_data.estimate_gas, {"from": address})
                max_priority_fee = web3.to_wei(0.001, "gwei")
                approve_tx = await asyncio.to_thread(approve_data.build_transaction, {
                    "from": address,
                    "gas": int(estimated_gas * 1.2),
                    "maxFeePerGas": max_priority_fee,
                    "maxPriorityFeePerGas": max_priority_fee,
                    "nonce": await asyncio.to_thread(web3.eth.get_transaction_count, address, "pending"),
                    "chainId": web3.eth.chain_id,
                })
                tx_hash = await self.send_raw_transaction_with_retries(account, web3, approve_tx)
                receipt = await self.wait_for_receipt_with_retries(web3, tx_hash)
                self.log(f"{Fore.GREEN+Style.BRIGHT}Approve Success: Block {receipt.blockNumber}, Tx {tx_hash}{Style.RESET_ALL}")
            return True
        except Exception as e:
            raise Exception(f"Approve Failed: {str(e)}")

    def build_instructions_data(self, address: str, swap_type: str, token_in: str, token_out: str):
        from eth_abi.abi import encode
        from eth_utils import to_hex
        try:
            payable_receiver = False if swap_type == "native to erc20" else True
            trade_hex = to_hex(
                encode(
                    ['uint8', 'uint8', 'uint256', 'uint256', 'address', 'address', 'address'],
                    [32, 96, 0, 0, '0x0000000000000000000000000000000000000002', token_in, token_out]
                )
            )
            return (
                1, address, payable_receiver, address, 0, 500000, [
                    (
                        3, 2620000, 2120000, trade_hex,
                        (
                            self.ZERO_CONTRACT_ADDRESS,
                            False,
                            self.ZERO_CONTRACT_ADDRESS,
                            self.SWAP_ROUTER_ADDRESS,
                            self.DEST_BLOCKCHAIN_ID,
                            0,
                            0
                        )
                    )
                ]
            )
        except Exception as e:
            raise Exception(f"Build Instructions Failed: {str(e)}")

    async def perform_swap(self, account: str, address: str, swap_type: str, token_in: str, token_out: str, amount: float, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, self.KITE_AI["rpc_url"], use_proxy=True)  
            amount_to_wei = web3.to_wei(amount, "ether")
            token_contract = web3.eth.contract(
                address=web3.to_checksum_address(self.SWAP_ROUTER_ADDRESS),
                abi=self.NATIVE_CONTRACT_ABI if swap_type == "native to erc20" else self.ERC20_CONTRACT_ABI
            )
            if swap_type == "erc20 to native":
                await self.approving_token(account, address, self.SWAP_ROUTER_ADDRESS, token_in, amount_to_wei, use_proxy=True)
            instructions = self.build_instructions_data(address, swap_type, token_in, token_out)
            token_address = self.ZERO_CONTRACT_ADDRESS if swap_type == "native to erc20" else token_in
            swap_data = token_contract.functions.initiate(token_address, amount_to_wei, instructions)
            max_priority_fee = web3.to_wei(0.001, "gwei")
            estimated_gas = await asyncio.to_thread(swap_data.estimate_gas, {"from": address, "value": amount_to_wei} if swap_type == "native to erc20" else {"from": address})
            swap_tx = await asyncio.to_thread(swap_data.build_transaction, {
                "from": address,
                "value": amount_to_wei if swap_type == "native to erc20" else 0,
                "gas": int(estimated_gas * 1.2),
                "maxFeePerGas": max_priority_fee,
                "maxPriorityFeePerGas": max_priority_fee,
                "nonce": await asyncio.to_thread(web3.eth.get_transaction_count, address, "pending"),
                "chainId": web3.eth.chain_id,
            })
            tx_hash = await self.send_raw_transaction_with_retries(account, web3, swap_tx)
            receipt = await self.wait_for_receipt_with_retries(web3, tx_hash)
            return tx_hash, receipt.blockNumber
        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Swap Failed: {str(e)}{Style.RESET_ALL}")
            return None, None

    async def process_swap(self, account: str, address: str, swap_count: int, use_proxy: bool):
        self.log(f"{Fore.CYAN+Style.BRIGHT}Swap      :{Style.RESET_ALL}")
        for i in range(swap_count):
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}   ● {Style.RESET_ALL}"
                f"{Fore.GREEN+Style.BRIGHT}Swap {i+1}/{swap_count}{Style.RESET_ALL}"
            )
            swap_type = "native to erc20"
            option = "KITE to USDT"
            token_in = self.WKITE_CONTRACT_ADDRESS
            token_out = self.USDT_CONTRACT_ADDRESS
            ticker = "KITE"
            token_type = "native"
            amount = self.kite_swap_amount
            
            balance = await self.get_token_balance(address, token_in, token_type, use_proxy=True)  
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Pair    :{Style.RESET_ALL}"
                f"{Fore.BLUE+Style.BRIGHT} {option}{Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Balance :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {balance} {ticker}{Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Amount  :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {amount} {ticker}{Style.RESET_ALL}"
            )
            if not balance or balance <= amount:
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}     Status  :{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} Insufficient {ticker} Balance{Style.RESET_ALL}"
                )
                continue
            tx_hash, block_number = await self.perform_swap(account, address, swap_type, token_in, token_out, amount, use_proxy=True)  # Use proxy
            if tx_hash and block_number:
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}     Status  :{Style.RESET_ALL}"
                    f"{Fore.GREEN+Style.BRIGHT} Success{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}     Block   :{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {block_number}{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}     Tx Hash :{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {tx_hash}{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}     Explorer:{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {self.KITE_AI['explorer']}{tx_hash}{Style.RESET_ALL}"
                )
            await asyncio.sleep(random.randint(5, 10))

    async def run_swaps(self, kite_swap_amount: float, swap_count: int, use_proxy: bool):
        try:
            with open('accounts.txt', 'r') as file:
                accounts = [line.strip() for line in file if line.strip()]
            self.kite_swap_amount = kite_swap_amount
            for account in accounts:
                address = Account.from_key(account).address
                self.log(f"{Fore.CYAN+Style.BRIGHT}===== [{address[:6]}...{address[-6:]}] ====={Style.RESET_ALL}")
                await self.process_swap(account, address, swap_count, use_proxy)
        except FileNotFoundError:
            self.log(f"{Fore.RED+Style.BRIGHT}File 'accounts.txt' Not Found{Style.RESET_ALL}")
        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {str(e)}{Style.RESET_ALL}")

    def save_config(self, kite_swap_amount: float, swap_count: int):
        config = {
            "kite_swap_amount": kite_swap_amount,
            "swap_count": swap_count
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
        self.log(f"{Fore.GREEN+Style.BRIGHT}Configuration saved to {self.config_file}{Style.RESET_ALL}")

    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                return config.get("kite_swap_amount", 0), config.get("swap_count", 0)
        except FileNotFoundError:
            return 0, 0
        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error loading config: {str(e)}{Style.RESET_ALL}")
            return 0, 0

    def format_time_remaining(self, seconds):
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    async def main(self):
        try:
            self.log(f"{Fore.YELLOW+Style.BRIGHT}===== KiteAi_Swap - Tesseract Bot =====(Bamar Airdrop Group){Style.RESET_ALL}")

            use_proxy_choice, self.rotate_proxy = self.get_proxy_settings()
            if use_proxy_choice in [1, 2]:
                await self.load_proxies(use_proxy_choice)
            use_proxy = use_proxy_choice in [1, 2]

            kite_swap_amount, swap_count = self.load_config()
            if kite_swap_amount == 0 or swap_count == 0:
                self.log(f"{Fore.YELLOW+Style.BRIGHT}===== Bamar Airdrop Group ====={Style.RESET_ALL}")
                kite_swap_amount = float(input(f"{Fore.YELLOW + Style.BRIGHT}Enter KITE Swap Amount? -> {Style.RESET_ALL}"))
                swap_count = int(input(f"{Fore.YELLOW + Style.BRIGHT}Swap Transaction Count? -> {Style.RESET_ALL}"))
                self.save_config(kite_swap_amount, swap_count)
            else:
                self.log(f"{Fore.GREEN+Style.BRIGHT}Loaded config: KITE Amount = {kite_swap_amount}, Swap Count = {swap_count}{Style.RESET_ALL}")

            while True:
                await self.run_swaps(kite_swap_amount, swap_count, use_proxy)
                next_run = datetime.now(wib) + timedelta(hours=24)
                self.log(f"{Fore.CYAN+Style.BRIGHT}Next run scheduled at {next_run.strftime('%x %X %Z')}{Style.RESET_ALL}")
                while datetime.now(wib) < next_run:
                    time_remaining = (next_run - datetime.now(wib)).total_seconds()
                    self.log(f"{Fore.CYAN+Style.BRIGHT}Time until next run: {self.format_time_remaining(time_remaining)}{Style.RESET_ALL}")
                    await asyncio.sleep(60)
        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error in main: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    bot = KiteAi()
    asyncio.run(bot.main())
