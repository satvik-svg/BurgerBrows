#!/usr/bin/env python3
"""
🔗 BurgerBrows Web3 Wallet Module
Real blockchain connectivity for Sepolia testnet
"""

import json
import secrets
from web3 import Web3
from eth_account import Account
from typing import Optional, Dict, Any

class BurgerBrowsWallet:
    def __init__(self, use_hackathon_wallet: bool = True):
        # Sepolia testnet RPC endpoints
        self.rpc_urls = [
            "https://eth-sepolia.g.alchemy.com/v2/wvPB7N5GFQnyBB2FRL9L9",  # Your Alchemy endpoint
            "https://rpc.sepolia.org",  # Backup public RPC
            "https://ethereum-sepolia.blockpi.network/v1/rpc/public"  # Additional backup
        ]
        
        self.w3 = None
        self.account = None
        self.chain_id = 11155111  # Sepolia testnet
        
        # Hackathon wallet credentials
        self.hackathon_private_key = "0x05b40792c4a08ab87063e304a619f586921473c6bd74834e322a9fc202951eec"
        self.hackathon_address = "0x1f95Fe3186aCc2BcA155D239Be36dD2B8Fb6e795"
        
        # Initialize connection
        self.connect_to_network()
        
        # Initialize wallet
        if use_hackathon_wallet:
            self.init_hackathon_wallet()
        
        print(f"🔗 Web3 wallet initialized")
        print(f"📡 Connected to Sepolia testnet: {self.is_connected}")

    def init_hackathon_wallet(self):
        """Initialize with hackathon wallet for testing"""
        try:
            success = self.import_wallet(self.hackathon_private_key)
            if success:
                print(f"🎯 Hackathon wallet loaded: {self.account.address}")
                print(f"✅ Expected address: {self.hackathon_address}")
                if self.account.address.lower() == self.hackathon_address.lower():
                    print("🎉 Address verification successful!")
                else:
                    print("⚠️  Address mismatch - check private key")
            else:
                print("❌ Failed to load hackathon wallet")
        except Exception as e:
            print(f"❌ Error loading hackathon wallet: {e}")

    def connect_to_network(self) -> bool:
        """Connect to Sepolia testnet using available RPC endpoints"""
        for rpc_url in self.rpc_urls:
            try:
                print(f"🔄 Trying to connect to {rpc_url}...")
                
                # Create provider with timeout
                provider = Web3.HTTPProvider(rpc_url, request_kwargs={'timeout': 10})
                self.w3 = Web3(provider)
                
                # Test connection with timeout
                if self.w3.is_connected():
                    try:
                        latest_block = self.w3.eth.block_number
                        print(f"✅ Connected to Sepolia via {rpc_url}")
                        print(f"📊 Latest block: {latest_block}")
                        return True
                    except Exception as block_error:
                        print(f"⚠️  Connected but can't get block number: {block_error}")
                        # Still consider this a successful connection
                        return True
                else:
                    print(f"❌ No connection to {rpc_url}")
                    
            except Exception as e:
                print(f"❌ Failed to connect via {rpc_url}: {str(e)[:100]}...")
                continue
        
        print("❌ Could not connect to any Sepolia RPC endpoint")
        print("💡 Using offline mode - wallet functions will be limited")
        return False

    @property
    def is_connected(self) -> bool:
        """Check if connected to blockchain"""
        return self.w3 is not None and self.w3.is_connected()

    def create_new_wallet(self) -> Dict[str, str]:
        """Create a new wallet with private key and address"""
        try:
            # Generate secure random private key
            private_key = secrets.token_hex(32)
            
            # Create account from private key
            self.account = Account.from_key(private_key)
            
            wallet_data = {
                'address': self.account.address,
                'private_key': private_key,
                'public_key': self.account.public_key.hex() if hasattr(self.account.public_key, 'hex') else str(self.account.public_key)
            }
            
            print(f"🆕 New wallet created: {self.account.address}")
            return wallet_data
            
        except Exception as e:
            print(f"❌ Error creating wallet: {e}")
            return {}

    def import_wallet(self, private_key: str) -> bool:
        """Import existing wallet from private key"""
        try:
            # Remove 0x prefix if present
            if private_key.startswith('0x'):
                private_key = private_key[2:]
            
            # Validate private key format
            if len(private_key) != 64:
                print("❌ Invalid private key length")
                return False
            
            # Create account
            self.account = Account.from_key(private_key)
            print(f"📥 Wallet imported: {self.account.address}")
            return True
            
        except Exception as e:
            print(f"❌ Error importing wallet: {e}")
            return False

    def get_eth_balance(self, address: str = None) -> float:
        """Get ETH balance for address"""
        if not self.is_connected:
            return 0.0
        
        try:
            addr = address or (self.account.address if self.account else None)
            if not addr:
                return 0.0
            
            balance_wei = self.w3.eth.get_balance(addr)
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            return float(balance_eth)
            
        except Exception as e:
            print(f"❌ Error getting ETH balance: {e}")
            return 0.0

    def get_token_balance(self, token_address: str, holder_address: str = None) -> float:
        """Get ERC20 token balance (USDC, etc.)"""
        if not self.is_connected or not self.account:
            return 0.0
        
        try:
            # Standard ERC20 ABI for balanceOf function
            erc20_abi = [
                {
                    "constant": True,
                    "inputs": [{"name": "_owner", "type": "address"}],
                    "name": "balanceOf",
                    "outputs": [{"name": "balance", "type": "uint256"}],
                    "type": "function"
                },
                {
                    "constant": True,
                    "inputs": [],
                    "name": "decimals",
                    "outputs": [{"name": "", "type": "uint8"}],
                    "type": "function"
                }
            ]
            
            # Create contract instance
            contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(token_address),
                abi=erc20_abi
            )
            
            addr = holder_address or self.account.address
            
            # Get balance and decimals
            balance_raw = contract.functions.balanceOf(addr).call()
            decimals = contract.functions.decimals().call()
            
            # Convert to human readable format
            balance = balance_raw / (10 ** decimals)
            return float(balance)
            
        except Exception as e:
            print(f"❌ Error getting token balance: {e}")
            return 0.0

    def send_transaction(self, to_address: str, value_eth: float, gas_limit: int = 21000) -> Optional[str]:
        """Send ETH transaction"""
        if not self.is_connected or not self.account:
            print("❌ Wallet not connected or no account")
            return None
        
        try:
            # Get current gas price
            gas_price = self.w3.eth.gas_price
            
            # Get nonce
            nonce = self.w3.eth.get_transaction_count(self.account.address)
            
            # Build transaction
            transaction = {
                'to': Web3.to_checksum_address(to_address),
                'value': self.w3.to_wei(value_eth, 'ether'),
                'gas': gas_limit,
                'gasPrice': gas_price,
                'nonce': nonce,
                'chainId': self.chain_id
            }
            
            # Sign transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
            
            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            print(f"📤 Transaction sent: {tx_hash.hex()}")
            return tx_hash.hex()
            
        except Exception as e:
            print(f"❌ Error sending transaction: {e}")
            return None

    def call_contract_function(self, contract_address: str, abi: list, function_name: str, 
                             args: list = None, value_eth: float = 0) -> Optional[str]:
        """Call a smart contract function (for transactions)"""
        if not self.is_connected or not self.account:
            print("❌ Wallet not connected or no account")
            return None
        
        try:
            # Create contract instance
            contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(contract_address),
                abi=abi
            )
            
            # Get function
            func = getattr(contract.functions, function_name)
            
            # Get current gas price and add buffer for quick succession transactions
            current_gas_price = self.w3.eth.gas_price
            buffered_gas_price = int(current_gas_price * 1.2)  # 20% higher gas price
            
            # Get latest nonce (including pending transactions)
            nonce = self.w3.eth.get_transaction_count(self.account.address, 'pending')
            
            # Prepare function call
            if args:
                transaction = func(*args).build_transaction({
                    'from': self.account.address,
                    'value': self.w3.to_wei(value_eth, 'ether'),
                    'gas': 300000,  # Higher gas limit for complex contracts
                    'gasPrice': buffered_gas_price,
                    'nonce': nonce,
                    'chainId': self.chain_id
                })
            else:
                transaction = func().build_transaction({
                    'from': self.account.address,
                    'value': self.w3.to_wei(value_eth, 'ether'),
                    'gas': 300000,
                    'gasPrice': buffered_gas_price,
                    'nonce': nonce,
                    'chainId': self.chain_id
                })
            
            # Sign and send transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            print(f"📤 Contract function called: {tx_hash.hex()}")
            return tx_hash.hex()
            
        except Exception as e:
            print(f"❌ Error calling contract function: {e}")
            return None

    def call_view_function(self, contract_address: str, abi: list, function_name: str, 
                          args: list = None):
        """Call a smart contract view function (read-only)"""
        if not self.is_connected:
            print("❌ Wallet not connected")
            return None
        
        try:
            # Create contract instance
            contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(contract_address),
                abi=abi
            )
            
            # Get function
            func = getattr(contract.functions, function_name)
            
            # Call function (no transaction needed)
            if args:
                result = func(*args).call()
            else:
                result = func().call()
            
            return result
            
        except Exception as e:
            print(f"❌ Error calling view function: {e}")
            return None

    def wait_for_transaction(self, tx_hash: str, timeout: int = 120) -> Optional[Dict[str, Any]]:
        """Wait for transaction confirmation"""
        if not self.is_connected:
            return None
        
        try:
            print(f"⏳ Waiting for transaction {tx_hash}...")
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=timeout)
            
            if receipt.status == 1:
                print(f"✅ Transaction confirmed in block {receipt.blockNumber}")
            else:
                print(f"❌ Transaction failed")
            
            return dict(receipt)
            
        except Exception as e:
            print(f"❌ Error waiting for transaction: {e}")
            return None

    def get_wallet_info(self) -> Dict[str, Any]:
        """Get current wallet information"""
        if not self.account:
            return {}
        
        return {
            'address': self.account.address,
            'eth_balance': self.get_eth_balance(),
            'connected': self.is_connected,
            'chain_id': self.chain_id,
            'network': 'Sepolia Testnet'
        }

    def save_wallet_to_file(self, filename: str, password: str) -> bool:
        """Save encrypted wallet to file"""
        if not self.account:
            print("❌ No wallet to save")
            return False
        
        try:
            # Create encrypted keystore
            encrypted = Account.encrypt(self.account.key, password)
            
            with open(filename, 'w') as f:
                json.dump(encrypted, f, indent=2)
            
            print(f"💾 Wallet saved to {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving wallet: {e}")
            return False

    def load_wallet_from_file(self, filename: str, password: str) -> bool:
        """Load encrypted wallet from file"""
        try:
            with open(filename, 'r') as f:
                encrypted = json.load(f)
            
            # Decrypt keystore
            private_key = Account.decrypt(encrypted, password)
            
            # Import the wallet
            return self.import_wallet(private_key.hex())
            
        except Exception as e:
            print(f"❌ Error loading wallet: {e}")
            return False


