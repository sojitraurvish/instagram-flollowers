import os
import time
from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired, ChallengeRequired, TwoFactorRequired,
    PleaseWaitFewMinutes
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration for nested follower collection
MAX_DEPTH = 2  # Maximum depth of nested followers (0 = only your followers, 1 = followers of followers, etc.)
DELAY_BETWEEN_REQUESTS = 1.0  # Delay in seconds between API requests to avoid rate limiting

def is_email(value):
    """Check if a string looks like an email address"""
    return '@' in str(value) and '.' in str(value)

def get_user_profile_info(cl, username, user_id=None):
    """Get complete profile information for a user"""
    try:
        user_info = cl.user_info_by_username(username)
        return {
            'username': user_info.username or "N/A",
            'full_name': user_info.full_name or "N/A",
            'user_id': user_info.pk,
            'biography': user_info.biography or "N/A",
            'external_url': user_info.external_url or "N/A",
            'is_private': user_info.is_private,
            'is_verified': user_info.is_verified,
            'is_business': user_info.is_business,
            'posts_count': user_info.media_count,
            'followers_count': user_info.follower_count,
            'following_count': user_info.following_count
        }
    except Exception as e:
        # Fallback: try to get basic info from user_id if available
        if user_id:
            try:
                user_info = cl.user_info(user_id)
                return {
                    'username': user_info.username or username or "N/A",
                    'full_name': user_info.full_name or "N/A",
                    'user_id': user_info.pk,
                    'biography': getattr(user_info, 'biography', 'N/A') or "N/A",
                    'external_url': getattr(user_info, 'external_url', 'N/A') or "N/A",
                    'is_private': getattr(user_info, 'is_private', False),
                    'is_verified': getattr(user_info, 'is_verified', False),
                    'is_business': getattr(user_info, 'is_business', False),
                    'posts_count': getattr(user_info, 'media_count', 'N/A'),
                    'followers_count': getattr(user_info, 'follower_count', 'N/A'),
                    'following_count': getattr(user_info, 'following_count', 'N/A')
                }
            except:
                pass
        # Return minimal info if all else fails
        return {
            'username': username or "N/A",
            'full_name': "N/A",
            'user_id': user_id or "N/A",
            'biography': "N/A",
            'external_url': "N/A",
            'is_private': False,
            'is_verified': False,
            'is_business': False,
            'posts_count': "N/A",
            'followers_count': "N/A",
            'following_count': "N/A"
        }

def print_user_profile(profile_info, indent_level=0):
    """Print user profile information with proper indentation"""
    indent = "  " * indent_level
    print(f"{indent}Username: @{profile_info['username']}")
    print(f"{indent}Full Name: {profile_info['full_name']}")
    print(f"{indent}User ID: {profile_info['user_id']}")
    print(f"{indent}Biography: {profile_info['biography']}")
    print(f"{indent}External URL: {profile_info['external_url']}")
    print(f"{indent}Is Private: {profile_info['is_private']}")
    print(f"{indent}Is Verified: {profile_info['is_verified']}")
    print(f"{indent}Is Business Account: {profile_info['is_business']}")
    print(f"{indent}Total Posts: {profile_info['posts_count']}")
    print(f"{indent}Total Followers: {profile_info['followers_count']}")
    print(f"{indent}Total Following: {profile_info['following_count']}")
    print()

