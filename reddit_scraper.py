import praw
#!/usr/bin/env python3
"""
A script to scrape posts from a specified subreddit using PRAW (Python Reddit API Wrapper)
and save the data to JSON or CSV format.
"""
import praw.exceptions
import argparse
import logging
import json
import csv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Main function to scrape Reddit data.
    """
    parser = argparse.ArgumentParser(description="Scrape data from a specified subreddit.")
    parser.add_argument("subreddit", help="Name of the subreddit to scrape (e.g., 'python')")
    parser.add_argument("--sort_type", default="hot", choices=["hot", "new", "top", "controversial"],
                        help="Sort type for posts (hot, new, top, controversial). Default: hot")
    parser.add_argument("--limit", type=int, default=10, help="Number of posts to retrieve. Must be positive. Default: 10")
    parser.add_argument("--output_format", default="none", choices=["json", "csv", "none"],
                        help="Format for saving the output (json, csv, none). Default: none")
    parser.add_argument("--output_file", default="reddit_posts",
                        help="Name of the output file (without extension). Default: reddit_posts")

    args = parser.parse_args()

    if args.limit <= 0:
        logging.error("Limit must be a positive integer.")
        return

    logging.info(f"Subreddit: {args.subreddit}")
    logging.info(f"Sort type: {args.sort_type}")
    logging.info(f"Limit: {args.limit}")
    logging.info(f"Output format: {args.output_format}")
    logging.info(f"Output file prefix: {args.output_file}")

    # Initialize PRAW.
    # Ensure you have a praw.ini file set up in the same directory or in ~/.config/
    # or ensure PRAW environment variables (PRAW_CLIENT_ID, PRAW_CLIENT_SECRET, PRAW_USER_AGENT) are set.
    # See PRAW documentation for more details: https://praw.readthedocs.io/en/stable/getting_started/configuration.html
    try:
        reddit = praw.Reddit(site_name="bot1") # Assuming 'bot1' is defined in your praw.ini or environment variables are set
        # Test authentication by trying to access reddit.user.me()
        # This will raise an exception if authentication fails
        user = reddit.user.me()
        if user:
            logging.info(f"Successfully authenticated as: {user}")
        else:
            # This case should ideally not be reached if praw.Reddit() succeeds without site_name and without anonymous access.
            # If site_name is used and it allows anonymous access, reddit.user.me() will be None.
            logging.warning("Authenticated for read-only access or anonymous mode. Some functionalities might be limited.")

    except Exception as e: # Consider more specific PRAW exceptions if known
        logging.error(f"Failed to initialize PRAW or authenticate. Please check your praw.ini or environment variables: {e}")
        return

    posts_data = fetch_posts(reddit, args.subreddit, args.sort_type, args.limit)

    if posts_data and args.output_format != "none":
        output_filename_with_ext = args.output_file
        if not output_filename_with_ext.endswith(f".{args.output_format}"):
            output_filename_with_ext += f".{args.output_format}"

        if args.output_format == "json":
            save_to_json(posts_data, output_filename_with_ext)
        elif args.output_format == "csv":
            save_to_csv(posts_data, output_filename_with_ext)
        # No need for further logging here as save functions have their own
    elif not posts_data and args.output_format != "none":
        logging.info("No data fetched; skipping file saving.")


def save_to_json(data, filename):
    """Saves data to a JSON file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logging.info(f"Data successfully saved to {filename}")
    except IOError as e:
        logging.error(f"Error writing to JSON file {filename}: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while saving to JSON: {e}")

def save_to_csv(data, filename):
    """Saves data to a CSV file."""
    if not data:
        logging.info("No data to save to CSV.")
        return

    keys = data[0].keys() # Assumes all dicts have the same keys, which they do from fetch_posts
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        logging.info(f"Data successfully saved to {filename}")
    except IOError as e:
        logging.error(f"Error writing to CSV file {filename}: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while saving to CSV: {e}")


def fetch_posts(reddit, subreddit_name, sort_type, limit):
    """
    Fetches posts from a given subreddit and returns them as a list of dictionaries.
    """
    fetched_posts_data = []
    try:
        subreddit = reddit.subreddit(subreddit_name)
        logging.info(f"Fetching {limit} posts from r/{subreddit_name} sorted by '{sort_type}'...")

        if sort_type == "hot":
            submissions = subreddit.hot(limit=limit)
        elif sort_type == "new":
            submissions = subreddit.new(limit=limit)
        elif sort_type == "top":
            submissions = subreddit.top(limit=limit)
        elif sort_type == "controversial":
            submissions = subreddit.controversial(limit=limit)
        else: # Should not happen due to argparse choices
            logging.error(f"Invalid sort_type: {sort_type}. Defaulting to 'hot'.")
            submissions = subreddit.hot(limit=limit)

        count = 0
        for post in submissions:
            post_data = {
                "id": post.id,
                "title": post.title,
                "score": post.score,
                "url": post.url,
                "num_comments": post.num_comments,
                "created_utc": post.created_utc,
                "selftext": post.selftext
            }
            fetched_posts_data.append(post_data)

            # Log fetched post info
            logging.info("-" * 30)
            logging.info(f"Title: {post_data['title']}")
            logging.info(f"ID: {post_data['id']}")
            # Add other relevant logs if needed, or remove to reduce console noise if saving to file
            count += 1

        if count == 0:
            logging.info(f"No posts found for r/{subreddit_name} with the current filters.")
        else:
            logging.info(f"Successfully fetched {count} posts.")

        return fetched_posts_data

    except praw.exceptions.PRAWException as e:
        logging.error(f"PRAW error while fetching posts from r/{subreddit_name}: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while fetching posts: {e}")

    return fetched_posts_data # Return empty list in case of error after some posts might have been fetched


def fetch_reddit_trends():
    """
    Fetches the top 10 hot post titles from r/popular.
    This function is intended to be called programmatically (e.g., by a bot)
    and does not rely on command-line arguments.
    """
    logging.info("Fetching Reddit trends from r/popular...")
    trending_post_titles = []
    try:
        # Initialize PRAW. Ensure praw.ini or environment variables are set up.
        # Using a specific site_name 'bot1' as an example, matching the main script's approach.
        # Adjust if a different configuration is needed for programmatic access.
        reddit = praw.Reddit(site_name="bot1")

        # Verify authentication (optional, but good for debugging)
        user = reddit.user.me()
        if user:
            logging.debug(f"Authenticated for trends fetch as: {user}")
        else:
            logging.warning("Authenticated for trends fetch in read-only/anonymous mode.")

        popular_subreddit = reddit.subreddit("popular")
        hot_posts = popular_subreddit.hot(limit=10)

        for post in hot_posts:
            trending_post_titles.append(post.title)

        if not trending_post_titles:
            logging.info("No trending posts found or r/popular is inaccessible.")
        else:
            logging.info(f"Successfully fetched {len(trending_post_titles)} trending posts.")

    except praw.exceptions.PRAWException as e:
        logging.error(f"PRAW error while fetching Reddit trends: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while fetching Reddit trends: {e}")

    return trending_post_titles

if __name__ == "__main__":
    main()
    # Example usage of the new function (optional, for testing)
    # trends = fetch_reddit_trends()
    # if trends:
    #     print("\nTop Reddit Trends:")
    #     for i, title in enumerate(trends):
    #         print(f"{i+1}. {title}")