# Demo/Testing functions
def demo_wallet():
    """Demo wallet functionality"""
    print("\n🍔 BurgerBrows Web3 Wallet Demo")
    print("="*40)
    
    # Create wallet instance
    print("🚀 Initializing Web3 wallet...")
    wallet = BurgerBrowsWallet()
    
    # Create new wallet (works offline too)
    print("\n🔐 Creating new wallet...")
    wallet_data = wallet.create_new_wallet()
    
    if wallet_data:
        print(f"✅ Wallet created successfully!")
        print(f"🔑 Address: {wallet_data['address']}")
        print(f"�️  Private Key: {wallet_data['private_key'][:20]}...{wallet_data['private_key'][-20:]}")
        
        if wallet.is_connected:
            print(f"\n💰 Checking balances...")
            eth_balance = wallet.get_eth_balance()
            print(f"💰 ETH Balance: {eth_balance:.6f} ETH")
            
            # Test token balance (Sepolia USDC if available)
            test_usdc_address = "0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238"  # Sepolia USDC
            print(f"💵 Checking USDC balance...")
            usdc_balance = wallet.get_token_balance(test_usdc_address)
            print(f"💵 USDC Balance: {usdc_balance:.2f} USDC")
        else:
            print(f"\n⚠️  Offline mode - cannot check balances")
            print(f"💡 Wallet created but blockchain connection failed")
    else:
        print("❌ Failed to create wallet")
    
    # Display wallet info
    print(f"\n📊 Wallet Info:")
    wallet_info = wallet.get_wallet_info()
    for key, value in wallet_info.items():
        print(f"   {key}: {value}")
    
    print("="*40)
    print("🍔 Demo completed!")
    return wallet


if __name__ == "__main__":
    # Run demo
    demo_wallet()