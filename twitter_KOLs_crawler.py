from tweety import Twitter
import asyncio
import os
import csv
import tweety
import time
import argparse
from itertools import product
from tweety.filters import SearchFilters

async def login(username, password):
    if not username or not password:
        raise ValueError("USERNAME or PASSWORD is not provided")

    # Initialize Twitter client
    app = Twitter("session")
    await app.sign_in(username, password, extra="")
    return app

async def crawl_KOLs(keywords, app, pages_num=20, wait_times=10, min_followers=2000, min_favourites=300, min_statuses=200, company_bot_list=None):
    if company_bot_list is None:
        company_bot_list = [] 

    csv_file = "twitter_KOLs.csv"
    with open("crawl_KOLs_error.txt", mode="a", encoding="utf-8") as error_file:
        # Loop through each keyword to find KOLs
        for keyword in keywords:
            print(f"Searching for KOLs with keyword: {keyword}")
            retry_count = 0

            while retry_count <= 3:  # Retry up to 3 times
                try:
                    results = await app.search(keyword, pages=pages_num, wait_time=wait_times, filter_=SearchFilters.Users())

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
                            if (user.followers_count > min_followers and 
                                user.favourites_count > min_favourites and 
                                user.statuses_count > min_statuses and 
                                not any(keyword in user.description.lower() for keyword in company_bot_list)):
                                writer.writerow({field: getattr(user, field, None) for field in fields})

                    print(f"Appended {len(results)} KOLs to {csv_file}")
                    break  # Exit retry loop if successful
                except Exception as e:
                    retry_count += 1
                    print(f"Error searching for KOLs with keyword {keyword}: {e}. Retrying ({retry_count}/3)...")
                    if retry_count > 3:
                        error_file.write(f"{keyword}\n")
                    time.sleep(500)

async def main(username, password):
   
    with open("role_keyword.txt", mode="r", encoding="utf-8") as role_file:
        roles = [line.strip().lower() for line in role_file if line.strip()]

   
    with open("web3_keyword.txt", mode="r", encoding="utf-8") as web3_file:
        web3_keywords = [line.strip().lower() for line in web3_file if line.strip()]

   
    with open("revert_keyword.txt", mode="r", encoding="utf-8") as revert_file:
        company_bot_list = [line.strip().lower() for line in revert_file if line.strip()]

  
    combined_keywords = [f"{role} {web3}" for role, web3 in product(roles, web3_keywords)]

   
    app = await login(username, password)
    await crawl_KOLs(
        keywords=combined_keywords,
        app=app,
        company_bot_list=company_bot_list
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Twitter KOL Crawler")
    parser.add_argument("-u", "--username", required=True, help="Twitter username")
    parser.add_argument("-p", "--password", required=True, help="Twitter password")
    
    args = parser.parse_args()
    asyncio.run(main(args.username, args.password)) 




    
