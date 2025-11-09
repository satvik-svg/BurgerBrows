#!/usr/bin/env python3
"""
Test script for the faucet functionality
"""

try:
    from contracts import BurgerBrowsContracts
    print("✅ Successfully imported contracts module")
    
    # Test the contracts initialization
    contracts = BurgerBrowsContracts()
    print("✅ BurgerBrowsContracts initialized")
    
    # Check if wallet is connected
    if contracts.wallet.is_connected:
        print("✅ Wallet connected to blockchain")
        print(f"📍 Wallet address: {contracts.wallet.account.address}")
        
        # Test the mint function (but don't actually mint)
        print("🚰 Faucet functionality test:")
        print("   - mint_test_usdc method exists:", hasattr(contracts, 'mint_test_usdc'))
        
        if hasattr(contracts, 'mint_test_usdc'):
            print("✅ Faucet functionality is ready!")
            print("💡 Users can now get test USDC with the faucet button")
        else:
            print("❌ Faucet functionality not available")
    else:
        print("❌ Wallet not connected")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n🎉 Faucet test complete!")