import re
import math
import sys

# 🎨 Colors for terminal output
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# 🖼️ Banner
BANNER = f"""{CYAN}
   ____                      _                         _     
  |  _ \ __ _ ___ ___  ___  | |__   ___  ___ _ __ ___ | |__  
  | |_) / _` / __/ __|/ _ \ | '_ \ / _ \/ __| '_ ` _ \| '_ \ 
  |  __/ (_| \__ \__ \  __/ | | | | (_) \__ \ | | | | | |_) |
  |_|   \__,_|___/___/\___| |_| |_|\___/|___/_| |_| |_|_.__/ 
            🔐 Password Strength Checker
{RESET}
"""

def calculate_entropy(password: str) -> float:
    """Calculate entropy of a password (bits of security)."""
    pool = 0
    if re.search(r"[a-z]", password):
        pool += 26
    if re.search(r"[A-Z]", password):
        pool += 26
    if re.search(r"\d", password):
        pool += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        pool += 32
    entropy = len(password) * math.log2(pool) if pool else 0
    return entropy

def check_password_strength(password: str) -> dict:
    """Check the strength of a password and return details."""
    errors = {
        "length": len(password) < 8,
        "digit": re.search(r"\d", password) is None,
        "uppercase": re.search(r"[A-Z]", password) is None,
        "lowercase": re.search(r"[a-z]", password) is None,
        "symbol": re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) is None,
    }

    # Score calculation
    score = 5 - sum(errors.values())
    entropy = calculate_entropy(password)

    if score == 5 and entropy >= 50:
        strength = "Strong"
    elif score >= 3:
        strength = "Medium"
    else:
        strength = "Weak"

    return {"strength": strength, "errors": errors, "entropy": entropy}


if __name__ == "__main__":
    print(BANNER)
    pwd = input("👉 Enter a password to check: ")
    result = check_password_strength(pwd)

    # Show results with colors
    color = GREEN if result["strength"] == "Strong" else YELLOW if result["strength"] == "Medium" else RED
    print(f"\n🔎 Password Strength: {color}{result['strength']}{RESET}")
    print(f"🔐 Entropy (bits of security): {CYAN}{result['entropy']:.2f}{RESET}\n")

    if not any(result["errors"].values()):
        print(f"{GREEN}✅ Password meets all security requirements.{RESET}")
    else:
        print(f"{RED}Suggestions to improve your password:{RESET}")
        if result["errors"]["length"]:
            print(" - Increase length to at least 8 characters.")
        if result["errors"]["digit"]:
            print(" - Add at least one number.")
        if result["errors"]["uppercase"]:
            print(" - Add at least one uppercase letter.")
        if result["errors"]["lowercase"]:
            print(" - Add at least one lowercase letter.")
        if result["errors"]["symbol"]:
            print(" - Add at least one special character.")
