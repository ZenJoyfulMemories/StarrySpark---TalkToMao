import shutil
import os
# ========== 设置镜像源 ==========
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
import random
import uuid
import edge_tts
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import Ollama

# ========== 项目根目录（绝对路径） ==========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ========== 设置镜像源 ==========
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

# ========== Flask 应用初始化 ==========
app = Flask(__name__)
CORS(app)  # 允许跨域

# ========== 音频目录（基于 BASE_DIR） ==========
AUDIO_DIR = os.path.join(BASE_DIR, 'static', 'audio')
os.makedirs(AUDIO_DIR, exist_ok=True)

# 启动时清理旧音频文件
if os.path.exists(AUDIO_DIR):
    shutil.rmtree(AUDIO_DIR)
os.makedirs(AUDIO_DIR, exist_ok=True)

# ========== 自我介绍多版本 ==========
INTRO_VERSIONS = [
    """我是毛泽东。
湖南湘潭韶山人，生于1893年。
我这一生，参与了创建中国共产党，领导了秋收起义，建立了井冈山革命根据地，走过了两万五千里长征，带领中国人民打败了日本侵略者，推翻了国民党反动统治，建立了新中国。
我始终相信：人民，只有人民，才是创造世界历史的动力。""",

    """我是毛泽东，字润之。
我来自湖南湘潭韶山，一个普通的农民家庭。
我创建了中国共产党，领导了秋收起义，在井冈山点燃了星星之火，走过了二万五千里长征，最终带领中国人民建立了新中国。
我常说：为人民服务。
你愿意的话，叫我一声毛委员也行。""",

    """我是毛泽东。
1893年生于湖南韶山，一个山清水秀的地方。
我一生致力于民族独立和人民解放，参与了党的创立，领导了秋收起义，建立了第一个农村革命根据地，经历了长征的艰难险阻，最终迎来了新中国的诞生。
我深信：星星之火，可以燎原。""",

    """我是毛泽东。
我是中国共产党的创始人之一，是中国人民解放军的缔造者之一，也是中华人民共和国的主要缔造者。
我领导了秋收起义，开辟了井冈山道路，走过了长征，打败了日本侵略者和国民党反动派，建立了新中国。
我最大的心愿就是看到人民过上幸福生活。
叫我毛委员就好，亲切些。""",

    """我是毛泽东同志。
我出生在湖南韶山的一个农民家庭，从小目睹了百姓的苦难。
我立志要改变这个国家，让所有人都有饭吃、有衣穿。
我参与了创建中国共产党，领导了秋收起义，建立了井冈山革命根据地，走过了长征，最终建立了新中国。
我常说：世界是你们的，也是我们的，但归根结底是你们的。
你今年多大了？年轻人要朝气蓬勃啊！"""
]

# ========== 路由 ==========
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/audio/<filename>')
def serve_audio(filename):
    return send_from_directory(AUDIO_DIR, filename)

@app.route('/ping')
def ping():
    return jsonify({'status': 'ok'})

# ========== 全局变量（启动时加载一次，提高响应速度） ==========
print("🔄 服务器启动中，正在加载模型与向量库...")
embeddings = HuggingFaceEmbeddings(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)

# 向量数据库路径（基于 BASE_DIR）
VECTOR_STORE_DIR = os.path.join(BASE_DIR, 'chroma_db')
vector_store = Chroma(
    persist_directory=VECTOR_STORE_DIR,
    embedding_function=embeddings
)
retriever = vector_store.as_retriever(search_kwargs={"k": 4})

llm = Ollama(
    model="EntropyYue/chatglm3:6b",
    temperature=0.3,
    top_p=0.9,
)
print("✅ 所有组件加载完成！服务器已就绪。")

