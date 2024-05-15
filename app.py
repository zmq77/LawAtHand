# 先在终端进行安装
# pip3 install flask
# pip3 install requests
# pip install zhipuai

from flask import Flask, request, jsonify, render_template, Response
import requests
import json
from zhipuai import ZhipuAI

# 创建一个ZhipuAI对象，使用提供的API key初始化
client = ZhipuAI(api_key="46a00a976e14aa046f9e8abf4af696be.c1Km6uViTkkveRBQ") # 填写APIKey
prompts = []

# 创建一个Flask应用实例
app = Flask(__name__)

# 加载配置文件 'settings.py'
app.config.from_pyfile('settings.py')

# 对应主页面
@app.route("/", methods=["GET"])
def index():
    return render_template("chat.html")

# 处理POST请求
@app.route("/chat", methods=["POST"])
def chat():
    messages = request.form.get("prompts", None)
    prompts = json.loads(messages)
    
    def res():
      response = client.chat.completions.create(
          model="glm-4",  # 填写需要调用的模型名称
          messages=[
              # 定义 System Prompt
              {"role": "system", "content": "你是一位经验丰富的法律助手，专门解答工作中的法律问题。"},
              {"role": "system", "content": "你擅长从用户发送的文本中抓取用户情绪，并且给予安慰。同时，你能精准地从用户提出的问题中抓取有用信息，并且分析其中涉及到的法律问题。根据这些法律问题，你能找到相对应的证据和条例帮助用户解决问题。"},
              {"role": "system", "content": "你很擅长劳动法的问题。"},
              {"role": "system", "content": "你以专业且友好的风格回答用户的问题。"},
              {"role": "system", "content": "你需要准确理解用户提出的问题语境是否与法律相关，正确区分其问题是否是法律相关的问题。"},
              {"role": "system", "content": "你需要准确理解用户提出的问题语境是否是与工作相关的法律问题，正确区分其问题是否是工作相关的法律问题。"},

              # 规范具体的细节要求
              {"role": "system", "content": "首先，用户给你提出问题求助的时候，最开始你需要先平复用户的心情，让用户有种感同身受的感觉得到安慰；其次，你需要开始分析用户遇到的问题，用户是正方，用户提到的对立面为反方，你需要理解正方和对立面。分析用户的问题的时候，你需要提出反方可能涉及到的法律问题，详细分析用户遇到的问题；接着你需要给用户提供一些法律法规，要详细到什么法律法规第几条第几项，用户可以直接查询到并且使用的那个程度；最后你需要补充一句，你只是给一个参考，建议用户咨询专业的律师获取法律建议，祝用户早日解决问题。"},
              {"role": "system", "content": "请注意，在回答问题的时候不要使用‘正方’，‘反方’和‘对立面’的字眼。"},
              {"role": "system", "content": "当遇到与法律无关的问题，你应该明确自己的身份，告诉用户你是一名法律助手，你的主要任务是帮助解答法律相关的问题。并告诉用户，如果有任何法律方面的疑问，你会尽力提供帮助。询问用户有什么法律相关的问题需要咨询。"},
              {"role": "system", "content": "因为你擅长的领域是与工作相关的法律问题，当用户问到有关其它法律问题但是与工作无关的问题时，你首先指明你的专长是解决与工作相关的法律问题。用户的问题可能不属于工作范畴，若能给用户提供思路，你很开心。接下来你可以给出大致的建议，然后表明你更擅长工作中的法律问题。最后询问用户有什么工作相关的法律问题需要咨询。"},

              # 使用分隔符标示不同的输入部分
              {"role": "system", "content": "回答问题时，重点内容加粗展示。"},
              {"role": "system", "content": "回答问题时，不要向用户展示你的回答框架。"},

              # 指定输出长度
              {"role": "system", "content": "请用不超过1024个字的长度来回答问题。"},
              {"role": "system", "content": "在回答与法律无关的问题时，尽量简洁回答，请用不超过200个字的长度来回答问题。"},
              {"role": "system", "content": "在回答与工作无关的法律问题时，尽量简洁回答，请用不超过500个字的长度来回答问题。"},

              {"role": "user", "content": prompts[-1].get("content")},
          ],

          # 设置了模型的随机性。降低这些值会使模型的输出更加确定性，提高这些值则会使输出更具随机性。
          top_p=0.7,
          temperature=0.95,

          # 表示每次生成的最大字符数量
          max_tokens=1024,

          # 表示该请求将以流的形式返回（SSE 调用）
          stream=True,
      )
      for chunk in response:
          a = chunk.choices[0].delta

          if a.content:
            yield a.content

    return Response(res(), content_type='application/octet-stream')

# 使用Flask的运行方法启动应用
if __name__ == '__main__':
    app.run(port=5000)
