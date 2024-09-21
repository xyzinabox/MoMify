import os
import warnings
import logging

def summarize(text):

    from transformers import AutoModelForCausalLM, AutoTokenizer
    from torch.cuda import is_available
    from torch import float16, float32

    device = "cuda" if is_available() else "cpu"

    model = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen2-0.5B-Instruct",
        torch_dtype="auto",
        device_map=device
    )
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-0.5B-Instruct")

    prompt = """Summarize this transcription into meeting minutes. Please do not only have long paragraphs 
    for the summary. You can use bullet points for important notes like action items and meeting highlights. 
    The transcription: {text}""".format(text=text)

    messages = [
        {"role": "system", "content": "You are a helpful assistant that takes meeting minutes."},
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(device)

    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=512
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response
