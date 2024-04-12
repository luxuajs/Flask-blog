import secrets, string


def create_secret_key(length=73):
  '''
    Function to create a random secret key.
  '''
  # Creating the alphabet
  alphabet = string.ascii_letters + string.digits + string.punctuation 

  secret_key = "".join([secrets.choice(alphabet) for _ in range(length)])

  return secret_key

# I've created a eviron varible(secret_key and wtf_csrf_secret_key)
secret_key = create_secret_key()
wtf_csrf_secret_key = create_secret_key()