# comfyui_text_list_stepper
用于批量抽取提示词

# Text List Processor Node for ComfyUI

**Author:** Gemini  
**Version:** 2.0

这是一个功能强大的 ComfyUI 自定义节点，用于处理文本列表。它允许您将大段文本按指定分隔符拆分为列表，根据一个可变的“种子（seed）”来循环选择列表中的一个或多个项目，最后将选中的项目用指定连接符合并成一个新的字符串。

这个节点的核心用途是实现 **提示词（Prompt）或参数的自动化迭代**。通过将节点的 `seed` 输入与 ComfyUI 的批处理计数器结合，您可以在每次生成时自动使用列表中的下一个提示词，极大地提高了工作流的自动化程度和效率。

## ✨ 功能特性

  - **自动化迭代**：与 ComfyUI 的 "increment" 种子（seed）控件配合使用，可为批处理中的每次运行自动选择列表中的下一个项目。
  - **多种分隔符**：支持按换行符 (`\n`)、逗号 (`,`)、分号 (`;`)、竖线 (`|`) 或空格来拆分输入文本。
  - **循环选择**：当选择到达列表末尾时，会自动从头开始，实现无缝循环。
  - **多项选择**：可以一次性从列表中选择多个连续的项目 (`selection_count`)。
  - **自定义连接符**：使用您指定的任何字符串（包括换行符 `\n` 等特殊字符）将选定的多个项目合并成单个文本输出。
  - **智能处理**：自动清理和忽略原始列表中的空白项。
  - **双重输出**：同时输出处理后的文本和用于本次选择的起始索引，方便调试和构建更复杂的工作流。

## 📥 安装

1.  打开您的 ComfyUI 安装目录。
2.  进入 `ComfyUI/custom_nodes/` 文件夹。
3.  下载本文档附带的 `__init__.py` 文件。
4.  在 `custom_nodes` 文件夹内创建一个新文件夹，例如 `TextListProcessor`。
5.  将 `__init__.py` 文件放入刚刚创建的 `TextListProcessor` 文件夹中。
      - 最终路径应为：`ComfyUI/custom_nodes/TextListProcessor/__init__.py`
6.  完全重启 ComfyUI。

安装完成后，您可以在节点的添加菜单中的 `Gemini/Text` 分类下找到 **Text List Processor (Gemini)** 节点。

## 🚀 使用方法与案例

### 主要用例：自动化提示词迭代

这是该节点最常见的用法。假设您想用一组不同的提示词生成多张图片，而不想手动修改它们。

1.  **添加节点**：在您的工作流中添加一个 `Text List Processor (Gemini)` 节点。
2.  **输入提示词列表**：
      - 在 `text_list` 框中，输入您的所有提示词，每行一个。
      - 例如：
        ```
        A beautiful landscape painting
        A futuristic city at night
        A portrait of a robot in a garden
        ```
3.  **设置参数**：
      - `separator`: 选择 `Newline (\n)`。
      - `selection_count`: 保持为 `1`，因为我们每次只想用一个提示词。
      - `join_with`: 可以留空或保持默认，因为只选择一项时，连接符无影响。
4.  **启用迭代**：
      - 在 `Text List Processor` 节点上右键单击，选择 `Convert seed to input`，将 `seed` 参数暴露为一个输入接口。
5.  **连接批处理计数器**：
      - 您需要一个能在每次运行时递增的整数。最简单的方法是使用 ComfyUI 内置的功能。当您设置批处理数量（Batch count）大于 1 并点击 "Queue Prompt" 时，像 `seed` 这样的输入会自动递增。
6.  **连接输出**：
      - 将 `Text List Processor` 节点的 `text` 输出连接到您的提示词编码器节点（如 `CLIP Text Encode (Prompt)`) 的 `text` 输入端。
7.  **执行**：
      - 设置您想要的批处理数量（例如 3），然后点击 **Queue Prompt**。ComfyUI 将会执行工作流 3 次，`Text List Processor` 的 `seed` 会从 0、1、2 依次变化，从而依次输出您的三个提示词，最终生成三张风格各异的图片。

### 其他用例：动态组合提示词

您也可以用它来动态地组合多个元素。

  - **`text_list`**: `red, green, blue, yellow, purple`
  - **`separator`**: `Comma (,`
  - **`seed`**: (连接到一个迭代器或设为固定值)
  - **`selection_count`**: `2`
  - **`join_with`**: ` ,  ` (逗号加空格)

如果 `seed` 为 0，输出将是 `"red, green"`。如果 `seed` 为 3，输出将是 `"yellow, purple"`。如果 `seed` 为 4，由于循环特性，输出将是 `"purple, red"`。

## 節點參數詳解

### Inputs (输入)

  - `text_list`
      - **类型**: `STRING` (多行文本)
      - **功能**: 包含项目列表的原始文本。项目应由下方选择的 `separator` 分隔。
      - **默认值**: `Positive prompt A\nPositive prompt B\nPositive prompt C`
  - `separator`
      - **类型**: `COMBO` (下拉菜单)
      - **功能**: 用于拆分 `text_list` 的字符。
      - **选项**: `Newline (\n)`, `Comma (,)`, `Semicolon (;)`, `Pipe (|)`, `Space`
  - `seed`
      - **类型**: `INT` (整数)
      - **功能**: 决定从列表中的哪个位置开始选择。起始位置由 `start_index = seed % list_length` 公式计算，这确保了选择是循环的。为了实现迭代，请将其转换为输入并连接到会递增的节点上。
      - **默认值**: `0`
  - `selection_count`
      - **类型**: `INT` (整数)
      - **功能**: 从 `start_index` 开始，要选择的连续项目的数量。如果选择超出列表末尾，会自动从头继续。
      - **默认值**: `1`
  - `join_with`
      - **类型**: `STRING` (单行文本)
      - **功能**: 当 `selection_count` \> 1 时，用于将选中的多个项目合并成一个字符串的分隔符。支持 `\n`、`\t` 等转义字符。
      - **默认值**: `\n`

### Outputs (输出)

  - `text`
      - **类型**: `STRING`
      - **功能**: 经过选择和合并后最终生成的文本字符串。您可以将其连接到任何接受文本输入的节点。
  - `start_index`
      - **类型**: `INT`
      - **功能**: 本次运行计算出的起始索引值（从 0 开始）。这个输出对于调试或需要了解当前迭代位置的复杂工作流非常有用。