def get_nested_followers(cl, user_id, username, current_depth=0, visited=None, max_depth=MAX_DEPTH):
    """
    Recursively get followers and their nested followers
    
    Args:
        cl: Instagram client
        user_id: User ID to get followers for
        username: Username for display
        current_depth: Current recursion depth
        visited: Set of visited user IDs to avoid cycles
        max_depth: Maximum depth to recurse
    
    Returns:
        Dictionary with user profile and nested followers
    """
    if visited is None:
        visited = set()
    
    # Avoid cycles
    if user_id in visited:
        print(f"{'  ' * current_depth}⚠️  @{username} already visited in this branch - skipping to avoid cycles\n")
        return None
    
    # Respect depth limit (but still show profile if at max depth)
    if current_depth > max_depth:
        print(f"{'  ' * current_depth}⚠️  Maximum depth ({max_depth}) reached - skipping @{username}\n")
        return None
    
    visited.add(user_id)
    
    # Get user profile info
    print(f"{'  ' * current_depth}📥 Fetching profile info for @{username}...")
    profile_info = get_user_profile_info(cl, username, user_id)
    time.sleep(DELAY_BETWEEN_REQUESTS)
    
    # Print user profile
    print(f"{'  ' * current_depth}{'=' * (60 - current_depth * 2)}")
    print(f"{'  ' * current_depth}FOLLOWER: @{username}")
    print(f"{'  ' * current_depth}{'=' * (60 - current_depth * 2)}")
    print_user_profile(profile_info, current_depth)
    
    result = {
        'profile': profile_info,
        'followers': []
    }
    
    # If we haven't reached max depth, get their followers
    if current_depth < max_depth:
        try:
            print(f"{'  ' * current_depth}📥 Fetching followers of @{username}...")
            followers = cl.user_followers(user_id, amount=0)  # Get all followers
            
            if followers:
                print(f"{'  ' * current_depth}✅ Found {len(followers)} followers for @{username}\n")
                sorted_followers = sorted(followers.values(), key=lambda x: (x.username or "").lower())
                
                for idx, follower in enumerate(sorted_followers, 1):
                    follower_username = follower.username or "N/A"
                    follower_user_id = follower.pk
                    
                    print(f"{'  ' * current_depth}{'─' * (60 - current_depth * 2)}")
                    print(f"{'  ' * current_depth}[{idx}/{len(followers)}] Processing @{follower_username}...")
                    
                    # Recursively get nested followers
                    nested_data = get_nested_followers(
                        cl, 
                        follower_user_id, 
                        follower_username, 
                        current_depth + 1, 
                        visited.copy(),  # Pass copy to allow different branches
                        max_depth
                    )
                    
                    if nested_data:
                        result['followers'].append(nested_data)
                    
                    # Delay between requests
                    if idx < len(sorted_followers):
                        time.sleep(DELAY_BETWEEN_REQUESTS)
            else:
                print(f"{'  ' * current_depth}No followers found for @{username}\n")
        except Exception as e:
            error_str = str(e).lower()
            if 'private' in error_str:
                print(f"{'  ' * current_depth}⚠️  @{username} has a private account - cannot fetch followers\n")
            elif 'rate' in error_str or 'wait' in error_str:
                print(f"{'  ' * current_depth}⚠️  Rate limited - waiting 5 seconds...\n")
                time.sleep(5)
            else:
                print(f"{'  ' * current_depth}⚠️  Error fetching followers for @{username}: {e}\n")
    
    return result

def login_user(cl, username, password):
    """Helper function to handle login with proper error handling"""
    # Warn if using email instead of username
    if is_email(username):
        print(f"⚠️  Warning: You're using an email address: {username}")
        print("   Instagram API usually requires your Instagram USERNAME, not email.")
        print("   Example: If your email is 'user@gmail.com', use your Instagram handle like 'your_instagram_handle'")
        print("   Continuing anyway...\n")
    
    try:
        print(f"🔐 Logging in as @{username}...")
        cl.login(username, password)
        # Small delay to let session stabilize
        time.sleep(2)
        # Verify login succeeded
        cl.account_info()
        print("✅ Login successful!\n")
        return True
    except PleaseWaitFewMinutes as e:
        print(f"⏳ Rate limited: {e}")
        print("   Instagram has temporarily blocked login attempts.")
        print("   Please wait 15-30 minutes before trying again.")
        print("   Too many failed attempts can trigger this.")
        return False
    except ChallengeRequired as e:
        print(f"❌ Instagram requires challenge verification: {e}")
        print("   You may need to verify your account through Instagram's app or website.")
        print("   Check your email or Instagram app for a verification request.")
        return False
    except TwoFactorRequired as e:
        print(f"❌ Two-factor authentication required: {e}")
        print("   Please disable 2FA temporarily or use an app-specific password.")
        return False
    except LoginRequired as e:
        print(f"❌ Login failed: login_required")
        print("   This usually means:")
        print("   1. Wrong username/password")
        print("   2. Using email instead of Instagram username")
        print("   3. Account security check required (login via Instagram app first)")
        print("   4. Too many failed attempts (wait 15-30 minutes)")
        return False
    except Exception as e:
        print(f"❌ Login error: {e}")
        error_str = str(e).lower()
        if 'rate' in error_str or 'wait' in error_str or 'few minutes' in error_str:
            print("   Instagram is rate limiting. Please wait 15-30 minutes and try again.")
        return False

