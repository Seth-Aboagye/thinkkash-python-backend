import uuid

def generate_tracking_code() -> str:
    return f"TKS-{str(uuid.uuid4()).split('-')[0].upper()}"
