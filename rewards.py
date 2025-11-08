#!/usr/bin/env python3
"""
Real RewardPool Integration for BurgerBrows
Implements actual USDC reward claims with blockchain transactions
"""

from contracts import BurgerBrowsContracts
import json
from datetime import datetime, timedelta

class RewardPoolManager:
    def __init__(self):
        self.contracts = BurgerBrowsContracts()
        self.reward_pool_abi = [
            {
                "inputs": [
                    {"name": "epochId", "type": "uint256"},
                    {"name": "userScore", "type": "uint256"},
                    {"name": "signature", "type": "bytes"}
                ],
                "name": "claimReward",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {"name": "epochId", "type": "uint256"},
                    {"name": "totalScore", "type": "uint256"}
                ],
                "name": "setEpochTotalScore", 
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"name": "epochId", "type": "uint256"}],
                "name": "getEpochInfo",
                "outputs": [
                    {"name": "yieldAmount", "type": "uint256"},
                    {"name": "totalScore", "type": "uint256"},
                    {"name": "scoreSet", "type": "bool"},
                    {"name": "remainingYield", "type": "uint256"}
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {"name": "epochId", "type": "uint256"},
                    {"name": "userScore", "type": "uint256"}
                ],
                "name": "calculateReward",
                "outputs": [{"name": "reward", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            }
        ]
        
    def set_epoch_total_score(self, epoch_id, total_score):
        """Admin function: Set total activity score for an epoch"""
        try:
            pool_addr = self.contracts.config['contracts']['RewardPool']['address']
            
            print(f"📝 Setting total score for epoch {epoch_id}: {total_score}")
            
            tx_hash = self.contracts.wallet.call_contract_function(
                pool_addr,
                self.reward_pool_abi,
                "setEpochTotalScore",
                [epoch_id, total_score]
            )
            
            if tx_hash:
                print(f"✅ Epoch total score set: {tx_hash}")
                print(f"🔗 View: https://sepolia.etherscan.io/tx/{tx_hash}")
                return tx_hash
            else:
                print(f"❌ Failed to set epoch score")
                return None
                
        except Exception as e:
            print(f"❌ Error setting epoch score: {e}")
            return None
    
    def get_epoch_info(self, epoch_id):
        """Get information about a specific epoch"""
        try:
            pool_addr = self.contracts.config['contracts']['RewardPool']['address']
            
            result = self.contracts.wallet.call_view_function(
                pool_addr,
                self.reward_pool_abi,
                "getEpochInfo",
                [epoch_id]
            )
            
            if result:
                return {
                    'yield_amount': int(result[0]) if result[0] else 0,
                    'total_score': int(result[1]) if result[1] else 0,
                    'score_set': bool(result[2]) if result[2] else False,
                    'remaining_yield': int(result[3]) if result[3] else 0
                }
            else:
                return None
                
        except Exception as e:
            print(f"❌ Error getting epoch info: {e}")
            return None
    
    def calculate_user_reward(self, epoch_id, user_score):
        """Calculate expected reward for user's score"""
        try:
            pool_addr = self.contracts.config['contracts']['RewardPool']['address']
            
            result = self.contracts.wallet.call_view_function(
                pool_addr,
                self.reward_pool_abi,
                "calculateReward",
                [epoch_id, user_score]
            )
            
            return int(result) if result else 0
                
        except Exception as e:
            print(f"❌ Error calculating reward: {e}")
            return 0
    
    def claim_reward_real(self, epoch_id, user_score, signature):
        """Real blockchain reward claim"""
        try:
            pool_addr = self.contracts.config['contracts']['RewardPool']['address']
            
            print(f"🎁 Claiming real USDC reward for epoch {epoch_id}")
            print(f"📊 Your activity score: {user_score}")
            
            # Convert signature to bytes if it's a hex string
            if isinstance(signature, str) and signature.startswith('0x'):
                signature_bytes = bytes.fromhex(signature[2:])
            else:
                signature_bytes = signature
            
            tx_hash = self.contracts.wallet.call_contract_function(
                pool_addr,
                self.reward_pool_abi,
                "claimReward",
                [epoch_id, user_score, signature_bytes]
            )
            
            if tx_hash:
                print(f"✅ Real reward claimed! TX: {tx_hash}")
                print(f"🔗 View: https://sepolia.etherscan.io/tx/{tx_hash}")
                return tx_hash
            else:
                print(f"❌ Reward claim failed")
                return None
                
        except Exception as e:
            print(f"❌ Error claiming reward: {e}")
            return None
    
    def claim_reward(self, user_address):
        """Simplified reward claiming for browser integration"""
        try:
            print(f"🎁 Claiming reward for user: {user_address}")
            
            # For now, use epoch 1 with default score
            epoch_id = 1
            user_score = 100  # Default activity score
            
            # Generate a simple signature (in real implementation, this would come from oracle)
            signature = "0x" + "00" * 65  # Dummy signature
            
            return self.claim_reward_real(epoch_id, user_score, signature)
            
        except Exception as e:
            print(f"❌ Error in claim_reward: {e}")
            return None

# Test the system
if __name__ == "__main__":
    print("🎁 Testing Real RewardPool Integration...")
    
    manager = RewardPoolManager()
    if manager.contracts.wallet.is_connected:
        # Test epoch info
        epoch_info = manager.get_epoch_info(1)
        if epoch_info:
            print(f"📊 Epoch 1 Info:")
            print(f"   Yield: {epoch_info['yield_amount']} USDC")
            print(f"   Total Score: {epoch_info['total_score']}")
            print(f"   Score Set: {epoch_info['score_set']}")
            print(f"   Remaining: {epoch_info['remaining_yield']} USDC")
        
        print(f"\n✅ RewardPool integration ready!")
        print(f"💡 Next: Integrate with browser for real claims")
    else:
        print("❌ Wallet not connected")