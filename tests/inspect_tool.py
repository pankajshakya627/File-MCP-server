
import sys
sys.path.append("/Volumes/CrucialX9_MAC/Local_MCPs/mcp-local")
from local_main_mcp import count_words

print(f"Type: {type(count_words)}")
print(f"Dir: {dir(count_words)}")
if hasattr(count_words, 'fn'):
    print("Has 'fn' attribute")
if hasattr(count_words, '__wrapped__'):
    print("Has '__wrapped__' attribute")
