"""
Run after: python -m venv venv && venv\\Scripts\\activate
Checks Python version and suggests fix if dependencies may not install.
"""
import sys

def main():
    v = sys.version_info
    py_ver = f"{v.major}.{v.minor}.{v.micro}"
    ok = (v.major == 3 and 10 <= v.minor <= 13)
    print(f"Python {py_ver}")
    if not ok:
        if v.minor >= 14:
            print("  Python 3.14+ detected. CrewAI and Streamlit may not support it yet.")
            print("  For a working install, use Python 3.11 or 3.12:")
            print("    - Install from https://www.python.org/downloads/")
            print("    - Then: py -3.12 -m venv venv   (if you have 3.12)")
            print("    - Or: python3.12 -m venv venv")
        else:
            print("  Python 3.10 or newer is recommended.")
    else:
        print("  Python version is fine for this project.")
    print("\nNext: pip install -r requirements.txt")
    print("Then: python database_setup.py")
    print("Then: python -m streamlit run app.py")

if __name__ == "__main__":
    main()
