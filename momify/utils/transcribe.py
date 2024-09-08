import os
import warnings
import logging

os.environ['USE_FLASH_ATTENTION'] = '0'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

def transcribe(audio_file):

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
    result = pipe(audio_file)
    return result["text"]
