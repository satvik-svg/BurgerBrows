# 🍔 BurgerBrows - Multi-User DeFi Browser

A secure, multi-user decentralized finance browser that creates unique wallets for each user and enables real blockchain transactions.

## 🚀 Features

- **🔐 Unique Wallet Generation**: Each device gets a cryptographically secure, unique wallet
- **💰 Real DeFi Operations**: Deposit, yield farming, and reward claiming on Sepolia testnet
- **🌐 Multi-User Isolation**: Complete user separation with device-based identification
- **⚡ Real Blockchain Integration**: All transactions hit the actual Sepolia blockchain

## 📁 Project Structure

```
BurgerBrows/
├── browser.py                       # Main application (PyQt6 GUI)
├── wallet.py                        # Web3 wallet integration
├── contracts.py                     # Smart contract interactions
├── rewards.py                       # Reward pool management
├── reward_system.py                 # Enhanced reward system
├── config.json                      # Contract addresses on Sepolia
├── contracts/                       # Smart contract source code
├── burgerbrows-env/                 # Python virtual environment
└── user_*.json                     # User wallet data (auto-generated)
```

## 🛠 Setup & Installation

1. **Clone and Setup**
   ```bash
   cd BurgerBrows
   source burgerbrows-env/bin/activate
   ```

2. **Run the Browser**
   ```bash
   python browser.py
   ```

## 👥 Multi-User System

- **Automatic Wallet Creation**: New users get unique wallets based on device fingerprint
- **Secure Key Management**: Private keys generated using cryptographically secure methods
- **Persistent User Data**: User wallets saved locally for return visits
- **Zero Hardcoded Data**: No predefined user addresses or keys

## 💰 DeFi Functions

### Deposit USDC
- Users deposit their own USDC to the BrowserVault
- Uses their own ETH for gas fees
- Real blockchain transactions with confirmations

### Check Balance  
- Real-time balance queries from Sepolia blockchain
- Shows actual USDC holdings in user's unique wallet

### Claim Rewards
- Users receive 20 USDC rewards for activity
- Real USDC transfers to their unique wallet
- Immediate balance updates

## 🌐 Deployed Contracts (Sepolia)

- **MockUSDC**: `0xE32f7a8eB4Fb132675292306A5928071d126F082`
- **BrowserVault**: `0x9dAE42f31DB601fD0094c05d5b52Eb0a3074f786`  
- **RewardPool**: `0xc7Fd8EF7Ee3e93e8eff2E12715E504aDfbaE3750`

## 🔧 User Requirements

New users need:
- **ETH**: For gas fees (get from Sepolia faucet)
- **MockUSDC**: For deposits (can be minted or transferred)

## 🏆 Hackathon Ready

This project demonstrates:
- Real blockchain integration with Web3.py
- Secure multi-user wallet management
- Complete DeFi user experience
- Production-ready architecture

## 🔒 Security Features

- Unique wallet per device/user
- Cryptographically secure private key generation
- Local key storage (no central database)
- Real gas fee payments by users
- Isolated user experiences

---

**Built for hackathons, ready for production! 🚀**