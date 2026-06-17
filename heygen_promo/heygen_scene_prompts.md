# HeyGen 视频配置提示词

## 目标

制作一个约 3 分钟的中文宣传视频，推广“量子知识图谱 · 3D 推演引擎”。

## 主播形象

使用 HeyGen 的真人感女性虚拟主播，必须是虚构的成年女性，不使用任何真实公众人物肖像。

推荐提示词：

Photorealistic fictional adult female technology presenter, elegant and glamorous, confident, attractive but tasteful, professional studio lighting, natural facial expression, realistic skin texture, accurate lip sync, seated at a modern desk, operating a laptop, cinematic tech studio, no nudity, no explicit content.

中文描述：

真实感虚构成年女性科技主播，优雅、有魅力、镜头表现力强，但整体专业克制。她坐在现代科技感办公桌前，一边操作电脑，一边讲解屏幕中的量子知识图谱页面。画面左下角使用圆形画中画主播框，背景是项目真实页面或屏幕演示。

## 画面布局

- 背景：使用 `exports/quantum_kg_background_sequence.mp4` 作为主屏幕演示背景。
- 主播：放在左下角圆形画中画框内，占画面宽度约 18%-22%。
- 主播动作：看向镜头、偶尔看向电脑、手部轻微操作电脑。
- 口型：直接使用 `narration_zh.txt` 作为 HeyGen 口播脚本，启用中文普通话语音和 lip sync。
- 字幕：上传 `subtitles_zh.srt`，或者让 HeyGen 根据同一稿件自动生成字幕。

## 声音

- 语言：中文普通话。
- 风格：科技产品发布会，清晰、兴奋但不夸张。
- 语速：中等偏稳，约 3 分钟至 3 分 45 秒。
- 要求：字幕文字必须与口播稿一致，避免临场改稿，否则口型和字幕会错位。

## 镜头结构

1. 00:00-00:34 项目开场：3D 量子研究地球。
2. 00:34-01:22 三维图谱讲解：节点、来源、证据、难度、攻击路径。
3. 01:22-01:44 二维图谱切换：搜索、筛选、密集关系查看。
4. 01:44-02:42 推演过程：逐步推理和多智能体模拟。
5. 02:42-03:28 文献、报告导出、用户大模型设置。
6. 03:28-03:46 结尾 Call to Action。

## HeyGen 操作建议

1. 创建 Landscape 16:9 视频。
2. 选择真人感女性 Studio Avatar 或 Instant Avatar。
3. 上传 `exports/quantum_kg_background_sequence.mp4` 作为背景视频。
4. 将 Avatar 放到左下角，设置圆形或软边画中画框。
5. 粘贴 `narration_zh.txt` 到脚本框。
6. 选择中文普通话语音，生成口型。
7. 上传或导入 `subtitles_zh.srt`。
8. 预览确认每段字幕和口型同步。
9. 最后确认消耗额度后再点击 Generate / Export。
