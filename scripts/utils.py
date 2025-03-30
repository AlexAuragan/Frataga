import re
import unicodedata
def name_to_key(name: str):
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    return re.sub(r'[^a-zA-Z0-9]+', '_', name).lower()