def main():
    # Initialize client
    cl = Client()
    
    # Get credentials from environment or prompt
    username = os.getenv("IG_USERNAME") or os.getenv("USERNAME")
    password = os.getenv("IG_PASSWORD") or os.getenv("PASSWORD")
    
    # Try to load existing session
    session_file = "session.json"
    logged_in = False
    
    if os.path.exists(session_file):
        try:
            print("📂 Loading existing session...")
            cl.load_settings(session_file)
            # Verify session is still valid
            try:
                cl.account_info()
                print("✅ Session is valid!\n")
                logged_in = True
            except (LoginRequired, PleaseWaitFewMinutes):
                print("⚠️  Session expired or invalid, will login again...\n")
                # Remove old session file to start fresh
                try:
                    os.remove(session_file)
                    print("🗑️  Removed old session file for fresh login\n")
                except:
                    pass
                if not username or not password:
                    print("💡 Tip: Use your Instagram USERNAME (not email) if login fails")
                    username = input("Enter your Instagram username: ")
                    password = input("Enter your Instagram password: ")
                logged_in = login_user(cl, username, password)
                if logged_in:
                    cl.dump_settings(session_file)
                    print("💾 Session saved\n")
        except Exception as e:
            print(f"⚠️  Could not load session: {e}")
            # Remove corrupted session
            try:
                if os.path.exists(session_file):
                    os.remove(session_file)
                    print("🗑️  Removed corrupted session file\n")
            except:
                pass
            if not username or not password:
                print("💡 Tip: Use your Instagram USERNAME (not email) if login fails")
                username = input("Enter your Instagram username: ")
                password = input("Enter your Instagram password: ")
            logged_in = login_user(cl, username, password)
            if logged_in:
                cl.dump_settings(session_file)
                print("💾 Session saved\n")
    else:
        # No session file, login required
        if not username or not password:
            print("💡 Tip: Use your Instagram USERNAME (not email)")
            username = input("Enter your Instagram username: ")
            password = input("Enter your Instagram password: ")
        logged_in = login_user(cl, username, password)
        if logged_in:
            cl.dump_settings(session_file)
            print("💾 Session saved\n")
    
    if not logged_in:
        print("\n" + "="*60)
        print("❌ Could not authenticate")
        print("="*60)
        print("\nCommon solutions:")
        print("1. Use your Instagram USERNAME (not email) in .env file")
        print("   Example: IG_USERNAME=your_instagram_handle")
        print("2. Wait 15-30 minutes if you've tried multiple times (rate limiting)")
        print("3. Login to Instagram via app/website first to verify account")
        print("4. Check that credentials are correct in .env file")
        print("\nTo update credentials, edit .env file:")
        print("  IG_USERNAME=your_instagram_username")
        print("  IG_PASSWORD=your_password")
        return
    
    # Get account info
    print("="*60)
    print("YOUR PROFILE INFORMATION")
    print("="*60)
    print()
    
    try:
        account = cl.account_info()
        # Get User object for counts (media_count, follower_count, following_count)
        # Handle the pinned_channels_info KeyError bug in instagrapi
        try:
            user = cl.user_info_by_username(account.username)
            posts_count = user.media_count
            followers_count = user.follower_count
            following_count = user.following_count
        except KeyError as e:
            if 'pinned_channels_info' in str(e):
                # Fallback: try to get counts from account_info if available
                print("⚠️  Note: Using account_info for counts (pinned_channels_info error handled)")
                posts_count = getattr(account, 'media_count', 0)
                followers_count = getattr(account, 'follower_count', 'N/A')
                following_count = getattr(account, 'following_count', 'N/A')
            else:
                raise
        except Exception as e:
            # For other errors, try fallback
            error_str = str(e).lower()
            if 'pinned_channels' in error_str or 'keyerror' in error_str:
                print("⚠️  Note: Using account_info for counts (fallback)")
                posts_count = getattr(account, 'media_count', 0)
                followers_count = getattr(account, 'follower_count', 'N/A')
                following_count = getattr(account, 'following_count', 'N/A')
            else:
                raise
        
        print(f"Username: @{account.username}")
        print(f"Full Name: {account.full_name}")
        print(f"User ID: {account.pk}")
        print(f"Biography: {account.biography or 'N/A'}")
        print(f"External URL: {account.external_url or 'N/A'}")
        print(f"Is Private: {account.is_private}")
        print(f"Is Verified: {account.is_verified}")
        print(f"Is Business Account: {account.is_business}")
        print(f"Total Posts: {posts_count}")
        print(f"Total Followers: {followers_count}")
        print(f"Total Following: {following_count}")
        print("="*60)
        
        # Get and display nested followers
        print("\n" + "="*60)
        print("NESTED FOLLOWERS COLLECTION")
        print("="*60)
        print(f"Max Depth: {MAX_DEPTH} (0 = your followers only, 1 = followers of followers, etc.)")
        print(f"Delay between requests: {DELAY_BETWEEN_REQUESTS} seconds")
        print("="*60)
        print()
        
        try:
            print("📥 Starting nested follower collection...")
            print(f"🔍 Collecting followers at depth 0 (your followers)...\n")
            
            # Get your followers first
            followers = cl.user_followers(account.pk, amount=0)  # amount=0 means get all
            
            if not followers:
                print("No followers found.")
            else:
                print(f"✅ Found {len(followers)} direct followers\n")
                print("="*60)
                print("STARTING NESTED COLLECTION")
                print("="*60)
                print()
                
                # Sort followers by username for better readability
                sorted_followers = sorted(followers.values(), key=lambda x: (x.username or "").lower())
                
                all_nested_data = []
                
                for idx, follower in enumerate(sorted_followers, 1):
                    follower_username = follower.username or "N/A"
                    follower_user_id = follower.pk
                    
                    print(f"\n{'='*60}")
                    print(f"PROCESSING FOLLOWER {idx}/{len(sorted_followers)}: @{follower_username}")
                    print(f"{'='*60}\n")
                    
                    # Get nested followers recursively
                    nested_data = get_nested_followers(
                        cl,
                        follower_user_id,
                        follower_username,
                        current_depth=0,
                        visited=set(),
                        max_depth=MAX_DEPTH
                    )
                    
                    if nested_data:
                        all_nested_data.append(nested_data)
                    
                    # Delay between main followers
                    if idx < len(sorted_followers):
                        print(f"\n⏸️  Waiting {DELAY_BETWEEN_REQUESTS} seconds before next follower...\n")
                        time.sleep(DELAY_BETWEEN_REQUESTS)
                
                print("\n" + "="*60)
                print("NESTED COLLECTION COMPLETE")
                print("="*60)
                print(f"Total direct followers processed: {len(all_nested_data)}")
            
        except (LoginRequired, PleaseWaitFewMinutes) as e:
            print(f"\n❌ Error fetching followers: {e}")
            print("   Session may have expired or rate limited.")
        except Exception as e:
            print(f"\n❌ Error fetching followers: {e}")
            error_str = str(e).lower()
            if 'rate' in error_str or 'wait' in error_str:
                print("   Instagram is rate limiting. Please wait 15-30 minutes and try again.")
            import traceback
            traceback.print_exc()
        
        print("\n✅ Done!")
    except (LoginRequired, PleaseWaitFewMinutes) as e:
        print(f"\n❌ Session expired or rate limited: {e}")
        print("   Please run the script again after waiting a few minutes.")
    except Exception as e:
        print(f"\n❌ Error getting account info: {e}")
        error_str = str(e).lower()
        if 'rate' in error_str or 'wait' in error_str:
            print("   Instagram is rate limiting. Please wait 15-30 minutes and try again.")
        raise

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
