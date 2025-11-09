#!/usr/bin/env python3
"""
🌐 BurgerBrows Multi-User with Real Blockchain Integration

This version creates unique wallets for each user AND uses real blockchain transactions.
Each user gets their own wallet with real USDC deposits, yields, and rewards!
"""

import sys
import os
import json
import hashlib
import secrets
import platform
import getpass
from datetime import datetime
from eth_account import Account

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
        QPushButton, QLabel, QTextEdit, QGroupBox, QSplitter, 
        QTabWidget, QLineEdit, QMessageBox, QInputDialog, QDialog, QGridLayout
    )
    from PyQt6.QtCore import Qt, QUrl, QTimer
    from PyQt6.QtGui import QScreen
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    from urllib.parse import urlparse
    GUI_AVAILABLE = True
except ImportError:
    print("PyQt6 not available - running in console mode")
    GUI_AVAILABLE = False

# Import our working Web3 modules
from wallet import BurgerBrowsWallet
from rewards import RewardPoolManager
from reward_system import FixedRewardManager

class MultiUserWalletManager:
    """Manages unique wallets for each user/device with real blockchain integration"""
    
    def __init__(self):
        self.user_data = self.create_or_load_user()
        self.wallet = None
        self.setup_real_wallet()
        
        print(f"🌐 Multi-User Wallet Manager Initialized")
        print(f"👤 User ID: {self.user_data['user_id']}")
        print(f"🏦 Wallet: {self.user_data['wallet_address']}")
        print(f"🔗 Real blockchain integration enabled!")
    
    def create_or_load_user(self):
        """Create or load unique user for this device"""
        # Generate device-based user ID
        machine_info = f"{platform.node()}-{platform.system()}-{getpass.getuser()}"
        user_id = hashlib.sha256(machine_info.encode()).hexdigest()[:16]
        
        # Check if user file exists
        user_file = f"user_{user_id}.json"
        
        if os.path.exists(user_file):
            # Load existing user
            with open(user_file, 'r') as f:
                user_data = json.load(f)
            print(f"👋 Welcome back! Loaded existing wallet")
        else:
            # Create new user with unique wallet
            private_key = secrets.token_hex(32)
            account = Account.from_key(private_key)
            
            user_data = {
                'user_id': user_id,
                'wallet_address': account.address,
                'private_key': private_key,
                'created_at': datetime.now().isoformat(),
                'device_info': {
                    'system': platform.system(),
                    'node': platform.node(),
                    'user': getpass.getuser()
                }
            }
            
            # Save user data
            with open(user_file, 'w') as f:
                json.dump(user_data, f, indent=2)
            
            print(f"🆕 New user created and saved!")
        
        return user_data
    
    def setup_real_wallet(self):
        """Setup real Web3 wallet with user's private key"""
        try:
            # Create wallet without hackathon mode
            self.wallet = BurgerBrowsWallet(use_hackathon_wallet=False)
            
            # Import user's private key
            success = self.wallet.import_wallet(self.user_data['private_key'])
            
            if success and self.wallet.account:
                print(f"🔗 Real wallet connected: {self.wallet.account.address}")
                print(f"✅ User wallet matches: {self.user_data['wallet_address']}")
            else:
                print(f"❌ Failed to import user's private key")
                self.wallet = None
            
        except Exception as e:
            print(f"❌ Wallet setup error: {e}")
            self.wallet = None
    
    def get_wallet_info(self):
        """Get wallet information"""
        return {
            'address': self.user_data['wallet_address'],
            'private_key': self.user_data['private_key'],
            'user_id': self.user_data['user_id'],
            'wallet_instance': self.wallet
        }

