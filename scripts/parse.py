import pandas as pd
from loguru import logger
from dotenv import load_dotenv
import json
load_dotenv(".env.local")

df = pd.read_csv('scripts/corpus/slide/idiomLexicon_fetched.tsv', sep='\t')

# Log initial number of rows
logger.info(f"Initial number of rows: {len(df)}")

# Drop rows where content is null
df = df.dropna(subset=['raw'])

# Log number of rows after dropping nulls
logger.info(f"Number of rows after dropping nulls: {len(df)}")


from pydantic import BaseModel, Field



class Sense(BaseModel):
    content: str = Field(description="The definition of the sense (do not parapharse - just repeat the definition as it is layed out in the text).")
    # examples: list[str] = Field(description="Examples of the sense. Abbreviate the examples to a single sentence. Leave it as an empty list if there are no examples.")


class ParseResponse(BaseModel):
    senses: list[Sense] = Field(description="The senses of the phrase. There could be more than one sense.")
    etymology: str | None = Field(description="The etymology of the phrase. Set this to null if no etymology is present.")


from openai import AsyncOpenAI
import math
from openai import ContentFilterFinishReasonError

PARSE_PROMPT = """
### RAW TEXT ###
{raw}
---
Find the requested information for the phrase "{phrase}" from the above raw text.
"""

# Initialize OpenAI client
aclient = AsyncOpenAI()
from loguru import logger
from pprint import pformat

async def parse(text: str, phrase: str) -> dict:
    try:
        response = await aclient.beta.chat.completions.parse(
            model="gpt-4o-mini",
            response_format=ParseResponse,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that parses text for information about idioms. Keep your answer short and sweet."},
                {"role": "user", "content": PARSE_PROMPT.format(raw=text, phrase=phrase)}
            ]
        )
        parse_response = response.choices[0].message.parsed
        logger.info(f"Response for {phrase}:\n {pformat(parse_response.model_dump())}")
        return {
            "phrase": phrase,
            "response": parse_response.model_dump()
        }
    except ContentFilterFinishReasonError as e:
        logger.warning(f"Content filter rejected request for phrase '{phrase}': {str(e)}")
        return {
            "phrase": phrase,
            "response": None
        }
    except Exception as e:
        logger.error(f"Unexpected error processing phrase '{phrase}': {str(e)}")
        raise  # Re-raise unexpected errors

import asyncio

import yaml

async def process(df: pd.DataFrame, bnum: int, yaml_path: str):
    tasks = []
    for _, row in df.iterrows():
        phrase, text = row['Idiom'], row['text']
        tasks.append(parse(text, phrase))
    responses = await asyncio.gather(*tasks)
    logger.info(f"Persisting batch {bnum} to yaml at: {yaml_path}")
    with open(yaml_path, 'w') as fh:
        yaml.dump(responses, fh, allow_unicode=True)

# Split the dataframe into three roughly equal parts
BATCH_COUNT = 1000
total_rows = len(df)
batch_size = math.ceil(total_rows / BATCH_COUNT)

logger.info(f"Splitting dataframe with {total_rows} rows into {BATCH_COUNT} batches of approximately {batch_size} rows each")

from tqdm import tqdm
import os
# Process each batch
for i in tqdm(range(BATCH_COUNT)):
    start_idx = i * batch_size
    end_idx = min((i + 1) * batch_size, total_rows)
    bdf = df.iloc[start_idx:end_idx].copy()
    logger.info(f"Processing batch {i+1}: rows {start_idx} to {end_idx-1} (total: {len(bdf)} rows)")
    yaml_path = f'scripts/corpus/slide/parsed/batch-{i+1}.yaml'
    if os.path.exists(yaml_path):
        logger.info(f"Skipping batch {i+1} because it already exists at {yaml_path}")
        continue
    asyncio.run(process(bdf, i+1, yaml_path))



