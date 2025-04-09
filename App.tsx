// App.tsx
import React, { useEffect, useState } from "react";
import { ethers } from "ethers";
import CONFIG from "./config.ts";
import validatorImage from "./assets/validator-nft.png";
import logo from "./assets/logo.svg";
import maskot from "./assets/maskot.avif";
import "./App.css";

const App = () => {
  const [walletAddress, setWalletAddress] = useState<string | null>(null);
  const [isWhitelisted, setIsWhitelisted] = useState(false);
  const [hasMinted, setHasMinted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [txHash, setTxHash] = useState<string | null>(null);
  const [showNote, setShowNote] = useState(false);

  useEffect(() => {
    if ((window as any).ethereum?.selectedAddress) {
      connectWallet();
    }
  }, []);

  const connectWallet = async () => {
    if (!(window as any).ethereum) return alert("Metamask is not installed");
    try {
      const provider = new ethers.BrowserProvider((window as any).ethereum);
      await (window as any).ethereum.request({ method: "eth_requestAccounts" });
      const signer = await provider.getSigner();
      const address = await signer.getAddress();
      setWalletAddress(address);
      await checkWhitelist(address);
      await checkMinted(address);
    } catch (err) {
      alert("Wallet connection failed");
    }
  };

  const disconnectWallet = () => {
    setWalletAddress(null);
    setIsWhitelisted(false);
    setHasMinted(false);
    setTxHash(null);
  };

  const checkWhitelist = async (address: string) => {
    try {
      const res = await fetch(CONFIG.VALIDATORS_JSON);
      const data = await res.json();
      const match = data.find((entry: any) => entry.evm_address.toLowerCase() === address.toLowerCase());
      setIsWhitelisted(!!match);
    } catch (err) {
      console.error("Whitelist check failed:", err);
    }
  };

  const checkMinted = async (address: string) => {
    try {
      const provider = new ethers.BrowserProvider((window as any).ethereum);
      const contract = new ethers.Contract(CONFIG.CONTRACT_ADDRESS, ["function hasMinted(address) view returns (bool)"], provider);
      const minted = await contract.hasMinted(address);
      setHasMinted(minted);
    } catch (err) {
      console.error("Mint check failed:", err);
    }
  };

  const mintNFT = async () => {
    if (!walletAddress) return;
    setLoading(true);
    setTxHash(null);
    try {
      const provider = new ethers.BrowserProvider((window as any).ethereum);
      const signer = await provider.getSigner();
      const contract = new ethers.Contract(CONFIG.CONTRACT_ADDRESS, ["function mint() public"], signer);
      const tx = await contract.mint();
      await tx.wait();
      setTxHash(tx.hash);
      setHasMinted(true);
    } catch (err) {
      alert("Minting failed.");
      console.error("Mint error:", err);
    } finally {
      setLoading(false);
    }
  };

  const addNetworkToMetamask = async () => {
    try {
      await (window as any).ethereum.request({
        method: "wallet_addEthereumChain",
        params: [
          {
            chainId: "0x40d8",
            chainName: "OG-Newton-Testnet",
            rpcUrls: ["https://evmrpc-testnet.0g.ai"],
            nativeCurrency: {
              name: "AOGI",
              symbol: "AOGI",
              decimals: 18,
            },
            blockExplorerUrls: ["https://chainscan-newton.0g.ai"],
          },
        ],
      });
    } catch (err) {
      console.error("Add network error:", err);
    }
  };

  return (
    <div className="main-container">
      <header className="header">
        <img src={logo} alt="Logo" className="logo" />
        <div className="wallet-buttons">
          {walletAddress ? (
            <>
              <span className="wallet-text">{walletAddress.slice(0, 6)}...{walletAddress.slice(-4)}</span>
              <button onClick={disconnectWallet} className="disconnect-btn">Logout</button>
            </>
          ) : (
            <button onClick={connectWallet} className="connect-btn">Connect Wallet</button>
          )}
        </div>
      </header>

      <main>
        <h1 className="title">OG Validator NFT Mint</h1>

        <div className="nft-wrapper">
          <img src={validatorImage} alt="NFT" className="nft-image" />
        </div>

        {!walletAddress ? (
          <p className="status">Connect your wallet to continue.</p>
        ) : !isWhitelisted ? (
          <p className="error">Only whitelisted validators can mint.</p>
        ) : hasMinted ? (
          <p className="success">You have already minted your NFT.</p>
        ) : (
          <button onClick={mintNFT} disabled={loading} className="mint-btn">
            {loading ? "Minting..." : "Mint Now"}
          </button>
        )}

        {txHash && (
          <p className="success">
            TX: <a href={`https://chainscan-newton.0g.ai/tx/${txHash}`} target="_blank" rel="noreferrer">{txHash.slice(0, 10)}...</a>
          </p>
        )}

        <button onClick={addNetworkToMetamask} className="metamask-btn">Add OG Network</button>

        <div
          className="note-bar"
          onMouseEnter={() => setShowNote(true)}
          onMouseLeave={() => setShowNote(false)}
        >
          !!! Validator Notice
          {showNote && (
            <div className="note-detail">
              This NFT can only be minted by active bonded validators. The active list is limited to 200 entries. It is refreshed automatically every 24 hours and synced to the contract.
            </div>
          )}
        </div>
      </main>

      <footer className="footer">
        <p>
          Site design & development by <b className="glow">coinsspor ✨ </b>
        </p>
        <img src={maskot} alt="Maskot" className="footer-maskot" />
      </footer>
    </div>
  );
};

export default App;
