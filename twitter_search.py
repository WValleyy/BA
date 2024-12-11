from tweety import Twitter
from tweety.filters import SearchFilters
from dotenv import load_dotenv
import os
from datetime import datetime
import csv
import pandas as pd
# Load variables from the .env file
load_dotenv()

async def login():
    # Read username and password from environment variables
    username = os.getenv("USERNAMEE")
    password = os.getenv("PASSWORD")

    if not username or not password:
        raise ValueError("USERNAMEE or PASSWORD is not configured in the .env file")

    # Initialize Twitter client
    app = Twitter("session")
    await app.sign_in(username, password)
    return app


async def run_search_user(keywords, app, pages_num=1,wait_times=2,cursor_=None):
    for keyword in keywords:
        results = await app.search(keyword, pages=pages_num, wait_time = wait_times, cursor = cursor_, filter_= SearchFilters.Users())

        # Specify the CSV file name for each keyword
        csv_file = f"twitter_users_{keyword}.csv"

        # Define the fields to save
        fields = [
            "id", "rest_id", "created_at", "date", "bio", "can_dm", "is_blocked",
            "fast_followers_count", "favourites_count", "followers_count",
            "friends_count", "listed_count", "location", "media_count", "name",
            "normal_followers_count", "profile_banner_url", "profile_image_url_https",
            "protected", "screen_name", "username", "statuses_count", "verified",
            "possibly_sensitive", "pinned_tweets", "notifications_enabled",
            "notifications", "community_role"
        ]

        # Check if the file exists and open in append mode if so
        try:
            with open(csv_file, mode="x", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fields)
                # Write header row
                writer.writeheader()
        except FileExistsError:
            pass  # File exists, no need to write header

        # Append user data
        with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            for user in results:
                writer.writerow({field: getattr(user, field, None) for field in fields})

        print(f"Appended {len(results)} users to {csv_file}")



import csv

async def run_crawl_user_profile(name_lists, app):
    # Specify the CSV file name for the final output file
    csv_file = "KOL_profile.csv"
    
    # Define the fields to save
    fields = [
        "id", "rest_id", "created_at", "date", "bio", "can_dm", "is_blocked",
        "fast_followers_count", "favourites_count", "followers_count", "friends_count",
        "listed_count", "location", "media_count", "name", "normal_followers_count",
        "profile_banner_url", "profile_image_url_https", "protected", "screen_name",
        "username", "statuses_count", "verified", "possibly_sensitive", "pinned_tweets",
        "notifications_enabled", "notifications", "community_role"
    ]

    # Check if the file exists and open in append mode if so
    try:
        with open(csv_file, mode="x", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            # Write header row
            writer.writeheader()
    except FileExistsError:
        pass  # File exists, no need to write header

    # Open the file to log users that could not be found
    with open("notfound_user.txt", mode="a", encoding="utf-8") as notfound_file:
        # Loop over the list of names to get user information
        for keyword in name_lists:
            try:
                result = await app.get_user_info(keyword)  # Assuming `results` is a single user object now
                # Append user data to the file
                with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=fields)
                    writer.writerow({field: getattr(result, field, None) for field in fields})
                print(f"Appended user {keyword} to {csv_file}")
            except Exception as e:
                # Log the user that caused the error to the notfound_user.txt file
                notfound_file.write(f"Error with user {keyword}: {str(e)}\n")
                print(f"Error with user {keyword}: {str(e)}")
                continue  # Continue with the next user if error occurs



# Read keywords from a text file
def read_keywords_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]
    

# Filter users from all CSV files
import os
import pandas as pd

def filter_users(keywords):
    filtered_users = []

    for keyword in keywords:
        csv_file = f"twitter_users_{keyword}.csv"
        if os.path.exists(csv_file):
            # Read the CSV file
            df = pd.read_csv(csv_file)

            # Filter users with followers >= 1000 and favourites/tweets average >= 50
            df_filtered = df[(df["followers_count"] >= 1000) &
                             ((df["favourites_count"] / df["statuses_count"]).fillna(0) >= 50)]

            # Print the number of users remaining after filtering for the current keyword
            print(f"Keyword '{keyword}': {len(df_filtered)} users remaining after filtering.")

            # Append filtered users to the list
            filtered_users.extend(df_filtered.to_dict(orient="records"))

    # Save the filtered users to a new CSV file
    output_file_path = "filtered_twitter_users.csv"
    if filtered_users:
        pd.DataFrame(filtered_users).to_csv(output_file_path, index=False, encoding="utf-8")
        print(f"Filtered users saved to {output_file_path}")
        print(f"Total filtered users: {len(filtered_users)}")
    else:
        print("No users matched the criteria.")

    return output_file_path



