from tweety import Twitter
import asyncio
import os
import csv
import tweety
import time
import argparse
from itertools import product
from tweety.filters import SearchFilters

from tweety.types import twDataTypes

async def login(username, password):
    if not username or not password:
        raise ValueError("USERNAME or PASSWORD is not provided")

    # Initialize Twitter client
    app = Twitter("session")
    await app.sign_in(username, password, extra="")
    return app


async def crawl_followers_usernames(input_file_path, output_file_path, app, pages=1, wait_time=2):
    # Đọc danh sách screen_name từ file đầu vào
    with open(input_file_path, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        screen_names = [row['screen_name'] for row in reader]
        screen_names = screen_names[140:]
    # Mở file lỗi để ghi log những user gặp lỗi
    with open("crawl_user_followers_error.txt", mode="a", encoding="utf-8") as error_file, \
         open(output_file_path, mode='a', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        
        # Ghi header vào file đầu ra (nếu file rỗng)
        if outfile.tell() == 0:  # Chỉ ghi header nếu file chưa có nội dung
            writer.writerow(['KOL_username', 'followers_usernames'])

        # Lặp qua từng KOL username để fetch followers
        for screen_name in screen_names:
            print(f"Fetching followers for user: {screen_name}")
            retry_count = 0

            while retry_count <= 3:  # Thử lại tối đa 3 lần
                try:
                    # Fetch followers bằng app Tweety
                    all_followers = await app.get_user_followers(
                        username=screen_name,
                        pages=pages,
                        wait_time=wait_time
                    )
                    
                    # Lấy danh sách username của followers
                    followers_usernames = [follower.username for follower in all_followers]
                    
                    # Lưu dữ liệu của user vừa crawl được vào file
                    writer.writerow([screen_name, ', '.join(map(str, followers_usernames))])
                    print(f"Saved followers for user: {screen_name}")
                    break  # Thoát khỏi vòng lặp retry nếu thành công
                except Exception as e:
                    retry_count += 1
                    print(f"Error fetching followers for user {screen_name}: {e}. Retrying ({retry_count}/3)...")
                    if retry_count > 3:
                        error_file.write(f"{screen_name}\n")
                    time.sleep(500)  # Chờ trước khi thử lại



async def main(username, password):

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

