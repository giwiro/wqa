#!/usr/bin/env python3
import argparse
import json
import os
import html
import unicodedata
from multiprocessing.pool import Pool as ProcessPool
from typing import Dict, Optional

import re
from tqdm import tqdm

from wqa.database import DatabaseFactory

# Create specific Database type, which hold the default uri
Database = DatabaseFactory.get_class("mongo")


def get_files_gen(data_path: str):
    if os.path.isfile(data_path):
        yield data_path
    elif os.path.isdir(data_path):
        for dir_path, _, files in os.walk(data_path):
            for f in files:
                yield os.path.join(dir_path, f)
    else:
        raise RuntimeError(f"Path {data_path} is invalid")


def process_doc(doc: Dict) -> Optional[Dict[str, str]]:
    new_doc = {"title": doc.get("title"), "text": doc.get("text")}
    # if it's a disambiguation article then ignore it
    if '(desambiguación)' in new_doc.get("title").lower():
        return None
    if '(página de desambiguación)' in new_doc.get("title").lower():
        return None

    # If title contains some link stuff, then ignore it
    # if regex.match(r'(List of .+)|(Index of .+)|(Outline of .+)',
    #               new_doc.get("title")):
    #     return None
    if '(list' in new_doc.get("title").lower():
        print(f"Lista :D: {new_doc.get('title').lower()}")
    # Apply Normalization Form Canonical Decomposition to remove special
    # chars from title
    new_doc["title"] = unicodedata.normalize("NFD", new_doc.get("title"))
    # Unescape some chars (as &gt; &#62; &#x3e;)
    for key, value in new_doc.items():
        new_doc[key] = html.unescape(value)
    return new_doc


def worker_job(file_name: str) -> [Dict[str, str]]:
    docs = []
    with open(file_name) as file:
        for l in file:
            doc = json.loads(l)
            if not doc:
                continue
            processed_doc = process_doc(doc)
            if not processed_doc:
                continue
            # t = (processed_doc.get("title"), processed_doc.get("text"))
            d = {"title": processed_doc.get("title"),
                 "text": processed_doc.get("text")}
            docs.append(d)
    return docs


def persist_corpus(data_path: str, uri: str, processes: int):
    ppool = ProcessPool(processes)
    insert_documents = []
    file_names = [file_name for file_name in get_files_gen(data_path)]

    with Database(uri) as session:
        session.drop_db()
        session.create_db()

        session.start_transaction()

        with tqdm(total=len(file_names)) as progress:
            for docs in tqdm(ppool.imap_unordered(worker_job, file_names)):
                # insert_documents.extend(docs)
                session.insert_many(docs)
                progress.update()

    # inserted = db.insert_many(insert_documents)
    # print(inserted)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True,
                        help="Data folder path")
    parser.add_argument("--db-uri", type=str, default=Database.default_uri,
                        help="Full uri of the database")
    parser.add_argument("--processes", type=int, default=10,
                        help="Numbers of processes in the pool")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    persist_corpus(args.data, args.db_uri, args.processes)
