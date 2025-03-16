import pandas as pd
import requests 
from loguru import logger
import time
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from bs4 import BeautifulSoup


# Load the idiom lexicon from TSV file
df = pd.read_csv('scripts/corpus/slide/idiomLexicon.tsv', sep='\t')


"""
               Idiom                                     WiktionaryURL  Pos  Neg  Neu  ...  %Pos  %Neg  %Neu  Maj. Label  FilterOut(X)
0     American Dream     https://en.wiktionary.org/wiki/American_Dream    8    0    2  ...   0.8   0.0   0.2    positive           NaN
1           Catch-22           https://en.wiktionary.org/wiki/Catch-22    0    7    3  ...   0.0   0.7   0.3    negative           NaN
2  Christmas present  https://en.wiktionary.org/wiki/Christmas_present    6    0    4  ...   0.6   0.0   0.4    positive
"""
# Drop all columns except Idiom and WiktionaryURL
df = df[['Idiom', 'WiktionaryURL']]

# Log total number of idioms
logger.info(f"Total number of idioms in lexicon: {len(df)}")


# Rename WiktionaryURL column to Url
df = df.rename(columns={'WiktionaryURL': 'URL'})

# Initialize content column with None values
df['text'] = None
# Initialize html column with None values
df['raw'] = None

# Function to fetch content for a single idiom
def fetch_idiom_content(idx_row):
    idx, row = idx_row
    idiom, url = row['Idiom'], row['URL']
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # Store the raw HTML
            raw = response.text
            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract just the text content, removing all HTML tags
            text = soup.get_text(separator=' ', strip=True)
            logger.debug(f"Successfully fetched {idiom} from {url}")
            return idx, text, raw
        else:
            logger.error(f"Failed to fetch {idiom} from {url} with status code {response.status_code}")
            return idx, None, None
    except Exception as e:
        logger.error(f"Error fetching {idiom} from {url}: {str(e)}")
        return idx, None, None

# Concurrent fetching with ThreadPoolExecutor
max_workers = 80  # Process 100 requests concurrently
total_idioms = len(df)

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    # Submit all tasks and create a list of futures
    future_to_idx = {executor.submit(fetch_idiom_content, (i, row)): i 
                     for i, row in df.iterrows()}
    
    # Process results as they complete with tqdm progress bar
    for future in tqdm(future_to_idx, total=total_idioms, desc="Fetching idioms"):
        try:
            idx, text, raw = future.result()
            if text:
                df.at[idx, 'text'] = text
            if raw:
                df.at[idx, 'raw'] = raw
        except Exception as e:
            logger.error(f"Exception while processing result: {str(e)}")

# Save the updated dataframe
output_file = 'scripts/corpus/slide/idiomLexicon_fetched.tsv'
df.to_csv(output_file, sep='\t', index=False)
logger.info(f"Saved updated lexicon to {output_file}")

# Log statistics
successful_fetches = df['text'].notna().sum()
logger.info(f"Successfully fetched {successful_fetches} out of {len(df)} idioms")


