# 梅花易数 Skill

meihua-yishu/ 是可独立安装的技能目录：SKILL.md 为入口；scripts/cast.py 为 Python 3.10+ 标准库排盘器；references/ 包含规则、来源、案例及64卦卦辞与384条爻辞古文摘录。
保留现有 docs/ 和 meihua/mhys-main/ 网站应用，本次没有修改它们。技能不需要网站、数据库或 AI API。

## 使用

将整个 meihua-yishu/ 安装到 Codex 用户技能目录。发现技能后可输入：

```text
请用 $meihua-yishu 按三个数1、7、9起卦，说明合作要留意什么。
```

GitHub 保存不会自动安装。本次仅生成技能源码，没有修改本机用户技能目录。

## 验证

```text
python meihua-yishu/scripts/test_cast.py
python meihua-yishu/scripts/cast.py lunar 5 12 17 9
```

测试含两个古例、64种上下卦及6种动爻结构核对、体用生克、余零、无效输入、取互差异。
公历转换、闰月、子时换日未自动化；规则文件注明支持范围。

## 来源

维基文库梅花易数卷一与卷二链接及仓库快照出处见参考文件。古文摘录没有复制现代作者解说。
排盘脚本独立编写，卦名对照网站；未改动或重新授权原网站程序。古文转录不是校勘定本，实际疑难字句须核查出处。
