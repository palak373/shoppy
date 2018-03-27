import random
import string
import uuid

def rand_uid():
    return str(uuid.uuid4())[:8]

def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))