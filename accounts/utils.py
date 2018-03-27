import uuid

def rand_uid():
    return str(uuid.uuid4())[:8]