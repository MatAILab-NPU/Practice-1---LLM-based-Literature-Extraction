import os
import json
import requests
from tqdm import tqdm
from dotenv import load_dotenv

# 1️⃣ 读取配置
load_dotenv()
api_key = os.getenv("API_KEY")              # 你的 SiliconFlow API 密钥
base_url = os.getenv("API_BASE_URL")        # 一般是 https://api.siliconflow.cn/v1
model_name = os.getenv("API_MODEL")         # 比如 deepseek-ai/DeepSeek-V3 或 Qwen/Qwen2.5-14B-Instruct

# 2️⃣ 创建 headers
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 3️⃣ 读取模板
with open("template.json", "r", encoding="utf-8") as f:
    template = f.read()

# 4️⃣ 创建输出文件夹
os.makedirs("outputs", exist_ok=True)

# 5️⃣ 遍历论文文件
for filename in tqdm(os.listdir("papers"), desc="Processing papers"):
    if not filename.endswith(".txt"):
        continue

    with open(os.path.join("papers", filename), "r", encoding="utf-8") as f:
        text = f.read()

    # 构造提示词（Prompt）
    prompt = f"""
你是一名材料科学文献分析助手，请根据以下论文内容，
按照模板提取关键信息并输出严格的 JSON 格式结果。
不要解释，不要多余说明，只输出 JSON。

【模板】
{template}

【论文文本】
{text}
"""

    # 6️⃣ 调用 SiliconFlow API
    try:
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.0,
            "max_tokens": 4096
        }

        response = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()["choices"][0]["message"]["content"]

            # 保存结果
            output_path = os.path.join("outputs", filename.replace(".txt", "_output.json"))
            with open(output_path, "w", encoding="utf-8") as out:
                out.write(result)
        else:
            print(f"❌ 处理 {filename} 时出错：Error code {response.status_code} - {response.text}")

    except Exception as e:
        print(f"❌ 处理 {filename} 时出错：{e}")

print("✅ 所有文献已处理完成！请查看 outputs/ 文件夹。")
