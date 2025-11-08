#!/usr/bin/env python3
"""
🔗 BurgerBrows Contract Integration
Real smart contract interactions with deployed contracts
"""

import json
from wallet import BurgerBrowsWallet

class BurgerBrowsContracts:
    def __init__(self):
        # Load deployed contract configuration
        with open('config.json', 'r') as f:
            self.config = json.load(f)
        
        # Initialize wallet
        self.wallet = BurgerBrowsWallet(use_hackathon_wallet=True)
        
        # Contract addresses
        self.usdc_address = self.config['contracts']['MockUSDC']['address']
        self.vault_address = self.config['contracts']['BrowserVault']['address']
        self.pool_address = self.config['contracts']['RewardPool']['address']
        
        print(f"🔗 Contract integration initialized")
        print(f"💰 MockUSDC: {self.usdc_address}")
        print(f"🏦 BrowserVault: {self.vault_address}")
        print(f"🎁 RewardPool: {self.pool_address}")

    def get_usdc_balance(self) -> float:
        """Get USDC balance for current wallet"""
        return self.wallet.get_token_balance(self.usdc_address)
    
    def get_eth_balance(self) -> float:
        """Get ETH balance for current wallet"""
        return self.wallet.get_eth_balance()
    
    def test_contract_connections(self):
        """Test all contract connections and balances"""
        print("\n🧪 Testing Contract Connections...")
        print("-" * 50)
        
        # Test wallet
        if self.wallet.is_connected and self.wallet.account:
            print(f"✅ Wallet: {self.wallet.account.address}")
            print(f"💰 ETH Balance: {self.get_eth_balance():.6f} ETH")
            print(f"💵 USDC Balance: {self.get_usdc_balance():.2f} mUSDC")
        else:
            print("❌ Wallet not connected")
        
        # Test contract addresses
        contracts = [
            ("MockUSDC", self.usdc_address),
            ("BrowserVault", self.vault_address),
            ("RewardPool", self.pool_address)
        ]
        
        for name, address in contracts:
            if self.wallet.w3 and self.wallet.w3.is_connected():
                try:
                    code = self.wallet.w3.eth.get_code(address)
                    if len(code) > 0:
                        print(f"✅ {name} contract exists at {address}")
                    else:
                        print(f"❌ {name} contract not found at {address}")
                except Exception as e:
                    print(f"❌ Error checking {name}: {e}")
        
        return True

    def mint_test_usdc(self, amount: float = 1000) -> str:
        """Mint test USDC tokens (if we're the owner)"""
        if not self.wallet.is_connected or not self.wallet.account:
            return None
        
        try:
            # MockUSDC mint function ABI
            mint_abi = [
                {
                    "inputs": [
                        {"name": "to", "type": "address"},
                        {"name": "amount", "type": "uint256"}
                    ],
                    "name": "mint",
                    "outputs": [],
                    "stateMutability": "nonpayable",
                    "type": "function"
                }
            ]
            
            # Calculate amount with 6 decimals (USDC standard)
            amount_with_decimals = int(amount * 10**6)
            
            print(f"🪙 Minting {amount} mUSDC...")
            tx_hash = self.wallet.call_contract_function(
                self.usdc_address,
                mint_abi,
                "mint",
                [self.wallet.account.address, amount_with_decimals]
            )
            
            if tx_hash:
                receipt = self.wallet.wait_for_transaction(tx_hash)
                if receipt and receipt.get('status') == 1:
                    print(f"✅ Successfully minted {amount} mUSDC")
                    return tx_hash
            
            return None
            
        except Exception as e:
            print(f"❌ Error minting USDC: {e}")
            return None

if __name__ == "__main__":
    # Test the contract integration
    contracts = BurgerBrowsContracts()
    contracts.test_contract_connections()
    
    # Try to mint some test USDC
    if contracts.wallet.is_connected:
        print("\n🪙 Testing USDC minting...")
        contracts.mint_test_usdc(100)
        
        print(f"\n📊 Final balances:")
        print(f"💰 ETH: {contracts.get_eth_balance():.6f}")
        print(f"💵 USDC: {contracts.get_usdc_balance():.2f}")