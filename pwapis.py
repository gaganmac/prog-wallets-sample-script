import requests
import os
from dotenv import load_dotenv, dotenv_values
import uuid

# Generates unique idemopotent key each time
def generate_idempotent_key():
    return str(uuid.uuid4())

# Get the path to the directory this file is in
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Connect the path with your '.env' file name
load_dotenv(os.path.join(BASEDIR, '.env'))

# Get API Key
API_KEY = os.getenv("API_KEY")
USER_ID = "96a99b93-54b4-4004-ad11-b8d3b3dfa88f"
X_USER_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXZlbG9wZXJFbnRpdHlFbnZpcm9ubWVudCI6IlRFU1QiLCJlbnRpdHlJZCI6IjUxMGFlZWMxLWZhNWUtNDU0Yi05NDU2LTQyYjE0N2ZjMDJhNiIsImV4cCI6MTY4OTYxMzQzNywiaWF0IjoxNjg5NjA5ODM3LCJpbnRlcm5hbFVzZXJJZCI6IjQ0NzE4MzM4LTdlNzQtNTk2MS1iMmJjLTI5ZGYyYmQwYzllZCIsImlzcyI6Imh0dHBzOi8vcHJvZ3JhbW1hYmxlLXdhbGxldC5jaXJjbGUuY29tIiwianRpIjoiYjk4MTBhOGQtNGI2ZS00NGVjLWI4YjUtNmExZDhkYzQ5YmNjIiwic3ViIjoiOTZhOTliOTMtNTRiNC00MDA0LWFkMTEtYjhkM2IzZGZhODhmIn0.Z_HWZ3wWqIAmAJK2xIu9g53H32Nq8l3MYjPSIN_rI42wazGI-Nx5O_Wu7Xqea4ljQByaUqhg-FfE50Vdfgm20OjKOfEM2wvqBIJF33OVoDHyuMIgiN1DecQAbHrb4OKAokJIhLuf06ZAV9bjeGAs-58kizuTcyNPowjyOtB0TqTPtlvM6SKm1U-AWgxquik4lrlBFY1qxbZa0_ICyJW2zw5Xr5zk9gTS62yBYXEmx3_W4rlVSNe0SX5xZEfQfZr-uClNhjh9Fyp6S2HH7m1pdtEuJLtB66Btqt1Sgsy64x_BChV3BCUJcP0XmuJku_oH3FNKriIUYe5IuRCApb8reA"
IDEMPOTENCY_KEY = generate_idempotent_key()
ENCRYPTION_KEY = "7O6LdEHtYlw+Y7ybdFMVzLHwu2OXRbn/vJbBEI2+JCQ="
# "123e4567-e89b-12d3-a456-426614174000"


headers = {
    "accept" : "application/json",
    "content-type" : "application/json",
    "authorization" : "Bearer " + API_KEY
}


# 1. Create a user with the URL 
payload = {"userId" : generate_idempotent_key()}
usersUrl = "https://api.circle.com/v1/w3s/users"
# response = requests.post(usersUrl, headers = headers, json = payload, verify = False)


# 2. Create a JWT Token for this user
payload = {"userId" : USER_ID, "idempotencyKey": IDEMPOTENCY_KEY}
tokenUrl = "https://api.circle.com/v1/w3s/users/token"
# response = requests.post(tokenUrl, headers = headers, json = payload, verify=False)

# 3. Initialize User to get Challenge ID.
userInitUrl = "https://api.circle.com/v1/w3s/user/initialize"
payloadUserInit = {
    "blockchains": ["MATIC-MUMBAI"],
    "idempotencyKey": IDEMPOTENCY_KEY,
    "userId" : USER_ID
}
headersUserInit = {
    "accept": "application/json",
    "X-User-Token": X_USER_TOKEN,
    "content-type": "application/json",
    "authorization" : "Bearer " + API_KEY
}
response = requests.post(userInitUrl, json = payloadUserInit, headers = headersUserInit, verify = False)


# 4. Create wallet for the user
payload = {
    "blockchains": ["MATIC-MUMBAI"],
    "idempotencyKey": IDEMPOTENCY_KEY
}
headers = {
    "accept": "application/json",
    "X-User-Token": X_USER_TOKEN,
    "content-type": "application/json",
    "Authorization": "Bearer TEST_API_KEY:96ac39f6bb2213c0acffb31406eed379:266cbdfc38148f9c3ed92edeaac0839e"
}
userWalleturl = "https://api.circle.com/v1/w3s/user/wallets"
# response = requests.post(userWalleturl, json=payload, headers=headers, verify=False)

# 5. Enter Token info, Encryption Key, and Challenge-ID into the iOS simulator

# 6. Get User Wallets to check it was created
getWalletUrl = "https://api.circle.com/v1/w3s/wallets/"
# response = requests.get(getWalletUrl, json = payloadUserInit, headers = headersUserInit, verify=False)

# 7. Go to Polygon faucet, get Matic and transfer from Metamask to Address

# 8. Get Wallet Balance
walletId = "018963d6-b8d4-72a8-91c5-e541e1dec171"
getWalletBalanceUrl = "https://api.circle.com/v1/w3s/wallets/" + walletId + "/balances"
# response = requests.get(getWalletBalanceUrl, json = payloadUserInit, headers = headersUserInit, verify=False)

# 8. Get tokenID from the prior call, and Create a transaction
tokenId = "e4f549f9-a910-59b1-b5cd-8f972871f5db"
transactionUrl = "https://api.circle.com/v1/w3s/user/transactions/transfer"
txPayload = {
    "userId" : USER_ID, # Created in user init
    "destinationAddress": "0xa2C256243E5DE1891dEf26b715FEAe279F7E5fD4", # My metamask
    "idempotencyKey": IDEMPOTENCY_KEY, # Created in user init
    "feeLevel": "LOW",
    "amounts" : ["0.000001"],
    "tokenId": "e4f549f9-a910-59b1-b5cd-8f972871f5db", # Gotten from step 7
    "walletId": "0189614c-b43c-7e80-be31-3ba8f28e145c" # Gotten from UI / console
}
txHeaders = {
    "Authorization": "Bearer TEST_API_KEY:96ac39f6bb2213c0acffb31406eed379:266cbdfc38148f9c3ed92edeaac0839e",
    "accept": "application/json",
    "X-User-Token": X_USER_TOKEN,
    "content-type": "application/json",    
}
# response = requests.post(transactionUrl, json = txPayload, headers = txHeaders, verify=False)

print(response.text)