import os
import typer
import logging
import warnings

from typing_extensions import Annotated

from momify.loopback.record import record

os.environ['USE_FLASH_ATTENTION'] = '0'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

def momify(
    name: Annotated[str, typer.Argument(help="The name of the process that you want recorded.")],
    output_dir: Annotated[str, typer.Option("--output-dir", "-o", help="Directory for the output of the process.")] = "results",
    duration: Annotated[int, typer.Option("--duration", "-d", help='''Duration of recording in minutes. 
                                          Zero indicates infinite duration''')] = 0,
):
    path = record(name, duration, output_dir)
    print("Loading S2T Model...")
    
    from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
    from torch.cuda import is_available
    from torch import float16, float32
    
    warnings.filterwarnings("ignore")
    logging.getLogger("transformers").setLevel(logging.CRITICAL)

    device = "cuda" if is_available() else "cpu"
    torch_dtype = float16 if is_available() else float32
    model_id = "openai/whisper-large-v3"

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        torch_dtype=torch_dtype,
        device=device,
        generate_kwargs={"language": "english", "forced_decoder_ids": None}
    )
    print("Generating text...")
    result = pipe(path)
    print(result["text"])

    with open(f"{output_dir}/text", "w") as f:
        f.write(result["text"])

    print("Summarizing...")