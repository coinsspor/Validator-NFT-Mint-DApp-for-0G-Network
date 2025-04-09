# Validator-NFT-Mint-DApp-for-0G-Network
A fully open-source DApp allowing active validators of the 0g Network testnet to mint a unique on-chain NFT as a badge of recognition.

# Validator NFT Mint DApp for OG Network

<p align="center">
  <img src="https://validatornft-0g.coinsspor.com/images/validator.png"" width="300" alt="NFT Preview">
</p>

## 🌐 Live

  
[🔗 https://validatornft-0g.coinsspor.com/](https://validatornft-0g.coinsspor.com/)

## 📜 Description
Open-source DApp that allows active validators on 0g Cosmos testnet to mint exclusive on-chain NFT badges.

## 🚀 Features
- 🔐 Whitelist-only minting
- ⚡ Real-time validator status checks
- 💰 One NFT per wallet (500 max supply)
- 🖼 Shared metadata with unique on-chain IDs
- 🔄 Automated whitelist updates via Python scripts

## 🏗 Project Structure
```bash
.
├── frontend/                 # React application
│   ├── public/               # Static files
│   │   └── validators.json   # Whitelist cache
│   └── src/
│       ├── App.tsx           # Core DApp logic
│       ├── config.ts         # Contract configuration
├── smart-contract/           # Ethereum smart contracts
│   ├── ValidatorNFT.sol      # Main ERC721 contract
│   └── ValidatorNFT_ABI.json # Contract interface
├── whitelist-scripts/        # Validator management
│   ├── fetch_validators.py   # Pulls active validators
│   └── update_whitelist.py   # Updates contract
└── metadata/                 # NFT assets
    ├── metadata.json         # Common metadata
    └── validator.png         # NFT image
```
## 🚀 Quick Start

### 1. 📄 Deploy the Smart Contract

Deploy ValidatorNFT.sol on 0g EVM testnet via Remix or Hardhat.
Use this metadata URI as constructor parameter:
```bash
https://validatornft-0g.coinsspor.com/metadata/metadata.json
```
Then copy the deployed contract address and update:
```bash
// frontend/src/config.ts
export default {
  CONTRACT_ADDRESS: "0xYourDeployedContractAddress",
  VALIDATORS_JSON: "/validators.json"
};
```
### 2. 📰 Run Python Scripts for Whitelist

Requirements: 
```bash 
pip install web3 requests bech32
```

Step 1: Fetch the top 200 active bonded validator EVM addresses
```bash 
python3 whitelist-scripts/fetch_validators.py
```
Step 2: Push whitelist to contract in batch:

```bash 
python3 whitelist-scripts/batch_whitelist_checker.py
```
### 3. 🌐 Serve the Frontend
```bash 
cd frontend
npm install
npm run build
```
Host the dist or build folder using Nginx, Vercel, Netlify, etc.

## 💼 Contract Functions
```bash 
function setValidator(address _addr, bool _status) public onlyOwner;
function batchSetValidators(address[] calldata addrs, bool status) public onlyOwner;
function mint() public;
function hasMinted(address) view returns (bool);
function isValidator(address) view returns (bool);
```
## 🚨 Security Notes

No private key is exposed in frontend 

Contract prevents duplicate minting (hasMinted check)

Only contract owner can manage whitelist

Metadata/image is hosted off-chain, but safely referenced

## 🎨 Metadata Example

```bash 
{
  "name": "Validator OG NFT",
  "description": "A unique badge for active 0g validators",
  "image": "https://validatornft-0g.coinsspor.com/metadata/validator.png"
}
```

## 🧳 Credits

This DApp is designed and developed by coinsspor ✨ as a community gift to the OG network.

Follow the repo for updates & validator tools!


# Copyright Notice

**Copyright © 2025 coinsspor**  
All rights reserved.

## License Terms

The software and associated documentation files (the "Software") are protected under copyright law.  
No part of this work may be:

- 📌 Copied or reproduced
- 🔧 Modified or adapted
- 📦 Distributed or published
- 💻 Used commercially or otherwise

without the **express written permission** of the copyright holder.

## Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

## Restrictions

Unauthorized use, reproduction, or distribution of this Software:
- 🚫 Is strictly prohibited
- ⚖️ May result in legal action
- 🔒 Violates intellectual property rights

For licensing inquiries, please contact:  
telegram, @coinsspor
