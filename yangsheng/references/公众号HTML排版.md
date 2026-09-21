# 公众号 HTML 交付与排版

**默认交付一个 `.html` 文件**，用户用浏览器打开后 Ctrl+A 全选、Ctrl+C 复制、粘贴进公众号编辑器即可发布。不再交付裸正文文本；用户明确要纯文本时才给。

规范来自微信公众平台《文章结构验证规范》（`verify-article-structure-spec`）。规范里有阈值和判定逻辑，写完后照本文件末尾的清单自检。

## 一、视觉标记体系

一篇里有三种强调，分工不重叠。**同一句只用一种**，不要既标红又加下划线。

| 标记 | 管什么 | 一篇几处 | 样式 |
| :--- | :--- | :--- | :--- |
| **红色加粗**（不带下划线） | 作者自己的核心判断、转折落点 | 2—4 处 | `color:#d0021b` + 加粗 |
| **下划线加粗**（保持正文灰） | 事实与数字层面的关键：被质疑的说法、真正显著的数值、测量局限、指南原文、试验边界 | 4—6 处 | `text-decoration:underline` + 加粗 |
| **小标题** | 每一节的判断句 | 3—5 处 | 红色 + 加大字号 + 下划线 + 加粗 |

- 红色 `#d0021b`。夜间模式下平台算法会保留色相、只调亮度，属正常，不必回避红色。
- 下划线**一次只覆盖一个短句**（二十字上下），跨两三行的长下划线读者抓不住重点，也会把版面压得很重。
- 不用第四种强调。没有红、没有线、只是加粗的句子要么补上归属，要么取消。
- 标记要贴着正文的判断走：红了哪一句，读者就会把那句当结论。红在铺垫句上，等于把铺垫当结论卖。

## 二、小标题

判断句小标题（写法要求见 `语言特征.md` 第二节）。样式固定为：

- 字号比正文大一档：正文 16px → 小标题 **20px**
- 颜色红 `#d0021b`，加粗，加下划线
- `line-height:1.6`（20 × 1.6 = 32px，大于字号，不会叠字）
- **不加左侧竖线、不加背景色块**。红字加下划线已经足够醒目，再叠一道竖线是两个强调色打架；背景色块在夜间模式下容易被算法转成纯色。

## 三、正文样式

| 部位 | 样式 |
| :--- | :--- |
| 外层容器 | 一个 `<section>`，承载全篇基础样式：`font-size:16px;line-height:1.75;color:#3f3f3f;letter-spacing:0.6px;text-align:left;` |
| 正文段 | `<p style="margin:0 0 16px 0;">`，段内文字包在 `<span leaf="">` 里 |
| 小标题 | `<p style="margin:30px 0 14px 0;font-size:20px;line-height:1.6;color:#d0021b;">` |
| 免责声明 | `<p style="margin:0;font-size:14px;line-height:1.8;color:#6b6b6b;text-align:center;">` |
| 段间距 | 普通段 16px（约一个字高）；开篇结束、以及结尾段用 24px |

**段间距不要超过约 1em。**16px 字号配 16px 段距，读起来是一段接一段；给到 22px 以上，视觉上接近一个空行，整篇会显得松散、留白过重。小标题靠上方间距（30px）拉开层级，不靠加大段距。

行高一律大于字号。免责声明用 `#6b6b6b`（对白底 5.3:1），不要用 `#999` 一类更浅的灰，对比度不够会被算法判低。

## 四、平台硬规则（写完逐条核对）

**CSS**

- 不设 `font-family`。公众号有默认字体栈，自定义字体会让编辑器预览与真机不一致。
- 不设 `width`。需要固定宽度的场景才用 `data-ignore-width` 豁免，正文排版用不到。
- 不设 `height`。`height:0` 且内含文字的结构在移动端文字会完全不可见。
- `text-align` 只用 `left` / `center` / `right`，不用 `start` / `end`（各端兼容性不一致）。
- 不用 `!important`。
- 不用 `opacity:0`。
- 字符背景不用渐变（`linear-gradient`）——夜间模式会被算法转成纯色。
- 不用绝对定位或 `transform` 打乱 DOM 顺序与视觉顺序的一致性。

**结构**

- 每段用 `<p>` 承载，文字包在 `<span leaf="">` 中。`<span leaf>` 内**只能放文本和行内元素**（`span`、`strong`、`a`、`img`、`br`），绝不能放 `section`、`div`、`p` 等块级元素。
- 同一标签名、同一内联样式、只有一个子节点的连续嵌套不得超过 10 层。正文排版通常只有 2—3 层。
- 一个容器里空子节点过多会被编辑器自动删除。不要留空的 `<p></p>`。
- 不用 `<pre>` 包裹普通文本（不换行，移动端横向截断）。
- 不用 `<table>` 做排版。
- 有图片时给 `<img>` 加 `data-w`（图片原始像素宽），否则引擎在图片加载超时时无可靠宽度。

**交付形态**

- 图片、SVG、表格在正文里能不出现就不出现；本类文章通常是纯文字稿。
- 文章主标题**不写进 HTML**——公众号标题是编辑器里单独的输入框，粘正文不会带过去。标题在回复里给。
- 文件顶部留一行注释，写明复制方法（浏览器打开 → 全选 → 复制 → 粘贴）。

## 五、模板骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="utf-8"><title>标题占位</title></head>
<body style="margin:0;padding:0;background:#ffffff;">

<!-- 复制方法：用浏览器打开本文件（不是用编辑器打开），Ctrl+A 全选，Ctrl+C，粘贴进公众号编辑器 -->

<section style="font-size:16px;line-height:1.75;color:#3f3f3f;letter-spacing:0.6px;text-align:left;">

<p style="margin:0 0 16px 0;"><span leaf="">正文段落。</span></p>

<p style="margin:30px 0 14px 0;font-size:20px;line-height:1.6;color:#d0021b;"><span leaf=""><strong style="text-decoration:underline;">判断句小标题</strong></span></p>

<p style="margin:0 0 16px 0;"><span leaf="">正文里的事实关键，<strong style="text-decoration:underline;">下划线加粗</strong>；作者的核心判断，<strong style="color:#d0021b;">红色加粗，不带线</strong>。</span></p>

<p style="margin:0;font-size:14px;line-height:1.8;color:#6b6b6b;text-align:center;"><span leaf="">本文仅作健康科普，不能替代个体诊疗；身体有不适请及时就医。</span></p>

</section>

</body>
</html>
```

## 六、交付前自检

字数仍按 `count_body.py` 的口径——**HTML 里剥掉标签后的可见文字**，即去掉 `<...>` 之后按非空白字符计数，与纯文本版一致，`--min-length` / `--max-length` 照旧。

排版部分：

- 三种标记的数量在范围内，没有一句同时标红又加下划线
- 小标题都是判断句，不是话题名
- 红字标在结论上，不是铺垫上
- 平台硬规则逐条为 OK（可以用脚本正则扫一遍：`font-family`、`width`、`height`、`text-align: start|end`、`<pre`、`opacity`、`gradient`、`!important`、`position:absolute`、`transform`）
- `<span leaf>` 内没有块级元素
- 段落数、空节点数正常（空节点应为 0）
- 免责声明在最后一行的位置
