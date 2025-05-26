# ABDUL-QASSIM

This repository contains example scripts for working with your own
ChatGPT data and local text notes. The goal is to experiment with a
completely offline workflow where a custom bot can answer questions
using your personal knowledge base.

## Getting your ChatGPT history

1. In ChatGPT, open **Settings & Beta** → **Data Controls**.
2. Choose **Export Data**. You will receive a ZIP archive containing a
   JSON file with your conversation history.
3. Unzip the archive and note the path to the `*.json` file.

To convert the exported history into individual text files, run:

```bash
python scripts/parse_history.py path/to/conversations.json history/
```

This will create one text file per conversation under the `history/`
directory.

## Using your own notes

Place any `.txt` files you want the bot to reference inside a directory,
e.g. `notes/`. Each file can contain sentences or bullet points.

The `offline_bot.py` script performs a very simple keyword search across
those files:

```bash
python scripts/offline_bot.py notes "your question here"
```

The script prints the sentences that match all the keywords in your
question. This is only a starting point. You can extend it with a local
language model or embedding-based search to improve the quality of the
answers.

## Custom training

If you wish to build a more advanced model, you can fine-tune an
open-source language model (such as LLaMA, GPT-J, or similar) using your
own dataset. The exported conversations and your notes can serve as the
training data. Refer to the documentation of the model you choose for
fine-tuning instructions.

These scripts are intentionally lightweight so they can run without any
network connection once the required Python packages are installed.
