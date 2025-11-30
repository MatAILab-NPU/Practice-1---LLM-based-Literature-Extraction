import os
import fitz  # PyMuPDF
import re
from tqdm import tqdm

# ========= 路径设置 =========
pdf_dir = "/data/wy/workT/literature_extraction/papers"    # 输入 PDF 文件夹
txt_dir = "/data/wy/workT/literature_extraction/papers"    # 输出 TXT 文件夹

os.makedirs(txt_dir, exist_ok=True)

# ========= PDF → 文本提取 =========
def pdf_to_text(pdf_path):
    """提取 PDF 文本"""
    text = ""
    try:
        doc = fitz.open(pdf_path)  # 打开 PDF 文件
        for page in doc:
            text += page.get_text("text")  # 提取纯文本
        doc.close()
    except Exception as e:
        print(f"❌ 无法读取 {pdf_path}：{e}")
    return text

# ========= 文本清洗 =========
def clean_text(text):
    """基础清洗：去页眉页脚、参考文献、空行等"""
    text = re.sub(r"Page \d+ of \d+", "", text)  # 删除页码
    text = re.sub(r"\n{3,}", "\n\n", text)       # 合并多余空行
    text = re.sub(r"\s{2,}", " ", text)          # 合并多余空格
    # 去掉 References 后的内容
    if "References" in text:
        text = text.split("References")[0]
    elif "REFERENCES" in text:
        text = text.split("REFERENCES")[0]
    return text.strip()

# ========= 主函数：批量处理 =========
def process_all_pdfs():
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
    for fn in tqdm(pdf_files, desc="Extracting and cleaning PDFs"):
        pdf_path = os.path.join(pdf_dir, fn)
        txt_path = os.path.join(txt_dir, fn.replace(".pdf", ".txt"))

        raw_text = pdf_to_text(pdf_path)
        cleaned_text = clean_text(raw_text)

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(cleaned_text)

    print(f"✅ 已处理 {len(pdf_files)} 篇 PDF，输出到 {txt_dir}/")


# ========= 程序入口 =========
if __name__ == "__main__": 
    process_all_pdfs()
