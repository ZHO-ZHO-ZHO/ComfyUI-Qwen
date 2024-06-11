
![qwen2](https://github.com/ZHO-ZHO-ZHO/ComfyUI-Qwen-2/assets/140084057/f6f2593e-7794-4c6a-a594-491d4457700b)

<h1 align="center">Qwen-2 in ComfyUI</h1>

![screenshot-20240612-002830](https://github.com/ZHO-ZHO-ZHO/ComfyUI-Qwen-2/assets/140084057/4c4fa10b-9beb-402a-b281-d4c6c4bfb5a7)


## 项目介绍 | Info

- 将 [Qwen2](https://github.com/QwenLM/Qwen2) 模型引入到 ComfyUI 中，目前支持 Qwen2-7B-Instruct 和 Qwen2-72B-Instruct 双模型，速度快且性能强，中文表现很不错，可用于 生成/补全提示词 或畅聊人生！

- 版本：V1.0 支持系统提示词，支持单/多轮对话双模式，支持中文输入自动并输出英文提示词



## 详细说明 | Features

- 节点:

   - ⛱️Qwen2 ModelLoader：会自动下载模型（请保持网络畅通），Qwen2-7B-Instruct 约 16G（所需 VRAM > 12GB），Qwen2-72B-Instruct 约 160G（所需 VRAM > 24GB）
     
   - ⛱️Qwen2：支持系统指令设置（System Instruction）     

   - ⛱️Qwen2 Chat：支持系统指令设置（System Instruction）+ 多轮对话
  

- 节点示例：

![screenshot-20240611-235613](https://github.com/ZHO-ZHO-ZHO/ComfyUI-Qwen-2/assets/140084057/2338eac7-1858-49b7-996a-8607ab5b5bd4)



- 上下文多轮对话：

![screenshot-20240611-234410](https://github.com/ZHO-ZHO-ZHO/ComfyUI-Qwen-2/assets/140084057/b3e9dcb6-115a-48cb-b771-d46f0ddb76a4)




## 参数说明 | Parameters

- model：接入模型
- tokenizer：分词器
- prompt：提示词
- system_instruction：系统指令


## 安装 | Install

- 环境依赖要求：transformers>=4.40.0，手动升级：`pip uninstall -y transformers && pip install git+https://github.com/huggingface/transformers`

- 推荐使用管理器 ComfyUI Manager 安装（ON THE WAY）

- 手动安装：
    1. `cd custom_nodes`
    2. `git clone https://github.com/ZHO-ZHO-ZHO/ComfyUI-Qwen-2.git`
    3. `cd custom_nodes/ComfyUI-Qwen-2`
    4. `pip install -r requirements.txt`
    5. 重启 ComfyUI

- 输出节点可配合像[ComfyUI-Gemini](https://github.com/ZHO-ZHO-ZHO/ComfyUI-Gemini)中 ✨DisplayText_Zho 一样的任何接受文本的节点


## 工作流 | Workflow

### V1.0 工作流

  [Qwen2 + CosXL【Zho】](https://github.com/ZHO-ZHO-ZHO/ComfyUI-Qwen-2/blob/main/QWEN2%20WORKFLOWS/Qwen2%20%2B%20CosXL%E3%80%90Zho%E3%80%91.json)

  ![screenshot-20240612-000459](https://github.com/ZHO-ZHO-ZHO/ComfyUI-Qwen-2/assets/140084057/9f130967-b066-45f9-8897-94c167094ee3)


  [Qwen2 Chat【Zho】](https://github.com/ZHO-ZHO-ZHO/ComfyUI-Qwen-2/blob/main/QWEN2%20WORKFLOWS/Qwen2%20Chat%E3%80%90Zho%E3%80%91.json)

  ![screenshot-20240612-003348](https://github.com/ZHO-ZHO-ZHO/ComfyUI-Qwen-2/assets/140084057/e684ffdd-725e-4e82-a418-012eaec06125)





## 更新日志 | Changelog

20240611

- V1.0： 支持系统提示词，支持单/多轮对话双模式，支持中文输入自动并输出英文提示词

- 创建项目


## Stars 

[![Star History Chart](https://api.star-history.com/svg?repos=ZHO-ZHO-ZHO/ComfyUI-Qwen-2&type=Timeline)](https://star-history.com/#ZHO-ZHO-ZHO/ComfyUI-Qwen-2&Timeline)


## 关于我 | About me

📬 **联系我**：
- 邮箱：zhozho3965@gmail.com
- QQ 群：839821928

🔗 **社交媒体**：
- 个人页：[-Zho-](https://jike.city/zho)
- Bilibili：[我的B站主页](https://space.bilibili.com/484366804)
- X（Twitter）：[我的Twitter](https://twitter.com/ZHOZHO672070)
- 小红书：[我的小红书主页](https://www.xiaohongshu.com/user/profile/63f11530000000001001e0c8?xhsshare=CopyLink&appuid=63f11530000000001001e0c8&apptime=1690528872)

💡 **支持我**：
- B站：[B站充电](https://space.bilibili.com/484366804)
- 爱发电：[为我充电](https://afdian.net/a/ZHOZHO)


## Credits

[Qwen2](https://github.com/QwenLM/Qwen2)
