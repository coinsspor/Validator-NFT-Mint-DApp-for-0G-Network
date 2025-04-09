# -*- coding: utf-8 -*-
import json
import time
from web3 import Web3

# === Ayarlar ===
RPC_URL = "https://evmrpc-testnet.0g.ai"
PRIVATE_KEY = "0x.............................................."
CONTRACT_ADDRESS = "0x565165f19dbe937e30f1d50397a6d53870f67e4a"
ABI_PATH = "ValidatorNFT_ABI.json"
VALIDATORS_JSON = "validators.json"

# === Web3 bağlantısı ===
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)
sender_address = account.address

print("[✓] RPC bağlantı durumu:", w3.is_connected())
print("[✓] Cüzdan adresi:", sender_address)
print("[✓] Son blok:", w3.eth.block_number)

# === Kontrat oluşturma ===
try:
    with open(ABI_PATH) as f:
        contract_abi = json.load(f)
    contract = w3.eth.contract(address=w3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)
except Exception as e:
    print("[!] Kontrat bağlanırken hata oluştu:", e)
    exit()

# === JSON'dan yeni validator evm adreslerini çek ===
try:
    with open(VALIDATORS_JSON, "r") as f:
        validators = json.load(f)
except Exception as e:
    print("[!] validators.json dosyası okunamadı:", e)
    exit()

# Yeni eklenecek evm adresleri
new_validators = []
for val in validators:
    try:
        evm = val["evm_address"].strip()
        checksum = Web3.to_checksum_address(evm)
        new_validators.append(checksum)
    except Exception as e:
        print(f"[!] EVM adres hatası: {val} -> {e}")

# === Zincirde şu an whitelist olan adresleri al ===
print("\n[...] Zincirde whitelist (isValidator=True) olan adresler kontrol ediliyor...")
existing_validators = []
for addr in new_validators:
    try:
        if contract.functions.isValidator(addr).call():
            existing_validators.append(addr)
    except Exception as e:
        print(f"[!] isValidator kontrol hatası: {addr} -> {e}")

print(f"[✓] Toplam {len(existing_validators)} mevcut whitelist'te olan adres bulundu:")
for i, addr in enumerate(existing_validators):
    print(f"[EXISTING-{i+1}] {addr}")

# === Önce whitelist'te olanları False yap ===
if existing_validators:
    print("\n[-] Mevcut whitelist adresleri False yapılacak...")
    try:
        nonce = w3.eth.get_transaction_count(sender_address)
        tx = contract.functions.batchSetValidators(existing_validators, False).build_transaction({
            "from": sender_address,
            "nonce": nonce,
            "gas": 8000000,
            "gasPrice": w3.to_wei("2", "gwei")
        })
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"[✓] False işlemi gönderildi! TX Hash: {tx_hash.hex()}")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=900)
        print("[✓] False işlemi onaylandı, status:", receipt.status)
    except Exception as e:
        print("[!] False işlemi sırasında hata:", e)

# === Şimdi yeni whitelist'e eklenecek adresleri yazdır ===
print(f"\n[+] Yeni {len(new_validators)} adres whitelist'e eklenecek:")
for i, addr in enumerate(new_validators[:200]):
    print(f"[NEW-{i+1}] {addr}")

# === Yeni whitelist True işlemi ===
try:
    nonce = w3.eth.get_transaction_count(sender_address)
    tx = contract.functions.batchSetValidators(new_validators, True).build_transaction({
        "from": sender_address,
        "nonce": nonce,
        "gas": 8000000,
        "gasPrice": w3.to_wei("2", "gwei")
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"\n[✓] Yeni whitelist işlemi gönderildi! TX Hash: {tx_hash.hex()}")
    print("[...] İşlem onayı bekleniyor...")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=900)
    print("[✓] Yeni whitelist işlemi onaylandı, status:", receipt.status)
except Exception as e:
    print(f"[!] HATA - Yeni whitelist işlemi gönderilemedi: {e}")

# === Final durum kontrolü ===
print("\n[🔍] Güncel whitelist durumu kontrol ediliyor...")
for i, addr in enumerate(new_validators):
    try:
        status = contract.functions.isValidator(addr).call()
        print(f"[{i+1}] {addr} => isValidator: {status}")
    except Exception as e:
        print(f"[{i+1}] {addr} => [HATA]: {e}")
