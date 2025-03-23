import torch
import os
import io
import gc
from io import BytesIO
from transformers import AutoModelForCausalLM, AutoTokenizer

device = "cuda"

class Qwen2_ModelLoader_Zho:
    def __init__(self):
        self.loaded = False
        self.m_name = "Qwen/Qwen2.5-3B-Instruct" #set a default model name to load
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_name": (["Qwen/Qwen2-7B-Instruct", "Qwen/Qwen2-72B-Instruct", "Qwen/Qwen2.5-0.5B-Instruct", "Qwen/Qwen2.5-1.5B-Instruct", "Qwen/Qwen2.5-3B-Instruct", "Qwen/Qwen2.5-7B-Instruct", "Qwen/Qwen2.5-14B-Instruct", "Qwen/Qwen2.5-32B-Instruct", "Qwen/Qwen2.5-72B-Instruct"],),
            }
        }

    RETURN_TYPES = ("QWEN2", "TK")
    RETURN_NAMES = ("qwen2", "tokenizer")
    FUNCTION = "load_model"
    CATEGORY = "⛱️Qwen2"
  
    def load_model(self, model_name):
        print("start load!")
        self.m_name = model_name
        try:
            model = AutoModelForCausalLM.from_pretrained(
                model_name, 
                device_map="auto", 
                torch_dtype="auto", 
            )
            tokenizer = AutoTokenizer.from_pretrained(model_name)

            # Store for unloading
            self.model = model
            self.loaded = True
            return (self, tokenizer)
        except Exception as e:
            print(f"Failed to load Qwen2 model: {e}")
            raise

    def reload_model(self):
        print("start reload!")
        self.load_model(self.m_name)

    def unload_model(self):
        if hasattr(self, "model") and self.model is not None:
            print("has model loaded. now will start the unload")
            try:
                if isinstance(self.model, torch.nn.Module):
                    # Check the device of the model's parameters
                    param = next(self.model.parameters(), None)
                    if param is not None:
                        device = param.device
                        print(f"Model is on device: {device}")
                    else:
                        print("Model has no parameters")
                else:
                    print("self.model is not a PyTorch model, skipping")

                # Remove reference
                del self.model
                print("self.model deleted")
                self.model = None

                # Clear CUDA cache if applicable
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                    print("cuda.empty_cache done")
                else:
                    print("CUDA not available, skipping cache clear")

                gc.collect()
                self.loaded = False
                print("Qwen2 model unloaded")
            except Exception as e:
                print(f"Error during unload_model: {e}")
        else:
            print("No model to unload")
        return self


class Qwen2_Zho:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "qwen2": ("QWEN2",),
                "tokenizer": ("TK",),
                "prompt": ("STRING", {"default": "What is the meaning of life?", "multiline": True}),
                "system_instruction": ("STRING", {"default": "You are creating a prompt for Stable Diffusion to generate an image. First step: understand the input and generate a text prompt for the input. Second step: only respond in English with the prompt itself in phrase, but embellish it as needed but keep it under 200 tokens.", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "generate_content"

    CATEGORY = "⛱️Qwen2"


    def generate_content(self, qwen2, tokenizer, prompt, system_instruction):
        if not qwen2.loaded:
            qwen2.reload_model()
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

        generated_ids = qwen2.model.generate(
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
                "qwen2": ("QWEN2",),
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

    def generate_content(self, qwen2, tokenizer, prompt, system_instruction):
        if not qwen2.loaded:
            qwen2.reload_model()
        # Store model, tokenizer, and temperature as instance variables
        self.model = qwen2.model
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

class Qwen2_UnloadModel:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "qwen2": ("QWEN2",),
                "text": ("STRING", {"multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "unload"

    CATEGORY = "⛱️Qwen2"
    
    def unload(self, text, qwen2):
        print("Unload Qwen2 Model:")
        if qwen2 is not None and qwen2.loaded and text is not None:
            print(f"generated prompt is: {text}")
            try:
                qwen2.unload_model()
            except Exception as e:
                print(f"Failed to off-load Qwen2 model: {e}")
        return (text,)
        

NODE_CLASS_MAPPINGS = {
    "Qwen2_ModelLoader_Zho": Qwen2_ModelLoader_Zho,
    "Qwen2_Zho": Qwen2_Zho,
    "Qwen2_Chat_Zho": Qwen2_Chat_Zho,
    "Qwen2_UnloadModel": Qwen2_UnloadModel,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Qwen2_ModelLoader_Zho": "⛱️Qwen2 ModelLoader",
    "Qwen2_Zho": "⛱️Qwen2",
    "Qwen2_Chat_Zho": "⛱️Qwen2 Chat",
    "Qwen2_UnloadModel": "⛱️Qwen2 Unload model"
}
