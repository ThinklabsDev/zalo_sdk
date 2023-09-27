import pkce
code_verifier = pkce.generate_code_verifier(length=43)
print(code_verifier)
code_challenge = pkce.get_code_challenge(code_verifier)
print(code_challenge)