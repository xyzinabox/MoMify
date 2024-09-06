# MoMify

MoMify is a simple command-line tool that records and summarizes your meetings for you with the help of AI. It only supports Windows at the moment and is fairly easy to setup.

## Setup

For any Python version >= 3.8, you can install MoMify with the following command:

    pip install -U momify

Additionally, in order to run the speech-to-text model, you need to have [`ffmpeg`](https://ffmpeg.org/) installed in your system:

    choco install ffmpeg

That's it!

## Usage

Open a terminal, select an application that you want to record (e.g. discord) and type the following command:

    momify discord

The first time you run it, it will need to fetch the necessary models and cache them for subsequent runs. 
You are ready to momify!