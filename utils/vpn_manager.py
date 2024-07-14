import asyncio
from openvpn_api import VPN
import random
import time

class VPNManager:
    def __init__(self, config_files):
        self.config_files = config_files
        self.current_config = None
        self.vpn = None

    async def connect(self):
        if self.vpn:
            await self.disconnect()
        
        self.current_config = random.choice(self.config_files)
        self.vpn = VPN()
        await asyncio.to_thread(self.vpn.connect, config_file=self.current_config)
        print(f"Connected to VPN using {self.current_config}")

    async def disconnect(self):
        if self.vpn:
            await asyncio.to_thread(self.vpn.disconnect)
            print("Disconnected from VPN")
            self.vpn = None

    async def rotate(self):
        await self.disconnect()
        await asyncio.sleep(1)  # Wait a bit before reconnecting
        await self.connect()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()