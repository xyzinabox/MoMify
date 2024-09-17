import typer
from typing_extensions import Annotated

from momify.loopback.record import record
from momify.utils import transcribe, summarize
from pathlib import Path

def momify(
    name: Annotated[str, typer.Argument(help="The name of the process that you want recorded.")],
    output_dir: Annotated[str, typer.Option("--output-dir", "-o", help="Directory for the output of the process.")] = "results",
    duration: Annotated[int, typer.Option("--duration", "-d", help='''Duration of recording in minutes. 
                                          Zero indicates infinite duration''')] = 0,
    audio_file: Annotated[str, typer.Option("--audio-file", "-a", help="Path to audio file that you want processed.")] = "",
    text_file: Annotated[str, typer.Option("--text-file", "-t", help="Path to text file that you want summarized.")] = "",
    record_only: Annotated[bool, typer.Option("--record-only", help="Disable transcription and summarization.")] = False,
    no_summary: Annotated[bool, typer.Option("--no-summary", help="Disable summarization.")] = False,
):  
    
    if text_file:
        with open(text_file,"r") as file:
            text = file.read()
            
        summary = summarize(text)

        with open(f"{output_dir}/summary_text", "w") as f:
            f.write(summary)
        return
        

    if not audio_file:
        audio_file = record(name, duration, output_dir)
    
    if record_only:
        return
    
    text = transcribe(audio_file)
    print(text)
    with open(f"{output_dir}/text", "w") as f:
        f.write(text)

    if no_summary:
        return
    
    # SUMMARIZE
    summary = summarize(text)

    with open(f"{output_dir}/summary_text" "w") as f:
        f.write(summary)