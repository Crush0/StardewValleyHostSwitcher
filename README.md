# 星露谷物语主机切换工具
# StardewValley Host Switcher

## 项目简介
本项目是一个专为《星露谷物语（Stardew Valley）》设计的工具，用于切换多人存档的主机。通过简单的图形界面，用户可以快速修改存档文件，使新的玩家成为主机。

This project is a tool designed specifically for Stardew Valley to switch hosts for multiplayer archives. With a simple graphical interface, users can quickly modify archive files to make new players the host.

## 功能特性
- **存档加载**：支持加载《星露谷物语》的多人存档文件。
- **主机切换**：从协助者列表中选择新的主机，并更新存档。
- **文件导出**：生成修改后的存档文件，方便用户替换原存档。
- **简洁易用**：基于 Gradio 构建的图形用户界面，操作直观。

## 目前已知问题
- 社区中心的精灵文本可能变得无法阅读，重新找法师触发剧情后可恢复正常。
- ~~农场洞穴重新变为未选择状态。（已修复）~~

## 使用说明

### 环境要求
- Python 3.7 或更高版本
- 必须安装以下依赖：
  ```bash
  pip install gradio
  ```

### 操作步骤
1. **准备存档文件**：找到你的游戏存档，存档路径通常为：
   - Windows: `C:\Users\<你的用户名>\AppData\Roaming\StardewValley\Saves`
   - Mac: `~/.config/StardewValley/Saves`
   - Linux: `~/.config/StardewValley/Saves`
   进入存档文件夹，选择以农场名开头的文件（不要选择以 `old` 结尾的文件）。

2. **运行程序**：
   ```bash
   python main.py
   ```
   程序会自动在浏览器中打开。

3. **加载存档文件**：点击“选择保存文件”上传存档文件，随后点击“加载文件”按钮。

4. **选择新主机**：从协助者列表中选择新的主机。

5. **切换主机**：点击“转换主机”按钮，生成新的存档文件。

6. **下载新存档**：点击右侧的下载按钮获取修改后的存档文件。

7. **替换原存档**：用新的存档文件替换原文件，重启游戏即可。

## 注意事项
- **备份原始存档**：在操作前，建议将原存档文件备份，以防操作失误。
- **存档版本**：本工具适用于《星露谷物语》1.6版本，可能与其他版本存档不兼容。
- 

## 贡献
欢迎对本项目提出建议或贡献代码！您可以通过以下方式参与：
- 提交 Issue 反馈问题或建议。
- Fork 本项目并提交 Pull Request。

## 许可证
本项目使用 [MIT 许可证](LICENSE)。