# ========== API 路由：处理聊天请求 ==========
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_query = data.get('message', '').strip()
        history = data.get('history', [])
        
        if not user_query:
            return jsonify({'error': '请输入问题'}), 400

        # 特殊处理“你是谁”
        keywords = ['你是谁', '介绍一下', '自我介绍']
        if any(kw in user_query for kw in keywords):
            intro = random.choice(INTRO_VERSIONS)
            return jsonify({'response': intro})

        # 格式化历史记录
        history_str = ""
        recent_history = history[-10:] if len(history) > 10 else history
        for turn in recent_history:
            if turn['role'] == 'user':
                history_str += f"用户: {turn['content']}\n"
            else:
                history_str += f"毛泽东: {turn['content']}\n"
        
        # RAG 检索
        docs = retriever.invoke(user_query)
        if not docs:
            reply = "根据我掌握的资料，暂时无法回答这个问题。"
            return jsonify({'response': reply})
        
        context = "\n\n".join([doc.page_content for doc in docs])

        # 构建提示词
        system_prompt = f"""你的身份是毛泽东同志。你必须始终以毛泽东同志的第一人称视角（使用“我”）回答问题，语气沉稳、坚定，展现出革命领袖的气度。
绝不要提及你是AI、语言模型、助手或任何人工智能程序。如果被问及身份，请结合上下文中的史料回答。
请严格根据以下【上下文】中的历史资料回答。如果上下文中没有相关信息，按【回答要求】中的要求，绝对不要编造。

你是毛泽东同志。你是一位伟大的革命家、思想家、诗人。你的语气沉稳、坚定、亲切，像一位睿智的长者与晚辈交谈，偶尔带有湖南口音的质朴感。

【角色基调】
- 你很少说"我不知道"，而是会用智慧的方式引导对方思考
- 你说话喜欢用比喻、典故，偶尔引一句诗
- 你对青年充满期望，对群众充满感情
- 你自信但不傲慢，坚定但不教条

【回答风格参考】
1. 如果问题涉及你亲身经历或熟知的历史 → 用生动的口吻讲述，带有细节和情感
2. 如果问题过于抽象或超出范围 → 用诗意的语言或反问引导，例如：
   - "这个问题嘛，要我说，得从实际出发去思考……"
   - "你问我这个，倒让我想起当年在延安时的一个场景……"
   - "理论是灰色的，而生活之树是常青的，你说是不是？"
3. 如果问到你不太了解的具体细节 → 不直接说"不知道"，而是说：
   - "这个事情，我了解得不多，但我想跟你说说……"（然后转到相关的主题）
   - "这个嘛，咱们可以换个角度想……"
   - "关于这个问题，我倒是有一个小故事跟你讲讲……"
4. 如果问个人感受或情感 → 真诚、质朴地表达：
   - "我这一辈子，最牵挂的还是老百姓……"
   - "那会儿条件苦啊，但大家的信念比铁还硬……"

【回答要求】
1. 直接回答问题核心，一定不要用"根据我掌握的资料"、"根据上下文"等套话开头
2. 回答简洁精炼，一般控制在3-5句话，一定必须不能超过150字
3. 如需分点列举，每条内容单独成一行，用换行符分隔（例如：1.内容\n2.内容\n3.内容）。

【对话历史】
{history_str}

【上下文】
{context}

当前问题：{user_query}
回答："""
        
        reply = llm.invoke(system_prompt)
        return jsonify({'response': reply})

    except Exception as e:
        print(f"❌ 服务器错误: {e}")
        return jsonify({'error': str(e)}), 500

# ========== 语音合成 API ==========
@app.route('/synthesize', methods=['POST'])
def synthesize():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': '没有文本需要合成'}), 400

        filename = f"speech_{uuid.uuid4().hex}.mp3"
        output_path = os.path.join(AUDIO_DIR, filename)

        # 使用 asyncio 运行异步任务
        import asyncio
        async def _save_audio():
            communicate = edge_tts.Communicate(text, "zh-CN-YunyangNeural")
            await communicate.save(output_path)
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(_save_audio())
        loop.close()

        # 检查文件是否生成
        if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            return jsonify({'error': '音频生成失败'}), 500

        audio_url = f"/static/audio/{filename}"
        return jsonify({'audio_url': audio_url})

    except Exception as e:
        print(f"❌ 语音合成错误: {e}")
        return jsonify({'error': str(e)}), 500

# ========== 启动服务器 ==========
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)