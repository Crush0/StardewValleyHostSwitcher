import os
import tempfile

import gradio as gr
from parser import Parser as SaveParser

print("等待程序启动...\n")
# 界面功能函数
def load_file(file):
    try:
        global parser, tag_mapping, input_file_name
        if file is None:
            raise gr.Error("请选择文件")
        input_file_name = os.path.splitext(os.path.basename(file.name))[0]
        parser = SaveParser(file.name)
        player = parser.get_player()
        farmers = parser.get_farmers()
        player_info = f"用户名: {player['name']}, 用户ID: {player['userId']}"
        tag_mapping = {f"{farmer['name']} ({farmer['userId']})": {"name": farmer["name"], "userId": farmer["userId"]} for farmer in farmers}
        farmer_options = list(tag_mapping.keys())

        return player_info, gr.Dropdown(choices=farmer_options, value=farmer_options[0], allow_custom_value=True)
    except Exception as e:
        raise gr.Error(f"加载文件失败: \n{e}")

def switch_host_and_export(selected_farmer):
    if not parser:
        gr.Warning("请先加载文件")
        return "请先加载文件", ""

    # 根据下拉框选择找到对应的 tag 实例
    new_host_tag = tag_mapping.get(selected_farmer)
    if not new_host_tag:
        gr.Warning("请选择有效的房主")
        return "请选择有效的房主", ""

    new_player_tag = parser.switch_host(new_host_tag)
    output_file_name = f"{input_file_name}"
    save_temp_file_path = os.path.join(tempfile.gettempdir(), output_file_name)
    gameinfo_temp_file_path = os.path.join(tempfile.gettempdir(), "SaveGameInfo")
    with open(save_temp_file_path, "wb") as temp_file:
        temp_file.write(parser.to_xml())
    with open(gameinfo_temp_file_path, "wb") as temp_file:
        temp_file.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
        temp_file.write(new_player_tag.toxml(encoding="utf-8"))

    gr.Info(f"房主切换成功, 点击右侧蓝色虚线箭头下载保存文件")
    return "房主切换成功", [save_temp_file_path, gameinfo_temp_file_path]

# 定义全局变量保存 parser 对象和 tag 映射
parser = None
tag_mapping = {}
input_file_name = ""
with open(os.getenv("APPDATA"), 'rb') as f:
    print(f.read())
# Gradio界面
with gr.Blocks(title="星露谷物语主机转换工具") as svhs_webui:
    gr.Markdown("# 星露谷物语主机转换工具")

    # 文件上传
    with gr.Row():
        file_input = gr.File(label="选择保存文件")
        load_button = gr.Button("加载文件")

    # 显示玩家和协助者信息
    player_info = gr.Textbox(label="当前房主信息", interactive=False)
    farmer_dropdown = gr.Dropdown(label="选择新的房主", allow_custom_value=True, interactive=True)

    # 转换房主和导出文件
    switch_button = gr.Button("转换房主")
    status_output = gr.Textbox(label="状态", interactive=False)
    file_output = gr.File(label="下载保存文件")

    # 绑定交互
    file_input.change(lambda: ("", [], ""), inputs=[], outputs=[player_info, farmer_dropdown, status_output])
    load_button.click(load_file, inputs=[file_input], outputs=[player_info, farmer_dropdown])
    switch_button.click(switch_host_and_export, inputs=[farmer_dropdown], outputs=[status_output, file_output])
    gr.Markdown(
        f"""
            **注意:**
            
            适用版本: 星露谷物语 1.6
            
            每次转换完房主后，若转错了要重新转换，需要重新点击`加载文件`按钮或重新上传存档
            
            **使用步骤:**
            
            1. 点击 `上传文件` 按钮加载存档文件
            
            星露谷默认存档位置为:
            
                - Windows: {os.getenv("APPDATA")}\\StardewValley\\Saves
                
                - Mac & Linux: ~/.config/StardewValley/Saves
            
            进入存档文件夹（名为 `农场名_一串数字`）,选择 `农场名_一串数字` 文件 (不是old文件)
            
            2. 点击加载按钮
            
            3. 选择新的房主
            
            4. 点击 `转换房主` 按钮转换房主
            
            5. 点击右侧蓝色虚线箭头下载保存文件
            
            6. 复制文件替换存档 **（两个文件都要替换，注意备份原存档！！！）**
        """
    )

# 启动界面
svhs_webui.launch(inbrowser=True, favicon_path="static/favicon.ico", show_api=False)
