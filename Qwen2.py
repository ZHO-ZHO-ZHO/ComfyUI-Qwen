import torch
import os
import io
from io import BytesIO
from transformers import AutoModelForCausalLM, AutoTokenizer

device = "cuda"

class Qwen2_ModelLoader_Zho:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_name": (["Qwen/Qwen2-7B-Instruct", "Qwen/Qwen2-72B-Instruct", "Qwen/Qwen2.5-0.5B-Instruct", "Qwen/Qwen2.5-1.5B-Instruct", "Qwen/Qwen2.5-3B-Instruct", "Qwen/Qwen2.5-7B-Instruct", "Qwen/Qwen2.5-14B-Instruct", "Qwen/Qwen2.5-32B-Instruct", "Qwen/Qwen2.5-72B-Instruct"],),
            }
        }

    RETURN_TYPES = ("QWEN2", "TK")
    RETURN_NAMES = ("Qwen2", "tokenizer")
    FUNCTION = "load_model"
    CATEGORY = "⛱️Qwen2"
  
    def load_model(self, model_name):
        model = AutoModelForCausalLM.from_pretrained(
            model_name, 
            device_map="cuda", 
            torch_dtype="auto", 
        )
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        return model, tokenizer


class Qwen2_Zho:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("QWEN2",),
                "tokenizer": ("TK",),
                "prompt": ("STRING", {"default": "What is the meaning of life?", "multiline": True}),
                "system_instruction": ("STRING", {"default": "You are creating a prompt for Stable Diffusion to generate an image. First step: understand the input and generate a text prompt for the input. Second step: only respond in English with the prompt itself in phrase, but embellish it as needed but keep it under 200 tokens.", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "generate_content"

    CATEGORY = "⛱️Qwen2"


    def generate_content(self, model, tokenizer, prompt, system_instruction):

        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt},
        ]

        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = tokenizer([text], return_tensors="pt").to(device)

        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=512
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

        return (response,)


class Qwen2_Chat_Zho:
    def __init__(self):
        self.chat_history = []

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("QWEN2",),
                "tokenizer": ("TK",),
                "prompt": ("STRING", {"default": "What is the meaning of life?", "multiline": True}),
                "system_instruction": ("STRING", {"default": "You are creating a prompt for Stable Diffusion to generate an image. First step: understand the input and generate a text prompt for the input. Second step: only respond in English with the prompt itself in phrase, but embellish it as needed but keep it under 200 tokens.", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "generate_content"

    CATEGORY = "⛱️Qwen2"

    def qwen_2(self, user_question, system_role):
        messages = [{"role": "system", "content": system_role},
                    {"role": "user", "content": user_question}]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(device)

        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=512
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

        return response

    def generate_content(self, model, tokenizer, prompt, system_instruction):
        # Store model, tokenizer, and temperature as instance variables
        self.model = model
        self.tokenizer = tokenizer

        # Generate response and update chat history
        response = self.qwen_2(prompt, system_instruction)
        self.chat_history.append({"role": "user", "content": prompt})
        self.chat_history.append({"role": "system", "content": response})
        
        # Format and return chat history
        formatted_history = self.format_chat_history()
        return (formatted_history,)

    def format_chat_history(self):
        formatted_history = []
        for message in self.chat_history:
            formatted_message = f"{message['role']}: {message['content']}"
            formatted_history.append(formatted_message)
            formatted_history.append("-" * 40)  # Add a separator line
        return "\n".join(formatted_history)

        

NODE_CLASS_MAPPINGS = {
    "Qwen2_ModelLoader_Zho": Qwen2_ModelLoader_Zho,
    "Qwen2_Zho": Qwen2_Zho,
    "Qwen2_Chat_Zho": Qwen2_Chat_Zho,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Qwen2_ModelLoader_Zho": "⛱️Qwen2 ModelLoader",
    "Qwen2_Zho": "⛱️Qwen2",
    "Qwen2_Chat_Zho": "⛱️Qwen2 Chat",
}
