import os
os.chdir('/root/.......')
import json
import requests
import bech32  # pip install bech32

def valoper_to_account(valoper_address):
    hrp, data = bech32.bech32_decode(valoper_address)
    return bech32.bech32_encode("0g", data)

def bech32_to_eth(bech32_addr):
    hrp, data = bech32.bech32_decode(bech32_addr)
    decoded_bytes = bytes(bech32.convertbits(data, 5, 8, False))
    return '0x' + decoded_bytes.hex()

def main():
    url = "https://0gchain-api.coinsspor.com/cosmos/staking/v1beta1/validators?status=BOND_STATUS_BONDED&pagination.limit=200"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("API isteği başarısız oldu.")

    bonded_data = response.json()
    validators = bonded_data.get("validators", [])
    result = []

    for val in validators:
        try:
            moniker = val["description"]["moniker"]
            operator_address = val["operator_address"]
            account_address = valoper_to_account(operator_address)
            evm_address = bech32_to_eth(account_address)

            result.append({
                "moniker": moniker,
                "operator_address": operator_address,
                "account_address": account_address,
                "evm_address": evm_address
            })
        except Exception as e:
            print(f"[!] Error parsing {val.get('operator_address', 'UNKNOWN')}: {e}")

    if not result:
        print("[!] Aktif validator bulunamadı veya veri çekilemedi.")
    else:
        with open("validators.json", "w", encoding="utf-8") as outfile:
            json.dump(result, outfile, indent=4)
        print("✅ validators.json başarıyla oluşturuldu.")

if __name__ == "__main__":
    main()
