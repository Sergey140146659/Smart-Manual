import g4f

g4f.logging = True # enable logging
g4f.check_version = False # Disable automatic version checking


# normal response
response = g4f.ChatCompletion.create(
    model=g4f.models.gpt_4,
    messages=[{"role": "user", "content": "Hello"}],
)  # alterative model setting

print(response)