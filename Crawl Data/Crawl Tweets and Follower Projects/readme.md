# Twitter Projects Crawler

This project crawls Twitter to find Key Projects from a given list of their Twitter username. It fetches detailed user information and saves the results into a CSV file.

## Prerequisites
Before running the script, ensure you have the following:

- Python 3.7 or later installed.
- Pip package manager installed.

## Installation
Follow the steps below to set up your environment:

1. Clone the repository or download the script.

2. Install the required libraries by running the following commands:

   ```bash
   pip install tweety-ns
   pip install https://github.com/mahrtayyab/tweety/archive/main.zip --upgrade
   ```

## Usage

### Running the Script

To run the script, use the following command:

```bash
python twitter_projects_crawler.py -u YOUR_USERNAME -p PASSWORD
```

Replace `YOUR_USERNAME` with your Twitter username and `PASSWORD` with your Twitter password.

### Example

```bash
python twitter_projects_crawler.py -u my_twitter_username -p my_secure_password
```

### Output

- The script generates a CSV file named `twitter_KOLs.csv` containing the details of the KOLs found.
- If there are errors during the crawling process, they will be logged in the `crawl_KOLs_error.txt` file.

## Files Used

- `input_ids.csv`: Contains Twitter username of projects.


Ensure these files are in the same directory as the script and are properly populated.

## Notes

- Make sure your Twitter account credentials are correct to avoid login issues.
- Ensure your network connection is stable during the crawling process.
- This script is subject to Twitter's API usage policies and scraping limits.

## Support
If you encounter any issues or have questions, feel free to reach out or raise an issue on the project repository.

