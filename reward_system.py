#!/usr/bin/env python3
"""
Fix the reward system by giving direct USDC transfers as rewards
Since the RewardPool contract yields are too small, we'll use direct transfers
"""

from rewards import RewardPoolManager
from wallet import BurgerBrowsWallet

class FixedRewardManager:
    """Enhanced reward manager with meaningful rewards"""
    
    def __init__(self):
        self.wallet = BurgerBrowsWallet()
        self.contracts_config = None
        self.load_contracts_config()
        
    def load_contracts_config(self):
        """Load contract configuration"""
        import json
        try:
            with open('config.json', 'r') as f:
                self.contracts_config = json.load(f)
        except FileNotFoundError:
            print("❌ No deployed contracts found")
    
    def claim_meaningful_reward(self, user_address, activity_score=100):
        """Give user a meaningful USDC reward based on activity"""
        try:
            print(f"🎁 Claiming meaningful reward for: {user_address}")
            print(f"📊 Activity Score: {activity_score}")
            
            # Calculate reward: 10 USDC base + (activity_score / 10) USDC
            base_reward = 10.0  # 10 USDC base
            activity_bonus = activity_score / 10.0  # 0.1 USDC per activity point
            total_reward = base_reward + activity_bonus
            
            print(f"💰 Calculated reward: {total_reward} USDC")
            
            # Transfer USDC directly from hackathon wallet
            usdc_address = self.contracts_config['contracts']['MockUSDC']['address']
            
            # ERC20 transfer ABI
            transfer_abi = [{
                "inputs": [
                    {"name": "to", "type": "address"},
                    {"name": "amount", "type": "uint256"}
                ],
                "name": "transfer",
                "outputs": [{"name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function"
            }]
            
            amount_with_decimals = int(total_reward * 10**6)  # USDC has 6 decimals
            
            tx_hash = self.wallet.call_contract_function(
                usdc_address,
                transfer_abi,
                "transfer",
                [user_address, amount_with_decimals]
            )
            
            if tx_hash:
                print(f"✅ Meaningful reward sent: {total_reward} USDC")
                print(f"🔗 Transaction: {tx_hash}")
                print(f"🔗 View: https://sepolia.etherscan.io/tx/{tx_hash}")
                return tx_hash
            else:
                print("❌ Reward transfer failed")
                return None
                
        except Exception as e:
            print(f"❌ Error sending reward: {e}")
            return None

if __name__ == "__main__":
    print("🎁 Testing Fixed Reward System...")
    
    manager = FixedRewardManager()
    if manager.wallet.is_connected:
        # Test reward for user wallet
        user_wallet = "0x3d01D6ceD68aaD92c58aE0A09437687daF918c6d"
        result = manager.claim_meaningful_reward(user_wallet, 100)
        
        if result:
            print(f"\n✅ SUCCESS! User will receive meaningful rewards!")
        else:
            print(f"\n❌ Failed to send reward")
    else:
        print("❌ Wallet not connected")