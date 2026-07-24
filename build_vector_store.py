import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
import re
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# 设置 Hugging Face 镜像（如果你还没设置，在这里加上）

# ========== 配置区 ==========
# 你的 docx 文件存放目录（可放多个文件）
DOCS_DIR = r"E:\红色文化实践探索赛备赛项目\RAG数据库\data"          # 请改为你存放 docx 的实际路径
# 向量库保存目录
VECTOR_STORE_DIR = "./chroma_db"

# ========== 1. 加载文档 ==========
def load_documents(directory):
    """加载目录下所有 .docx 文件"""
    docs = []
    for file in os.listdir(directory):
        if file.endswith(".docx"):
            file_path = os.path.join(directory, file)
            print(f"正在加载: {file}")
            loader = Docx2txtLoader(file_path)
            docs.extend(loader.load())
    return docs

print("📂 开始加载 docx 文档...")
documents = load_documents(DOCS_DIR)
print(f"✅ 共加载了 {len(documents)} 个文档片段")

# ========== 2. 文本分割 ==========
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,          # 每块最多500个字符
    chunk_overlap=50,        # 块间重叠50字符，保证上下文连贯
    separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]
)

chunks = text_splitter.split_documents(documents)
print(f"✂️ 分割为 {len(chunks)} 个文本块")

# ========== 3. 加载嵌入模型 ==========
print("🧠 正在加载嵌入模型（首次会下载，稍等片刻）...")
embeddings = HuggingFaceEmbeddings(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)

# ========== 4. 向量化并存入 ChromaDB ==========
print("💾 正在生成向量并存入 ChromaDB...")
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=VECTOR_STORE_DIR
)
vector_store.persist()  # 保存到磁盘
print(f"✅ 向量库已保存至 {VECTOR_STORE_DIR}")

# ========== 5. 简单测试 ==========
print("\n🔍 测试检索：输入一个关于毛泽东的问题")
retriever = vector_store.as_retriever(search_kwargs={"k": 3})
test_query = "毛泽东在井冈山时期提出了什么重要思想？"
results = retriever.invoke(test_query)
print(f"📄 检索到 {len(results)} 个相关片段：")
for i, doc in enumerate(results):
    print(f"\n--- 片段 {i+1} ---")
    print(doc.page_content[:200] + "...")