async def crawl_tweets(screen_name,app,):

    
    all_tweets = await app.get_tweets("elonmusk")
    for tweet in all_tweets:
        print(tweet.text)
        print(tweet.id)


async def crawl_tweets_from_KOLs(input_file_path, output_file_path, app, pages=1, replies=False, wait_time=2, cursor=None):
    """
    Crawl tweets from a CSV file and save results to another CSV file with all available attributes.
    
    :param input_file_path: Path to the input CSV file containing the screen names.
    :param output_file_path: Path to the output CSV file to save tweets.
    :param app: The application instance used to call get_tweets.
    :param pages: Number of pages to fetch per user.
    :param replies: Include replies in the fetched tweets or not.
    :param wait_time: Wait time between requests.
    :param cursor: Cursor for pagination, if applicable.
    """
    tweets_data = []

    # Read the input file and get screen names
    with open(input_file_path, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        screen_names = [row['screen_name'] for row in reader]

    # Crawl tweets for each screen name
    for screen_name in screen_names:
        print(f"Fetching tweets for user: {screen_name}")
        try:
            all_tweets = await app.get_tweets(
                username=screen_name,
                pages=pages,
                replies=replies,
                wait_time=wait_time,
                cursor=cursor
            )

            for tweet in all_tweets:
                tweets_data.append({
                    'id': tweet.id,
                    'created_on': tweet.created_on,
                    'date': tweet.date,
                    'text': tweet.text,
                    'rich_text': tweet.rich_text.text if tweet.rich_text else None,
                    'author': tweet.author.username if tweet.author else None,
                    'is_retweet': tweet.is_retweet,
                    'retweeted_tweet_id': tweet.retweeted_tweet.id if tweet.is_retweet else None,
                    'is_quoted': tweet.is_quoted,
                    'quoted_tweet_id': tweet.quoted_tweet.id if tweet.is_quoted else None,
                    'is_reply': tweet.is_reply,
                    'replied_to': tweet.replied_to.id if tweet.is_reply else None,
                    'is_sensitive': tweet.is_sensitive,
                    'reply_counts': tweet.reply_counts,
                    'quote_counts': tweet.quote_counts,
                    'bookmark_count': tweet.bookmark_count,
                    'views': tweet.views,
                    'likes': tweet.likes,
                    'language': tweet.language,
                    'place': tweet.place.name if tweet.place else None,
                    'retweet_counts': tweet.retweet_counts,
                    'source': tweet.source,
                    'has_moderated_replies': tweet.has_moderated_replies,
                    'is_liked': tweet.is_liked,
                    'is_retweeted': tweet.is_retweeted,
                    'can_reply': tweet.can_reply,
                    'broadcast': tweet.broadcast.title if tweet.broadcast else None,
                    'edit_control': tweet.edit_control,
                    'has_newer_version': tweet.has_newer_version,
                    'audio_space_id': tweet.audio_space_id,
                    'pool': tweet.pool.title if tweet.pool else None,
                    'community': tweet.community.name if tweet.community else None,
                    'media': [media.url for media in tweet.media],
                    'user_mentions': [mention.username for mention in tweet.user_mentions],
                    'urls': [url.url for url in tweet.urls],
                    'hashtags': [hashtag.text for hashtag in tweet.hashtags],
                    'symbols': [symbol.text for symbol in tweet.symbols],
                    'community_note': tweet.community_note,
                    'url': tweet.url,
                    'threads': [thread.id for thread in tweet.threads],
                    'comments': [comment.id for comment in tweet.comments]
                })

        except Exception as e:
            print(f"Error fetching tweets for user {screen_name}: {e}")

    # Check if output file exists
    file_exists = os.path.isfile(output_file_path)

    # Save results to a CSV file (append if file exists, else write headers)
    with open(output_file_path, mode='a' if file_exists else 'w', newline='', encoding='utf-8') as outfile:
        fieldnames = [
            'id', 'created_on', 'date', 'text', 'rich_text', 'author', 'is_retweet', 'retweeted_tweet_id',
            'is_quoted', 'quoted_tweet_id', 'is_reply', 'replied_to', 'is_sensitive', 'reply_counts',
            'quote_counts', 'bookmark_count', 'views', 'likes', 'language', 'place', 'retweet_counts',
            'source', 'has_moderated_replies', 'is_liked', 'is_retweeted', 'can_reply', 'broadcast',
            'edit_control', 'has_newer_version', 'audio_space_id', 'pool', 'community', 'media', 
            'user_mentions', 'urls', 'hashtags', 'symbols', 'community_note', 'url', 'threads', 'comments'
        ]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        # Write header only if file does not exist
        if not file_exists:
            writer.writeheader()

        writer.writerows(tweets_data)

    print(f"Saved {len(tweets_data)} tweets to {output_file_path}.")
