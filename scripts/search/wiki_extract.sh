#!/usr/bin/env sh

FOLDER_NAME="wikiextractor"
REPO="https://github.com/attardi/wikiextractor.git"
EXTRACTOR_COMMAND="WikiExtractor.py"

DATASET_FILE_NAME="eswiki-latest-pages-articles.xml.bz2"
DATASET_URL="https://dumps.wikimedia.org/eswiki/latest/$DATASET_FILE"
DATASET_FOLDER_NAME="dataset/eswiki/"
DATASET_OUTPUT_FOLDER_NAME="dataset/eswiki/extracted"

if ! [ -x "$(command -v git)" ]; then
    echo "[ERROR] Command 'git' not found :'("
    exit 1
fi

if ! [ -x "$(command -v $EXTRACTOR_COMMAND)" ]; then
    git clone $REPO $FOLDER_NAME
    cd $FOLDER_NAME
    if ! (python3 setup.py install) ; then
        echo "[ERROR] Could not install '$EXTRACTOR_COMMAND'"
        exit 1
    fi
    cd ..
    rm -rf $FOLDER_NAME
    echo "[SUCCESS] Installing '$EXTRACTOR_COMMAND' completed"
fi

if [ ! -f "$DATASET_FOLDER_NAME$DATASET_FILE_NAME" ]; then
    echo "[ERROR] Dataset: $DATASET_FILE_NAME"
    echo "        was not found on directory: $DATASET_FOLDER_NAME"
    echo "Please download it from: $DATASET_URL"
    exit 1
fi

$EXTRACTOR_COMMAND --processes=3 --json --output="$DATASET_OUTPUT_FOLDER_NAME" "$DATASET_FOLDER_NAME$DATASET_FILE_NAME"