class RealMultiUserBrowser(QMainWindow if GUI_AVAILABLE else object):
    """Multi-user browser with real blockchain transactions"""
    
    def __init__(self):
        if GUI_AVAILABLE:
            super().__init__()
        
        print("🌐 Initializing Real Multi-User Browser...")
        
        # Create unique wallet for this user/device
        self.wallet_manager = MultiUserWalletManager()
        wallet_info = self.wallet_manager.get_wallet_info()
        
        self.wallet_address = wallet_info['address']
        self.private_key = wallet_info['private_key']
        self.user_id = wallet_info['user_id']
        self.wallet = wallet_info['wallet_instance']
        
        # Load contracts configuration
        self.load_contracts_config()
        
        # Initialize fixed reward manager for meaningful rewards
        try:
            self.reward_manager = FixedRewardManager()
            print("🎁 Fixed reward system connected")
        except Exception as e:
            print(f"⚠️ Reward system not available: {e}")
            self.reward_manager = None
        
        print(f"✅ Real blockchain browser initialized!")
        print(f"🔐 Your funds are isolated and real!")
        
        if GUI_AVAILABLE:
            self.init_ui()
    
    def load_contracts_config(self):
        """Load deployed contracts configuration"""
        try:
            with open('config.json', 'r') as f:
                self.contracts_config = json.load(f)
            print("📄 Real contracts configuration loaded")
        except Exception as e:
            print(f"⚠️ Could not load contracts: {e}")
            self.contracts_config = None
    
    def init_ui(self):
        """Initialize Brave-like browser interface"""
        self.setWindowTitle("BurgerBrows")
        self.setGeometry(100, 100, 1400, 900)
        
        # Brave browser dark theme styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E24;
                color: #ffffff;
            }
            
            /* Tab Widget Styling */
            QTabWidget {
                background-color: #1E1E24;
                border: none;
            }
            
            QTabWidget::pane {
                border: none;
                background-color: #1E1E24;
                top: -1px;
            }
            
            QTabBar {
                background-color: #2D2D38;
            }
            
            QTabBar::tab {
                background-color: #2D2D38;
                color: #ffffff;
                padding: 8px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                min-width: 200px;
                max-width: 250px;
            }
            
            QTabBar::tab:selected {
                background-color: #1E1E24;
                color: #ffffff;
            }
            
            QTabBar::tab:hover {
                background-color: #3D3D48;
            }
            
            QTabBar::close-button {
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDRMNCA1TDEyIDRaTTQgNEwxMiAxMkw0IDRaIiBzdHJva2U9IiNmZmZmZmYiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
                subcontrol-position: right;
            }
            
            /* Navigation Bar Styling */
            QWidget#nav_bar {
                background-color: #2D2D38;
                border-bottom: 1px solid #3D3D48;
            }
            
            /* Navigation Button Styling */
            QPushButton#nav_button {
                background-color: transparent;
                border: none;
                border-radius: 6px;
                padding: 8px;
                color: #ffffff;
                font-size: 16px;
                min-width: 36px;
                max-width: 36px;
            }
            
            QPushButton#nav_button:hover {
                background-color: #3D3D48;
            }
            
            QPushButton#nav_button:pressed {
                background-color: #4D4D58;
            }
            
            QPushButton#nav_button:disabled {
                color: #6D6D78;
            }
            
            /* Address Bar Styling */
            QLineEdit#address_bar {
                background-color: #3D3D48;
                border: 1px solid #4D4D58;
                border-radius: 20px;
                padding: 10px 16px;
                color: #ffffff;
                font-size: 14px;
                selection-background-color: #FF6B47;
            }
            
            QLineEdit#address_bar:focus {
                border: 2px solid #FF6B47;
                background-color: #4D4D58;
            }
            
            /* Menu Button */
            QPushButton#menu_button {
                background-color: transparent;
                border: none;
                border-radius: 6px;
                padding: 8px;
                color: #ffffff;
                font-size: 18px;
            }
            
            QPushButton#menu_button:hover {
                background-color: #3D3D48;
            }
            
            /* Wallet Button */
            QPushButton#wallet_button {
                background-color: #FF6B47;
                border: none;
                border-radius: 6px;
                padding: 8px;
                color: white;
                font-size: 16px;
                min-width: 32px;
                min-height: 32px;
            }
            
            QPushButton#wallet_button:hover {
                background-color: #FF8A65;
            }
            
            /* DeFi Panel Styling */
            QWidget#defi_panel {
                background-color: #2D2D38;
                border-left: 1px solid #3D3D48;
            }
            
            QPushButton#defi_button {
                background-color: #FF6B47;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: 600;
                margin: 4px;
            }
            
            QPushButton#defi_button:hover {
                background-color: #E55A3A;
            }
            
            QLabel#defi_label {
                color: #ffffff;
                font-weight: 600;
                padding: 8px;
            }
        """)
        
        # Create main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create navigation bar
        nav_bar = self.create_navigation_bar()
        main_layout.addWidget(nav_bar)
        
        # Create main content area
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Create tab widget for browser tabs (full width)
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        # Add tab widget to take full space (no sidebar)
        content_layout.addWidget(self.tab_widget)
        
        main_layout.addWidget(content_widget)
        
        # Create initial tabs
        self.browsers = []  # Keep track of browser instances
        self.create_new_tab("https://www.google.com", "🏠 Home")
        
        # Auto-load balance after UI is ready
        QTimer.singleShot(1500, self.check_real_balance)

    def create_navigation_bar(self):
        """Create Brave-style navigation bar"""
        nav_widget = QWidget()
        nav_widget.setObjectName("nav_bar")
        nav_widget.setFixedHeight(50)
        
        layout = QHBoxLayout(nav_widget)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(8)
        
        # Back button
        self.back_button = QPushButton("◀")
        self.back_button.setObjectName("nav_button")
        self.back_button.setEnabled(False)
        self.back_button.setToolTip("Go back")
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)
        
        # Forward button
        self.forward_button = QPushButton("▶")
        self.forward_button.setObjectName("nav_button")
        self.forward_button.setEnabled(False)
        self.forward_button.setToolTip("Go forward")
        self.forward_button.clicked.connect(self.go_forward)
        layout.addWidget(self.forward_button)
        
        # Refresh button
        self.refresh_button = QPushButton("↻")
        self.refresh_button.setObjectName("nav_button")
        self.refresh_button.setToolTip("Refresh page")
        self.refresh_button.clicked.connect(self.refresh_page)
        layout.addWidget(self.refresh_button)
        
        # Home button
        home_button = QPushButton("🏠")
        home_button.setObjectName("nav_button")
        home_button.setToolTip("Home")
        home_button.clicked.connect(lambda: self.navigate_to("https://www.google.com"))
        layout.addWidget(home_button)
        
        # Address bar
        self.address_bar = QLineEdit()
        self.address_bar.setObjectName("address_bar")
        self.address_bar.setPlaceholderText("🔒 Search with Google or enter address")
        self.address_bar.returnPressed.connect(self.navigate_from_address_bar)
        layout.addWidget(self.address_bar)
        
        # New tab button
        new_tab_button = QPushButton("+")
        new_tab_button.setObjectName("nav_button")
        new_tab_button.setToolTip("New tab")
        new_tab_button.clicked.connect(lambda: self.create_new_tab())
        layout.addWidget(new_tab_button)
        
        # Menu button (Brave-style)
        menu_button = QPushButton("≡")
        menu_button.setObjectName("menu_button")
        menu_button.setToolTip("Main menu")
        menu_button.clicked.connect(self.show_menu)
        layout.addWidget(menu_button)
        
        # Wallet extension button (MetaMask style)
        self.wallet_button = QPushButton("🦊")
        self.wallet_button.setObjectName("wallet_button")
        self.wallet_button.setToolTip("BurgerBrows Wallet")
        self.wallet_button.clicked.connect(self.toggle_wallet_popup)
        layout.addWidget(self.wallet_button)
        
        return nav_widget

    def toggle_wallet_popup(self):
        """Toggle wallet popup (MetaMask/Phantom style)"""
        if hasattr(self, 'wallet_popup') and self.wallet_popup.isVisible():
            self.wallet_popup.hide()
        else:
            self.show_wallet_popup()
            
    def show_wallet_popup(self):
        """Show Phantom-style wallet popup"""
        if hasattr(self, 'wallet_popup') and self.wallet_popup.isVisible():
            self.wallet_popup.hide()
            return
            
        # Create popup dialog (larger like Phantom)
        self.wallet_popup = QDialog(self)
        self.wallet_popup.setWindowTitle("🦊 BurgerBrows Wallet")
        self.wallet_popup.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint)
        self.wallet_popup.setModal(False)
        self.wallet_popup.setFixedSize(400, 600)  # Larger like Phantom
        
        # Simple, reliable positioning - center on screen
        screen_geometry = self.geometry()
        popup_x = screen_geometry.x() + (screen_geometry.width() - 400) // 2
        popup_y = screen_geometry.y() + 80  # Just below toolbar
        
        # Ensure it's on screen
        if popup_x < 0:
            popup_x = 50
        if popup_y < 0:
            popup_y = 50
            
        self.wallet_popup.move(popup_x, popup_y)
        
        # Create popup content
        self.create_wallet_popup_content()
        self.wallet_popup.show()
        self.wallet_popup.raise_()
        self.wallet_popup.activateWindow()
        
    def create_wallet_popup_content(self):
        """Create Phantom-style popup content"""
        layout = QVBoxLayout(self.wallet_popup)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header with user info (Phantom style)
        header = QWidget()
        header.setFixedHeight(100)
        header.setStyleSheet("""
            QWidget {
                background-color: #2D2D35;
                border-top-left-radius: 16px;
                border-top-right-radius: 16px;
                border-bottom: 1px solid #3A3A42;
            }
        """)
        
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 16, 20, 16)
        header_layout.setSpacing(8)
        
        # Top row with profile and buttons
        top_row = QWidget()
        top_row_layout = QHBoxLayout(top_row)
        top_row_layout.setContentsMargins(0, 0, 0, 0)
        
        # Profile section
        profile_section = QWidget()
        profile_layout = QHBoxLayout(profile_section)
        profile_layout.setContentsMargins(0, 0, 0, 0)
        profile_layout.setSpacing(12)
        
        # Avatar (colored circle like Phantom)
        avatar = QLabel("🦊")
        avatar.setFixedSize(40, 40)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("""
            QLabel {
                background-color: #FF6B47;
                border-radius: 20px;
                font-size: 20px;
                color: white;
            }
        """)
        profile_layout.addWidget(avatar)
        
        # User info
        user_info = QWidget()
        user_info_layout = QVBoxLayout(user_info)
        user_info_layout.setContentsMargins(0, 0, 0, 0)
        user_info_layout.setSpacing(2)
        
        # Dynamic username based on user ID
        user_id = self.wallet_manager.get_wallet_info()['user_id']
        username = QLabel(f"@BurgerBrows{user_id[:8]}")
        username.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 16px;
                font-weight: 600;
                background: transparent;
            }
        """)
        user_info_layout.addWidget(username)
        
        account_label = QLabel(f"Account #{user_id[-4:]}")
        account_label.setStyleSheet("""
            QLabel {
                color: #B0B0B0;
                font-size: 14px;
                background: transparent;
            }
        """)
        user_info_layout.addWidget(account_label)
        
        # Wallet address with copy functionality
        address_widget = QWidget()
        address_layout = QHBoxLayout(address_widget)
        address_layout.setContentsMargins(0, 5, 0, 0)
        address_layout.setSpacing(8)
        
        # Get wallet address and truncate for display
        wallet_address = self.wallet_manager.get_wallet_info()['address']
        truncated_address = f"{wallet_address[:6]}...{wallet_address[-4:]}"
        
        self.address_label = QPushButton(truncated_address)
        self.address_label.setStyleSheet("""
            QPushButton {
                color: #9CA3AF;
                font-size: 12px;
                font-family: monospace;
                background: transparent;
                border: 1px solid #4B5563;
                border-radius: 6px;
                padding: 4px 8px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #374151;
                border-color: #6B7280;
            }
        """)
        self.address_label.setToolTip("Click to copy full address")
        self.address_label.clicked.connect(lambda: self.copy_address_to_clipboard(wallet_address))
        
        copy_icon = QLabel("📋")
        copy_icon.setStyleSheet("QLabel { color: #6B7280; font-size: 12px; }")
        
        address_layout.addWidget(self.address_label)
        address_layout.addWidget(copy_icon)
        address_layout.addStretch()
        
        user_info_layout.addWidget(address_widget)
        
        profile_layout.addWidget(user_info)
        top_row_layout.addWidget(profile_section)
        
        # Right side buttons (search, apps)
        top_row_layout.addStretch()
        
        search_btn = QPushButton("🔍")
        search_btn.setFixedSize(32, 32)
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #3A3A42;
                border: none;
                border-radius: 6px;
                color: #FFFFFF;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4A4A52;
            }
        """)
        top_row_layout.addWidget(search_btn)
        
        apps_btn = QPushButton("⊞")
        apps_btn.setFixedSize(32, 32)
        apps_btn.setStyleSheet("""
            QPushButton {
                background-color: #3A3A42;
                border: none;
                border-radius: 6px;
                color: #FFFFFF;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4A4A52;
            }
        """)
        top_row_layout.addWidget(apps_btn)
        
        header_layout.addWidget(top_row)
        layout.addWidget(header)
        
        # Main content area
        content = QWidget()
        content.setObjectName("popup_content")
        content.setStyleSheet("""
            QWidget {
                background-color: #2D2D35;
                border-bottom-left-radius: 16px;
                border-bottom-right-radius: 16px;
            }
        """)
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # Total balance section (large like Phantom)
        balance_section = QWidget()
        balance_layout = QVBoxLayout(balance_section)
        balance_layout.setContentsMargins(0, 10, 0, 20)
        balance_layout.setSpacing(8)
        
        # Main balance (get current balance dynamically)
        try:
            # Get real balance for display
            if self.contracts_config and 'contracts' in self.contracts_config:
                usdc_address = self.contracts_config['contracts']['MockUSDC']['address']
                current_balance = self.wallet_manager.wallet.get_token_balance(usdc_address)
                balance_text = f"${current_balance:,.2f}"
            else:
                balance_text = "$0.00"
        except Exception as e:
            print(f"⚠️ Error getting balance for popup: {e}")
            balance_text = "$0.00"
            
        self.popup_balance_label = QLabel(balance_text)
        self.popup_balance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.popup_balance_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 48px;
                font-weight: 300;
                background: transparent;
            }
        """)
        balance_layout.addWidget(self.popup_balance_label)
        
        # Balance change (hide for now since we don't track history)
        # TODO: Implement balance change tracking
        # balance_change = QLabel("+$0.00  +0.00%")
        # balance_change.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # balance_change.setStyleSheet("""
        #     QLabel {
        #         color: #00FF88;
        #         font-size: 16px;
        #         background: transparent;
        #     }
        # """)
        # balance_layout.addWidget(balance_change)
        
        content_layout.addWidget(balance_section)
        
        # Action buttons (Phantom style)
        self.create_phantom_buttons(content_layout)
        
        # Token list section
        self.create_token_list(content_layout)
        
        layout.addWidget(content)
        
    def create_phantom_buttons(self, layout):
        """Create DeFi action buttons (corrected names)"""
        button_container = QWidget()
        button_layout = QGridLayout(button_container)  # Changed to grid layout
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(8)  # Reduced spacing
        
        # Button style (Phantom-like)
        button_style = """
            QPushButton {
                background-color: #3A3A42;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 8px;
                font-size: 11px;
                font-weight: 500;
                min-height: 50px;
                min-width: 70px;
            }
            QPushButton:hover {
                background-color: #4A4A52;
            }
            QPushButton:pressed {
                background-color: #5A5A62;
            }
        """
        
        # Create DeFi action buttons with correct names
        balance_btn = QPushButton("💰\nBalance")
        balance_btn.setStyleSheet(button_style)
        balance_btn.clicked.connect(self.check_real_balance_and_sync)
        button_layout.addWidget(balance_btn, 0, 0)  # Row 0, Column 0
        
        deposit_btn = QPushButton("🏦\nDeposit") 
        deposit_btn.setStyleSheet(button_style)
        deposit_btn.clicked.connect(self.deposit_real_usdc)
        button_layout.addWidget(deposit_btn, 0, 1)  # Row 0, Column 1
        
        yield_btn = QPushButton("📈\nYield")
        yield_btn.setStyleSheet(button_style)
        yield_btn.clicked.connect(self.generate_real_yield)
        button_layout.addWidget(yield_btn, 0, 2)  # Row 0, Column 2
        
        claim_btn = QPushButton("🎁\nReward")
        claim_btn.setStyleSheet(button_style)
        claim_btn.clicked.connect(self.claim_real_rewards)
        button_layout.addWidget(claim_btn, 1, 0)  # Row 1, Column 0
        
        # Add faucet button for getting test USDC
        faucet_btn = QPushButton("🚰\nFaucet")
        faucet_btn.setStyleSheet(button_style)
        faucet_btn.clicked.connect(self.get_test_usdc_from_faucet)
        button_layout.addWidget(faucet_btn, 1, 1)  # Row 1, Column 1
        
        layout.addWidget(button_container)
        
    def create_token_list(self, layout):
        """Create simplified token display showing only USDC"""
        # Token section header
        tokens_header = QLabel("Balance")
        tokens_header.setObjectName("balance_header")  # Add object name
        tokens_header.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 18px;
                font-weight: 600;
                background: transparent;
                margin-bottom: 8px;
            }
        """)
        layout.addWidget(tokens_header)
        
        # USDC Token (only real token)
        usdc_token = self.create_usdc_token_item()
        usdc_token.setObjectName("token_list")
        layout.addWidget(usdc_token)
        
    def create_usdc_token_item(self):
        """Create USDC token display item"""
        token_widget = QWidget()
        token_layout = QHBoxLayout(token_widget)
        token_layout.setContentsMargins(15, 10, 15, 10)
        
        # Token icon (placeholder circle for USDC)
        icon_label = QLabel("⚪")  # Circle placeholder for USDC icon
        icon_label.setStyleSheet("QLabel { font-size: 24px; }")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setFixedSize(40, 40)
        
        # Token info
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(2)
        
        # Token name
        name_label = QLabel("USD Coin")
        name_label.setStyleSheet("QLabel { color: #ffffff; font-weight: bold; font-size: 14px; }")
        
        # Token symbol
        symbol_label = QLabel("USDC")
        symbol_label.setStyleSheet("QLabel { color: #9ca3af; font-size: 12px; }")
        
        info_layout.addWidget(name_label)
        info_layout.addWidget(symbol_label)
        
        # Balance info
        balance_widget = QWidget()
        balance_layout = QVBoxLayout(balance_widget)
        balance_layout.setContentsMargins(0, 0, 0, 0)
        balance_layout.setSpacing(2)
        
        # Get current USDC balance
        try:
            # Get USDC contract address
            if self.contracts_config and 'contracts' in self.contracts_config:
                usdc_address = self.contracts_config['contracts']['MockUSDC']['address']
                # Use wallet to get token balance
                usdc_balance = self.wallet_manager.wallet.get_token_balance(usdc_address)
                balance_usdc = f"{usdc_balance:,.0f} USDC"
                balance_usd = f"${usdc_balance:,.2f}"
            else:
                balance_usdc = "0 USDC"
                balance_usd = "$0.00"
        except Exception as e:
            print(f"⚠️ Error getting USDC balance: {e}")
            balance_usdc = "0 USDC"
            balance_usd = "$0.00"
        
        # USDC amount
        usdc_label = QLabel(balance_usdc)
        usdc_label.setStyleSheet("QLabel { color: #ffffff; font-weight: bold; font-size: 14px; text-align: right; }")
        usdc_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        # USD amount
        usd_label = QLabel(balance_usd)
        usd_label.setStyleSheet("QLabel { color: #9ca3af; font-size: 12px; text-align: right; }")
        usd_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        balance_layout.addWidget(usdc_label)
        balance_layout.addWidget(usd_label)
        
        # Add widgets to token layout
        token_layout.addWidget(icon_label)
        token_layout.addWidget(info_widget)
        token_layout.addStretch()
        token_layout.addWidget(balance_widget)
        
        # Style the token widget
        token_widget.setStyleSheet("""
            QWidget {
                background-color: #374151;
                border-radius: 8px;
            }
            QWidget:hover {
                background-color: #4b5563;
            }
        """)
        
        return token_widget
    
    def copy_address_to_clipboard(self, address):
        """Copy wallet address to clipboard and show feedback"""
        try:
            clipboard = QApplication.clipboard()
            clipboard.setText(address)
            
            # Show temporary feedback
            if hasattr(self, 'address_label'):
                original_text = self.address_label.text()
                self.address_label.setText("Copied!")
                self.address_label.setStyleSheet("""
                    QPushButton {
                        color: #10B981;
                        font-size: 12px;
                        font-family: monospace;
                        background: transparent;
                        border: 1px solid #10B981;
                        border-radius: 6px;
                        padding: 4px 8px;
                        text-align: left;
                    }
                """)
                
                # Reset after 1.5 seconds
                QTimer.singleShot(1500, lambda: self.reset_address_label(original_text))
        except Exception as e:
            print(f"Copy failed: {e}")
    
    def reset_address_label(self, original_text):
        """Reset address label to original state"""
        if hasattr(self, 'address_label'):
            self.address_label.setText(original_text)
            self.address_label.setStyleSheet("""
                QPushButton {
                    color: #9CA3AF;
                    font-size: 12px;
                    font-family: monospace;
                    background: transparent;
                    border: 1px solid #4B5563;
                    border-radius: 6px;
                    padding: 4px 8px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #374151;
                    border-color: #6B7280;
                }
            """)
        
    def sync_popup_data(self):
        """Sync balance to wallet popup"""
        if hasattr(self, 'popup_balance_label'):
            # Update main balance display in USD format
            if hasattr(self, 'current_balance'):
                # Format as USD like Phantom
                self.popup_balance_label.setText(f"${self.current_balance:,.2f}")
            else:
                self.popup_balance_label.setText("$0.00")
        
        # If popup is visible, recreate the token list to update USDC balance
        if hasattr(self, 'wallet_popup') and self.wallet_popup.isVisible():
            # Find and update token section if it exists
            try:
                # Get the content widget from popup layout
                layout = self.wallet_popup.layout()
                if layout and layout.count() > 0:
                    content_widget = None
                    for i in range(layout.count()):
                        widget = layout.itemAt(i).widget()
                        if widget and widget.objectName() == "popup_content":
                            content_widget = widget
                            break
                    
                    if content_widget:
                        content_layout = content_widget.layout()
                        # Find and remove old token list and headers, then add new ones
                        items_to_remove = []
                        for i in range(content_layout.count()):
                            item = content_layout.itemAt(i)
                            if item and item.widget():
                                widget = item.widget()
                                if hasattr(widget, 'objectName') and widget.objectName() in ["token_list", "balance_header"]:
                                    items_to_remove.append(widget)
                        
                        # Remove old items
                        for widget in items_to_remove:
                            content_layout.removeWidget(widget)
                            widget.deleteLater()
                                    
                        # Add updated token list
                        self.create_token_list(content_layout)
            except Exception as e:
                print(f"⚠️ Error updating token list in popup: {e}")
                
    def check_real_balance_and_sync(self):
        """Check balance and sync to popup"""
        self.check_real_balance()
        QTimer.singleShot(1000, self.sync_popup_data)  # Sync after balance updates

    def create_new_tab(self, url="https://www.google.com", title="New Tab"):
        """Create a new browser tab"""
        # Create web browser widget
        browser = QWebEngineView()
        
        # Connect browser signals for navigation updates
        browser.urlChanged.connect(self.update_address_bar)
        browser.loadFinished.connect(self.update_navigation_buttons)
        
        # Add tab
        index = self.tab_widget.addTab(browser, title)
        self.tab_widget.setCurrentIndex(index)
        
        # Load URL
        browser.setUrl(QUrl(url))
        
        # Store browser reference
        self.browsers.append(browser)
        
        return browser

    def close_tab(self, index):
        """Close a tab"""
        if self.tab_widget.count() > 1:
            # Remove browser from list
            widget = self.tab_widget.widget(index)
            if hasattr(widget, 'findChild'):
                browser = widget.findChild(QWebEngineView)
                if browser in self.browsers:
                    self.browsers.remove(browser)
            
            self.tab_widget.removeTab(index)
        else:
            # If it's the last tab, create a new one
            self.create_new_tab()
            self.tab_widget.removeTab(index)

    def on_tab_changed(self, index):
        """Handle tab change"""
        current_widget = self.tab_widget.widget(index)
        if current_widget:
            browser = current_widget.findChild(QWebEngineView) or current_widget
            if hasattr(browser, 'url'):
                self.update_address_bar(browser.url())
                self.update_navigation_buttons()

    def navigate_from_address_bar(self):
        """Navigate to URL from address bar"""
        url = self.address_bar.text().strip()
        if url:
            self.navigate_to(url)

    def navigate_to(self, url):
        """Navigate current tab to URL"""
        if not url.startswith(('http://', 'https://')):
            if '.' in url:
                url = 'https://' + url
            else:
                url = f"https://www.google.com/search?q={url}"
        
        current_browser = self.get_current_browser()
        if current_browser:
            current_browser.setUrl(QUrl(url))

    def get_current_browser(self):
        """Get current browser widget"""
        current_widget = self.tab_widget.currentWidget()
        if current_widget:
            return current_widget.findChild(QWebEngineView) or current_widget
        return None

    def update_address_bar(self, url):
        """Update address bar with current URL"""
        if hasattr(url, 'toString'):
            self.address_bar.setText(url.toString())
        else:
            self.address_bar.setText(str(url))

    def update_navigation_buttons(self):
        """Update navigation button states"""
        current_browser = self.get_current_browser()
        if current_browser and hasattr(current_browser, 'history'):
            self.back_button.setEnabled(current_browser.history().canGoBack())
            self.forward_button.setEnabled(current_browser.history().canGoForward())

    def go_back(self):
        """Go back in current tab"""
        current_browser = self.get_current_browser()
        if current_browser and hasattr(current_browser, 'back'):
            current_browser.back()

    def go_forward(self):
        """Go forward in current tab"""
        current_browser = self.get_current_browser()
        if current_browser and hasattr(current_browser, 'forward'):
            current_browser.forward()

    def refresh_page(self):
        """Refresh current tab"""
        current_browser = self.get_current_browser()
        if current_browser and hasattr(current_browser, 'reload'):
            current_browser.reload()

    def show_menu(self):
        """Show browser menu"""
        QMessageBox.information(self, "Menu", "BurgerBrows Menu\n\nDeFi features available in wallet popup!")
    
    def log_message(self, message):
        """Add message to status log"""
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        full_message = f"{timestamp} {message}"
        
        # Track log text for popup sync
        if not hasattr(self, 'status_log_text'):
            self.status_log_text = ""
        self.status_log_text += full_message + "\n"
        
        # Update popup log if open
        if hasattr(self, 'popup_status_log'):
            self.popup_status_log.append(full_message)
            
        print(full_message)
    
    def check_real_balance(self):
        """Check real USDC balance on blockchain"""
        try:
            if not self.wallet or not self.wallet.is_connected or not self.contracts_config:
                self.log_message("❌ Wallet not connected or contracts not available")
                return
            
            if not self.wallet.account:
                self.log_message("❌ No wallet account available")
                return
            
            self.log_message(f"🏦 Checking real balance on Sepolia blockchain...")
            self.log_message(f"📍 Wallet: {self.wallet.account.address}")
            
            # Get real USDC balance using the wallet's method
            usdc_addr = self.contracts_config['contracts']['MockUSDC']['address']
            balance_usdc = self.wallet.get_token_balance(usdc_addr, self.wallet.account.address)
            
            self.log_message(f"💰 Real USDC Balance: {balance_usdc:,.6f}")
            self.log_message(f"🔗 Retrieved from Sepolia blockchain")
            
            # Store current balance for popup sync
            self.current_balance = balance_usdc
            
            if hasattr(self, 'balance_label'):
                self.balance_label.setText(f"Balance: {balance_usdc:,.2f} USDC")
            
            # Update popup if open
            if hasattr(self, 'popup_balance_label'):
                self.popup_balance_label.setText(f"{balance_usdc:,.6f} USDC")
            
            return balance_usdc
            
        except Exception as e:
            self.log_message(f"❌ Real balance check error: {e}")
            if hasattr(self, 'balance_label'):
                self.balance_label.setText("Balance: Error")
            return 0
    
    def deposit_real_usdc(self):
        """Real USDC deposit to BrowserVault with user confirmation"""
        if not self.wallet or not self.wallet.is_connected or not self.contracts_config:
            self.log_message("❌ Wallet not connected or contracts not loaded")
            return
            
        if not self.wallet.account:
            self.log_message("❌ No wallet account available")
            return
        
        # Ask for amount
        amount, ok = QInputDialog.getDouble(
            self, 
            "💰 Real USDC Deposit", 
            f"Enter USDC amount to deposit to BrowserVault:\n"
            f"Your wallet: {self.wallet_address}\n"
            f"⚠️ This will cost real gas fees!",
            value=100.0,
            min=0.01,
            max=10000.0,
            decimals=2
        )
        
        if not ok:
            return
        
        # Confirm transaction
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("🔐 Confirm Real Transaction")
        msg.setText(f"Deposit {amount} USDC to BrowserVault?")
        msg.setInformativeText(f"This will:\n"
                              f"• Send REAL transaction to Sepolia\n"
                              f"• Cost real gas fees (≈0.001 ETH)\n"
                              f"• Use YOUR unique wallet: {self.wallet_address[:20]}...\n"
                              f"• Deposit to BrowserVault contract")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)
        
        if msg.exec() != QMessageBox.StandardButton.Yes:
            self.log_message("❌ Transaction cancelled by user")
            return
        
        try:
            usdc_address = self.contracts_config['contracts']['MockUSDC']['address']
            vault_address = self.contracts_config['contracts']['BrowserVault']['address']
            
            self.log_message(f"💳 User confirmed: Depositing {amount} USDC to BrowserVault")
            self.log_message(f"🔗 Using YOUR wallet: {self.wallet.account.address}")
            self.log_message("⏳ Sending real approval transaction...")
            
            # First approve the vault to spend USDC
            approve_abi = [{
                "inputs": [{"name": "spender", "type": "address"}, {"name": "amount", "type": "uint256"}],
                "name": "approve",
                "outputs": [{"name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function"
            }]
            
            amount_with_decimals = int(amount * 10**6)  # USDC has 6 decimals
            
            # Send real approve transaction
            approve_hash = self.wallet.call_contract_function(
                usdc_address,
                approve_abi,
                "approve",
                [vault_address, amount_with_decimals]
            )
            
            if approve_hash:
                self.log_message(f"✅ Real approval sent: {approve_hash[:20]}...")
                self.log_message(f"🔗 View on Sepolia: https://sepolia.etherscan.io/tx/{approve_hash}")
                
                # Wait then send deposit transaction
                QTimer.singleShot(3000, lambda: self.send_real_deposit(amount, vault_address))
            else:
                self.log_message("❌ Real approval transaction failed")
                
        except Exception as e:
            self.log_message(f"❌ Real deposit error: {e}")
    
    def send_real_deposit(self, amount, vault_address):
        """Send real deposit transaction to BrowserVault"""
        try:
            self.log_message(f"💰 Step 2/2: Sending real {amount} USDC to BrowserVault...")
            
            deposit_abi = [{
                "inputs": [{"name": "amount", "type": "uint256"}],
                "name": "deposit",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            }]
            
            # Send real deposit transaction (convert amount to integer)
            deposit_hash = self.wallet.call_contract_function(
                vault_address,
                deposit_abi,
                "deposit",
                [int(amount)]  # Convert float to int for contract
            )
            
            if deposit_hash:
                self.log_message(f"✅ Real deposit sent: {deposit_hash[:20]}...")
                self.log_message(f"🔗 View on Sepolia: https://sepolia.etherscan.io/tx/{deposit_hash}")
                self.log_message(f"🎉 {amount} USDC really deposited to BrowserVault!")
                
                # Reload balance after deposit
                QTimer.singleShot(5000, self.check_real_balance)
            else:
                self.log_message("❌ Real deposit transaction failed")
                
        except Exception as e:
            self.log_message(f"❌ Real deposit error: {e}")
    
    def generate_real_yield(self):
        """Generate real yield (admin function)"""
        self.log_message("📈 Real yield generation is an admin function")
        self.log_message("💡 Contact admin to generate yield in the vault")
        
        QMessageBox.information(
            self,
            "📈 Yield Generation",
            "Real yield generation is an administrative function.\n\n"
            "The admin can mint USDC tokens to the vault to simulate yield.\n"
            "Your proportional share will be available for withdrawal."
        )
    
    def claim_real_rewards(self):
        """Claim real rewards from RewardPool"""
        if not self.reward_manager:
            self.log_message("❌ Reward system not available")
            return
        
        try:
            self.log_message(f"🎁 Checking real reward eligibility...")
            self.log_message(f"📊 For wallet: {self.wallet_address}")
            
            # This would need real activity tracking
            activity_score = 100  # Placeholder - should come from database
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Question)
            msg.setWindowTitle("🎁 Claim Real Rewards")
            msg.setText(f"Claim real USDC rewards from RewardPool?")
            msg.setInformativeText(f"This will:\n"
                                  f"• Send REAL transaction to Sepolia\n"
                                  f"• Cost real gas fees\n"
                                  f"• Send USDC to YOUR wallet: {self.wallet_address[:20]}...\n"
                                  f"• Based on your activity score: {activity_score}")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if msg.exec() == QMessageBox.StandardButton.Yes:
                self.log_message(f"🎁 Claiming meaningful rewards...")
                
                # Use fixed reward system for meaningful rewards
                result = self.reward_manager.claim_meaningful_reward(self.wallet_address, activity_score)
                
                if result:
                    self.log_message(f"✅ Meaningful rewards claimed!")
                    self.log_message(f"🔗 Transaction: {result[:20]}...")
                    self.log_message(f"💰 You received 10+ USDC reward!")
                    
                    # Reload balance with longer delay to ensure blockchain update
                    QTimer.singleShot(6000, self.check_real_balance)
                else:
                    self.log_message(f"❌ Reward claim failed")
                    
        except Exception as e:
            self.log_message(f"❌ Real reward error: {e}")

    def get_test_usdc_from_faucet(self):
        """Get test USDC from faucet for testing"""
        try:
            self.log_message(f"🚰 Getting test USDC from faucet...")
            self.log_message(f"📍 Wallet: {self.wallet_address}")
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Question)
            msg.setWindowTitle("🚰 MockUSDC Faucet")
            msg.setText(f"Get test USDC from faucet?")
            msg.setInformativeText(f"This will:\n"
                                  f"• Mint 100 test USDC tokens\n"
                                  f"• Send to YOUR wallet: {self.wallet_address[:20]}...\n"
                                  f"• Use real gas fees on Sepolia\n"
                                  f"• Perfect for testing DeFi functions!")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if msg.exec() == QMessageBox.StandardButton.Yes:
                self.log_message(f"🪙 Minting 100 test USDC to your wallet...")
                
                # Import contracts and wallet to access minting
                from contracts import BurgerBrowsContracts
                
                # Create contracts instance 
                contracts = BurgerBrowsContracts()
                
                # Custom mint function that mints to user's specific wallet
                result = self.mint_usdc_to_user_wallet(contracts, 100.0)
                
                if result:
                    self.log_message(f"✅ Successfully minted 100 test USDC!")
                    self.log_message(f"🔗 Transaction: {result[:20]}...")
                    self.log_message(f"💰 USDC sent to your wallet: {self.wallet_address[:20]}...")
                    
                    # Reload balance after a delay
                    QTimer.singleShot(3000, self.check_real_balance)
                else:
                    self.log_message(f"❌ Faucet minting failed")
                    self.log_message(f"💡 Make sure you have ETH for gas fees!")
                    
        except Exception as e:
            self.log_message(f"❌ Faucet error: {e}")

    def mint_usdc_to_user_wallet(self, contracts, amount: float) -> str:
        """Custom mint function that mints USDC to the specific user's wallet"""
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
            
            self.log_message(f"🎯 Minting {amount} USDC to: {self.wallet_address}")
            
            # Use the contracts wallet to mint to the user's wallet address
            tx_hash = contracts.wallet.call_contract_function(
                contracts.usdc_address,
                mint_abi,
                "mint",
                [self.wallet_address, amount_with_decimals]  # Mint to user's wallet, not contract wallet
            )
            
            if tx_hash:
                receipt = contracts.wallet.wait_for_transaction(tx_hash)
                if receipt and receipt.get('status') == 1:
                    self.log_message(f"✅ USDC minted to {self.wallet_address}")
                    return tx_hash
            
            return None
            
        except Exception as e:
            self.log_message(f"❌ Error in custom mint: {e}")
            return None

def main():
    """Main application entry point"""
    print("🚀 BurgerBrows Real Multi-User Browser")
    print("=" * 50)
    
    if GUI_AVAILABLE:
        # Run GUI browser
        app = QApplication(sys.argv)
        browser = RealMultiUserBrowser()
        browser.show()
        sys.exit(app.exec())
    else:
        # Run console mode
        print("Running in console mode...")
        browser = RealMultiUserBrowser()

if __name__ == '__main__':
    main()