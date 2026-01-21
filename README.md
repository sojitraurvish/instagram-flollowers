# Instagram Follower Data Fetcher

A simple Python script to fetch and display your Instagram followers' data one by one using `instagrapi`.

## 🐍 For Node.js Developers - Python Setup Guide

Since you're a Node.js developer, here's what you need to know:

### Step 1: Install Python

**macOS (using Homebrew):**
```bash
brew install python@3.13
```

**Or download from:**
- Visit https://www.python.org/downloads/
- Download Python 3.13 or 3.12 (required for instagrapi 2.2.1+)
- Run the installer

**Verify installation:**
```bash
python3.13 --version
# Should show Python 3.13.x
```

### Step 2: Create Virtual Environment

**Important:** Always use a virtual environment (similar to `node_modules` in Node.js):

```bash
# Create virtual environment
python3.13 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

After activation, your terminal prompt will show `(venv)`.

**To deactivate later:**
```bash
deactivate
```

### Step 3: Install Project Dependencies

```bash
# Make sure venv is activated (you should see (venv) in your prompt)
# Install required packages
pip install -r requirements.txt
```

This is similar to `npm install` in Node.js!

### Step 4: Set Up Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Instagram credentials
# IG_USERNAME=your_instagram_username
# IG_PASSWORD=your_instagram_password
```

### Step 5: Run the Script

**Make sure your virtual environment is activated:**
```bash
source venv/bin/activate
```

**Then run:**
```bash
python get_followers.py
```

**Or run directly without activating:**
```bash
./venv/bin/python get_followers.py
```

## 📋 What Gets Displayed

For each follower, the script shows:
- ✅ Username
- ✅ Full Name
- ✅ User ID
- ✅ Profile Picture URL
- ✅ Verification Status
- ✅ Private/Public Account
- ✅ Business Account Status
- ✅ Follower Count
- ✅ Following Count
- ✅ Post Count
- ✅ Bio

## 🔄 Comparison: Node.js vs Python

| Node.js | Python |
|---------|--------|
| `npm install` | `pip install` (in venv) |
| `npm start` | `python script.py` (in venv) |
| `package.json` | `requirements.txt` |
| `node_modules/` | `venv/` (virtual environment) |
| `require()` | `import` |
| `.env` with `dotenv` | `.env` with `python-dotenv` |

## 🛠️ Troubleshooting

### "TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'"
- This means you're using Python 3.9 or earlier
- Install Python 3.13: `brew install python@3.13`
- Recreate venv: `rm -rf venv && python3.13 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`

### "python3: command not found"
- Make sure Python 3.13+ is installed: `brew install python@3.13`
- Use `python3.13` explicitly if needed

### "pip3: command not found" or "externally-managed-environment"
- Always use a virtual environment (see Step 2)
- Activate venv first: `source venv/bin/activate`
- Then use `pip install` (not `pip3`)

### Login Issues

#### "IP address is added to the blacklist" Error
This is the most common error. Instagram blocks IP addresses that show suspicious activity.

**Solutions (try in order):**
1. **Wait 30-60 minutes** - Instagram often temporarily blocks IPs
2. **Change your IP address:**
   - Use a VPN service
   - Restart your router (if using dynamic IP)
   - Use mobile data/hotspot instead of WiFi
   - Use a proxy (see below)
3. **Login via Instagram app/website first** - This helps verify your account
4. **Delete session.json and try again:**
   ```bash
   rm session.json
   python get_followers.py
   ```
5. **Use a proxy** - Add to your `.env` file:
   ```
   IG_PROXY=http://proxy-server:port
   # Or with authentication:
   IG_PROXY=http://username:password@proxy-server:port
   ```

#### Other Login Issues
- Make sure credentials are correct in `.env`
- If 2FA is enabled, the script will prompt for code
- If challenge is required, check your Instagram app/email
- The script now includes automatic retry logic (3 attempts with delays)

### Rate Limiting
- The script includes delays between requests (1-3 seconds)
- If you get rate limited, wait a few minutes and try again
- The script automatically retries failed logins with delays

## 📁 Project Structure

```
insta api/
├── get_followers.py      # Main script
├── requirements.txt      # Python dependencies (like package.json)
├── .env.example         # Environment variables template
├── .env                 # Your credentials (create this)
├── venv/                # Virtual environment (like node_modules)
└── session.json         # Saved session (created after first login)
```

## 🔐 Security Notes

- Never commit `.env` or `session.json` to git
- The `session.json` file stores your login session
- Keep your credentials secure

## 🚀 Advanced Usage

### Get Followers of Another User

Edit `get_followers.py` and change:
```python
user_id = cl.user_id_from_username(username)  # Your account
# To:
user_id = cl.user_id_from_username("target_username")  # Other user
```

### Save Data to File

You can modify the script to save data to JSON/CSV instead of just displaying.

## 📚 Learn More

- [instagrapi Documentation](https://adw0rd.github.io/instagrapi/)
- [Python Official Docs](https://docs.python.org/3/)

## ⚠️ Important Notes

- This uses Instagram's private API, which may violate their Terms of Service
- Use responsibly and at your own risk
- Rate limiting may apply
- Instagram may require challenges/verification

# instagram-flollowers
