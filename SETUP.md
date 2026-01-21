# Quick Setup Guide for Node.js Developers

## 🚀 Installation Steps

### 1. Check if Python is installed

```bash
python3 --version
```

If you see `Python 3.9.x` or higher, you're good! Skip to step 2.

If not, install Python:

**macOS:**
```bash
brew install python3
```

**Or download from:** https://www.python.org/downloads/

### 2. Activate the virtual environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt, indicating the virtual environment is active.

### 3. Install Python packages (like npm install)

```bash
pip install -r requirements.txt
```

**Note:** After activating the venv, you can use `pip` instead of `pip3`.

### 4. Create .env file

```bash
cp .env.example .env
```

Then edit `.env` and add your Instagram credentials:
```
IG_USERNAME=your_actual_username
IG_PASSWORD=your_actual_password
```

### 5. Run the script!

**Make sure the virtual environment is activated first!** Then:

```bash
python get_followers.py
```

**Or use the venv Python directly (without activating):**
```bash
venv/bin/python get_followers.py
```

## 📦 What Gets Installed

When you run `pip3 install -r requirements.txt`, it installs:

- **instagrapi** - Instagram Private API library (like a Node.js package)
- **python-dotenv** - Loads .env files (like dotenv in Node.js)

## 🔄 Node.js vs Python Cheat Sheet

| What you do in Node.js | Python equivalent |
|------------------------|-------------------|
| `npm install` | `pip install -r requirements.txt` (in venv) |
| `npm start` | `python script.py` (in venv) |
| `node script.js` | `python script.py` (in venv) |
| `require('dotenv')` | `from dotenv import load_dotenv` |
| `process.env.VAR` | `os.getenv('VAR')` |
| `package.json` | `requirements.txt` |
| `node_modules/` | `venv/` (virtual environment) |

## ✅ Verify Everything Works

1. **Check Python:**
   ```bash
   python3 --version
   # Should show: Python 3.9.x or higher
   ```

2. **Check pip:**
   ```bash
   pip3 --version
   # Should show: pip 21.x.x or higher
   ```

3. **Check installed packages:**
   ```bash
   pip3 list | grep instagrapi
   # Should show: instagrapi
   ```

4. **Activate venv and run the script:**
   ```bash
   source venv/bin/activate
   python get_followers.py
   ```

## 🆘 Common Issues

### "command not found: python3"
- Install Python from python.org
- Or use `python` instead of `python3`

### "No module named 'instagrapi'"
- **Activate the virtual environment first:** `source venv/bin/activate`
- Then run: `pip install -r requirements.txt`
- Or use venv Python directly: `venv/bin/python get_followers.py`

### "No module named 'dotenv'"
- Same as above, install requirements

### Login fails
- Check your credentials in `.env`
- Make sure 2FA is disabled or use app password
- Check internet connection

## 🎯 What the Script Does

1. Logs into Instagram using your credentials
2. Fetches your followers list
3. Displays each follower's info one by one:
   - Username
   - Full name
   - Profile picture
   - Verification status
   - Account type (private/public/business)
   - Follower/following counts
   - Bio

## 💡 Tips

- The script saves your session in `session.json` so you don't need to login every time
- It includes delays to avoid rate limiting
- If you get rate limited, wait 10-15 minutes and try again







