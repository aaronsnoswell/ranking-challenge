import os
import json
from datetime import datetime
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

from persistence import ScraperData, ScraperErrors, persist_data, persist_error, ensure_tables

DB_FILE_PATH = os.getenv('DB_FILE_PATH')

app = FastAPI(
    title="Scraper ingester",
    description="Basic API for ingesting results from a scraper.",
    version="0.1.0",
)

@app.on_event("startup")
async def initialize_persistence():
    ensure_tables()


class SuccessData(BaseModel):

    content_items: list[dict] = Field(
        description="The content items that were scraped.",
    )

class ErrorData(BaseModel):

    message: str = Field(
        description="The error message if the scrape was unsuccessful.",
    )

class IngestData(BaseModel):

    success: bool = Field(
        description="Whether the scrape was successful.",
    )
    task_id: str = Field(
        description="ID or label that uniquely identifies the scrape task.",
    )
    timestamp: datetime = Field(
        description="The timestamp of the scrape.",
    )
    data: Optional[SuccessData] = Field(default=None)
    error: Optional[ErrorData] = Field(default=None)


@app.post("/data/scraper")
def ingest_scrape_data(data: IngestData):
    if not DB_FILE_PATH:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="DB_FILE_PATH not set.")
    if data.success:
        if not data.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Success data missing.")
        process_success(data.task_id, data.timestamp, data.data.content_items)
    else:
        if not data.error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error data missing.")
        process_error(data.task_id, data.timestamp, data.error.message)

@app.get("/")
def health_check():
    return {"status": "ok"}

def process_success(task_id: str, timestamp: datetime, results: list[dict]):
    logger.info(f"Received results for {task_id} completed at {timestamp}: length={len(results)}")
    rows = [
        ScraperData(
            post_id=result['id_str'],
            source_id='twitter',
            task_id=task_id,
            post_blob=json.dumps(result)
        )
        for result in results
    ]
    persist_data(rows)


def process_error(task_id: str, timestamp: datetime, message: str):
    logger.info(f"Received error for {task_id} completed at {timestamp}: {message}")
    persist_error(
        ScraperErrors(
            source_id='twitter',
            task_id=task_id,
            message=message)
    )
