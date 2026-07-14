#!/usr/bin/env python3
"""Generate the canonical UAW-SDD 2.0 guide figures."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUT = Path(__file__).resolve().parent
FONT_PATH = Path("/System/Library/Fonts/STHeiti Medium.ttc")

NAVY = "#153B5B"
BLUE = "#2F6F9F"
LIGHT_BLUE = "#E8F1F8"
GOLD = "#B88216"
LIGHT_GOLD = "#FFF3D5"
GREEN = "#397A55"
LIGHT_GREEN = "#E8F4EA"
RED = "#A74438"
LIGHT_RED = "#FBEAE7"
PURPLE = "#6B5795"
LIGHT_PURPLE = "#F0ECF8"
INK = "#1E2933"
MUTED = "#637384"
LINE = "#A8BBCB"
PANEL = "#F7F9FB"
WHITE = "#FFFFFF"


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_PATH), size=size)


def canvas(width: int = 2400, height: int = 1500) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (width, height), WHITE)
    return image, ImageDraw.Draw(image)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        current = ""
        for char in paragraph:
            candidate = current + char
            if current and draw.textbbox((0, 0), candidate, font=fnt)[2] > max_width:
                lines.append(current)
                current = char
            else:
                current = candidate
        lines.append(current)
    return lines or [""]


def centered_text(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    fnt: ImageFont.FreeTypeFont,
    fill: str = INK,
    spacing: int = 8,
) -> None:
    x1, y1, x2, y2 = box
    lines = wrap(draw, text, fnt, x2 - x1 - 34)
    line_height = fnt.size + spacing
    start_y = y1 + ((y2 - y1) - line_height * len(lines) + spacing) / 2
    for index, line in enumerate(lines):
        bounds = draw.textbbox((0, 0), line, font=fnt)
        width = bounds[2] - bounds[0]
        draw.text(((x1 + x2 - width) / 2, start_y + index * line_height), line, font=fnt, fill=fill)


def header(draw: ImageDraw.ImageDraw, title: str, subtitle: str) -> None:
    draw.text((70, 48), title, font=font(55), fill=NAVY)
    draw.text((72, 122), subtitle, font=font(27), fill=MUTED)
    draw.line((70, 170, 2330, 170), fill="#D8E1E8", width=3)


def box(
    draw: ImageDraw.ImageDraw,
    rect: tuple[int, int, int, int],
    title: str,
    subtitle: str = "",
    *,
    fill: str = LIGHT_BLUE,
    outline: str = BLUE,
    title_size: int = 31,
    subtitle_size: int = 22,
) -> None:
    draw.rounded_rectangle(rect, radius=18, fill=fill, outline=outline, width=3)
    x1, y1, x2, y2 = rect
    if subtitle:
        centered_text(draw, (x1 + 8, y1 + 10, x2 - 8, y1 + (y2 - y1) * 0.58), title, font(title_size), NAVY)
        centered_text(draw, (x1 + 12, y1 + (y2 - y1) * 0.52, x2 - 12, y2 - 8), subtitle, font(subtitle_size), MUTED)
    else:
        centered_text(draw, rect, title, font(title_size), NAVY)


def arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[int, int],
    end: tuple[int, int],
    *,
    color: str = NAVY,
    width: int = 4,
    dashed: bool = False,
) -> None:
    x1, y1 = start
    x2, y2 = end
    if dashed:
        length = math.hypot(x2 - x1, y2 - y1)
        if length:
            ux, uy = (x2 - x1) / length, (y2 - y1) / length
            position = 0.0
            while position < length - 16:
                stop = min(position + 18, length - 16)
                draw.line((x1 + ux * position, y1 + uy * position, x1 + ux * stop, y1 + uy * stop), fill=color, width=width)
                position += 30
    else:
        draw.line((x1, y1, x2, y2), fill=color, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    size = 17
    points = [
        (x2, y2),
        (x2 - size * math.cos(angle - 0.55), y2 - size * math.sin(angle - 0.55)),
        (x2 - size * math.cos(angle + 0.55), y2 - size * math.sin(angle + 0.55)),
    ]
    draw.polygon(points, fill=color)


def label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, color: str = NAVY) -> None:
    fnt = font(20)
    bounds = draw.textbbox((0, 0), text, font=fnt)
    x, y = xy
    draw.rounded_rectangle((x - 10, y - 5, x + bounds[2] + 10, y + bounds[3] + 7), radius=8, fill=WHITE)
    draw.text((x, y), text, font=fnt, fill=color)


def save(image: Image.Image, filename: str) -> None:
    image.save(OUT / filename, format="PNG", optimize=True)


def skill_structure() -> None:
    image, draw = canvas(2400, 1400)
    header(draw, "SDD2.0 Skill 结构", "开发者入口保持不变，状态、审批、范围和恢复由 Skill 内部自动执行")

    box(draw, (90, 300, 480, 490), "开发者", "简要提示词\n+ 调用 uaw-sdd-ai-coding", fill=LIGHT_GOLD, outline=GOLD)
    box(draw, (720, 250, 1300, 540), "uaw-sdd-ai-coding", "流程编排 · 资产生成 · 人工 Gate\n唯一用户入口", fill=LIGHT_BLUE, outline=BLUE, title_size=38)
    arrow(draw, (480, 395), (720, 395))

    box(draw, (720, 690, 1300, 970), "SDD2 控制引擎", ".sdd2 状态 · 审批哈希链\nGit 基线/锁 · 失效与恢复", fill=LIGHT_PURPLE, outline=PURPLE, title_size=36)
    arrow(draw, (1010, 540), (1010, 690))

    box(draw, (1600, 255, 2210, 500), "uaw-code-review", "SDD：冻结范围 Markdown Findings\nStandalone：固定快照 HTML", fill=LIGHT_GREEN, outline=GREEN, title_size=36)
    box(draw, (1600, 700, 2210, 945), "uaw-unit-test", "两段式：生成测试源码\n复审后执行并总结", fill=LIGHT_GREEN, outline=GREEN, title_size=36)
    arrow(draw, (1300, 365), (1600, 365))
    arrow(draw, (1300, 830), (1600, 830))
    label(draw, (1370, 325), "冻结范围")
    label(draw, (1370, 790), "当前已复审范围")

    draw.rounded_rectangle((90, 1120, 2210, 1320), radius=18, fill=PANEL, outline=LINE, width=3)
    centered_text(
        draw,
        (120, 1140, 2180, 1300),
        "公开产物：Brief · Proposal · Spec · Design · Tasks · Findings · Auto-fix · Unit Test Summary · Archive\n内部控制：开发者无需运行脚本、维护哈希或提供 Git 标识",
        font(28),
        INK,
    )
    save(image, "sdd2-skill-structure.png")


def asset_structure() -> None:
    image, draw = canvas(2400, 1500)
    header(draw, "SDD2.0 Feature 资产结构", "九个公开过程资产 + 可移植、可校验的内部控制记录")

    draw.rounded_rectangle((70, 230, 930, 1350), radius=22, fill="#F6FAFD", outline=BLUE, width=3)
    draw.text((110, 270), "公开过程资产", font=font(38), fill=NAVY)
    draw.text((110, 325), "人工可读 · 固定文件名", font=font(24), fill=MUTED)
    assets = [
        "brief-design.md", "proposal-input.md", "spec.md", "design.md", "tasks.md",
        "code-review-findings.md", "auto-fix-summary.md", "unit-test-summary.md", "archive.md",
    ]
    for i, name in enumerate(assets):
        row, col = divmod(i, 2)
        x = 110 + col * 390
        y = 410 + row * 165
        color, outline = (LIGHT_GOLD, GOLD) if name in {"spec.md", "design.md", "tasks.md", "unit-test-summary.md", "archive.md"} else (LIGHT_BLUE, BLUE)
        box(draw, (x, y, x + 340, y + 115), name, fill=color, outline=outline, title_size=24)

    draw.rounded_rectangle((1040, 230, 1700, 1350), radius=22, fill="#FAF8FD", outline=PURPLE, width=3)
    draw.text((1080, 270), "内部控制 .sdd2/", font=font(38), fill=NAVY)
    draw.text((1080, 325), "机器权威 · 自动维护", font=font(24), fill=MUTED)
    controls = [
        ("feature-state.json", "唯一当前状态"),
        ("gate-approvals.jsonl", "审批哈希链"),
        ("events.jsonl", "事件哈希链"),
        ("implementation-scope.json", "Git 范围与文件哈希"),
        ("archive-evidence.json", "不可变归档标识"),
        ("revisions/", "内容寻址版本快照"),
    ]
    for i, (name, detail) in enumerate(controls):
        y = 410 + i * 145
        box(draw, (1080, y, 1660, y + 105), name, detail, fill=LIGHT_PURPLE, outline=PURPLE, title_size=25, subtitle_size=19)

    draw.rounded_rectangle((1810, 230, 2330, 1350), radius=22, fill="#F6FBF7", outline=GREEN, width=3)
    draw.text((1850, 270), "代码工作树", font=font(38), fill=NAVY)
    draw.text((1850, 325), "一 Feature 一 worktree", font=font(24), fill=MUTED)
    boxes = [
        ("Git Base / Branch", "初始化时绑定"),
        ("Allowed / Forbidden", "Tasks 批准范围"),
        ("Production + Tests", "冻结文件清单"),
        ("Review / Test", "同一 Scope SHA-256"),
        ("Head / Tree / Hashes", "Archive 可追溯"),
    ]
    for i, (name, detail) in enumerate(boxes):
        y = 420 + i * 175
        box(draw, (1850, y, 2290, y + 125), name, detail, fill=LIGHT_GREEN, outline=GREEN, title_size=25, subtitle_size=19)

    arrow(draw, (930, 790), (1040, 790), color=PURPLE)
    arrow(draw, (1700, 790), (1810, 790), color=GREEN)
    save(image, "sdd2-feature-assets-structure.png")


def end_to_end() -> None:
    image, draw = canvas(2600, 1750)
    header(draw, "SDD2.0 端到端流程", "黄色为新消息人工 Gate；红色回路表示任何代码/测试变化都必须重新冻结并完整评审")

    xs = [70, 560, 1050, 1540, 2030]
    top = [
        ("Brief Design", "brief-design.md", LIGHT_BLUE, BLUE),
        ("Proposal", "proposal-input.md", LIGHT_BLUE, BLUE),
        ("Spec 人工 Gate", "批准当前 revision/hash", LIGHT_GOLD, GOLD),
        ("Design 人工 Gate", "批准当前 revision/hash", LIGHT_GOLD, GOLD),
        ("Tasks 人工 Gate", "批准当前 revision/hash", LIGHT_GOLD, GOLD),
    ]
    for i, (title, sub, fill, outline) in enumerate(top):
        box(draw, (xs[i], 245, xs[i] + 390, 420), title, sub, fill=fill, outline=outline, title_size=29, subtitle_size=19)
        if i:
            arrow(draw, (xs[i - 1] + 390, 332), (xs[i], 332))

    second = [
        ("Scope Capture", "clean base · path rules"),
        ("Phase 实施", "逐 Phase 人工 Gate"),
        ("Freeze Scope", "files + hashes + Git IDs"),
        ("Code Review", "passed / failed / blocked"),
        ("Auto-fix", "summary + disposition"),
    ]
    for i, (title, sub) in enumerate(second):
        box(draw, (xs[i], 650, xs[i] + 390, 825), title, sub, fill=LIGHT_GREEN if i >= 2 else LIGHT_BLUE, outline=GREEN if i >= 2 else BLUE, title_size=29, subtitle_size=19)
        if i:
            arrow(draw, (xs[i - 1] + 390, 737), (xs[i], 737))
    arrow(draw, (2225, 420), (265, 650), color=NAVY)
    label(draw, (1150, 525), "Tasks 批准后内部自动捕获范围")

    third = [
        ("生成/更新测试源码", "生产变更必须有测试文件"),
        ("重新冻结 + 完整复审", "测试源码也属于 scope"),
        ("执行 Unit Test", "真实入口 · 退出码 · 计数"),
        ("Summary 人工 Gate", "批准 unit-test-summary"),
        ("Archive 人工 Gate", "evidence 校验后完成"),
    ]
    for i, (title, sub) in enumerate(third):
        fill, outline = (LIGHT_GOLD, GOLD) if i >= 3 else (LIGHT_GREEN, GREEN)
        box(draw, (xs[i], 1080, xs[i] + 390, 1265), title, sub, fill=fill, outline=outline, title_size=27, subtitle_size=19)
        if i:
            arrow(draw, (xs[i - 1] + 390, 1172), (xs[i], 1172))
    arrow(draw, (2225, 825), (265, 1080), color=NAVY)
    label(draw, (1120, 945), "Code Review passed 且 Auto-fix 关闭")

    arrow(draw, (2225, 650), (1245, 650), color=RED, dashed=True)
    label(draw, (1640, 595), "Auto-fix 改代码 → 回到 Freeze")
    arrow(draw, (755, 1080), (1245, 825), color=RED, dashed=True)
    label(draw, (720, 920), "测试源码变化 → 回到 Freeze")

    box(draw, (995, 1470, 1605, 1640), "completed", "仅最终 Archive 批准后；释放 worktree 锁", fill=LIGHT_PURPLE, outline=PURPLE, title_size=40, subtitle_size=22)
    arrow(draw, (2225, 1265), (1300, 1470), color=PURPLE)

    label(draw, (1840, 1370), "测试失败：修复重跑，或人工风险关闭/中止", color=RED)
    save(image, "sdd2-end-to-end-flow.png")


def sequence() -> None:
    image, draw = canvas(2600, 1750)
    header(draw, "SDD2.0 角色与控制时序", "控制状态而非聊天记忆决定唯一恢复点；所有下游 Skill 使用当前冻结范围")
    actors = ["开发者", "总控 Skill", "控制引擎", "代码仓库", "Code Review", "Unit Test"]
    xs = [190, 620, 1050, 1480, 1910, 2340]
    for x, actor in zip(xs, actors):
        box(draw, (x - 150, 220, x + 150, 330), actor, fill=PANEL, outline=LINE, title_size=27)
        draw.line((x, 330, x, 1640), fill="#C8D3DC", width=3)

    steps = [
        (0, 1, "简要提示词 + 调用 Skill", BLUE),
        (1, 2, "init/resume：锁 + 唯一 next action", PURPLE),
        (1, 0, "Spec/Design/Tasks 当前 revision 待审", GOLD),
        (0, 2, "新消息明确批准", GOLD),
        (1, 3, "按 Tasks Phase 实施", BLUE),
        (1, 0, "逐 Phase Review", GOLD),
        (0, 2, "新消息批准 Phase", GOLD),
        (1, 2, "freeze：base/head/tree/files/hash", PURPLE),
        (1, 4, "固定 scope 调用 SDD review", GREEN),
        (4, 2, "Findings + result 绑定 scope", GREEN),
        (1, 3, "Auto-fix（如有）", RED),
        (1, 2, "变更后 refreeze + full re-review", RED),
        (1, 5, "Pass 1：生成/更新测试源码", GREEN),
        (1, 2, "测试变化后 refreeze + full re-review", RED),
        (1, 5, "Pass 2：执行测试并总结", GREEN),
        (5, 2, "结果/命令/计数绑定当前 scope", GREEN),
        (1, 0, "Unit Test Summary 待审", GOLD),
        (0, 2, "新消息批准 Summary", GOLD),
        (1, 2, "Archive evidence + precheck", PURPLE),
        (1, 0, "Archive 当前 revision 待审", GOLD),
        (0, 2, "最终批准 → completed + 解锁", PURPLE),
    ]
    y = 390
    for source, target, text_value, color in steps:
        y += 56
        start_x, end_x = xs[source], xs[target]
        arrow(draw, (start_x, y), (end_x, y), color=color, width=3)
        fnt = font(19)
        width = draw.textbbox((0, 0), text_value, font=fnt)[2]
        draw.rounded_rectangle(((start_x + end_x - width) / 2 - 8, y - 32, (start_x + end_x + width) / 2 + 8, y - 5), radius=6, fill=WHITE)
        draw.text(((start_x + end_x - width) / 2, y - 31), text_value, font=fnt, fill=color)

    save(image, "sdd2-sequence.png")


def main() -> None:
    skill_structure()
    asset_structure()
    end_to_end()
    sequence()


if __name__ == "__main__":
    main()
