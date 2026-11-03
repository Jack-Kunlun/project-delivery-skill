# Project Delivery · 项目研发交付流程

一个可复用的 Agent skill，用于追踪需求、设计、开发、测试、验收、上线和持续改进。

[English](README.md) · [Skill 指令说明](docs/zh-CN/guide.md) · [MIT 许可证](docs/zh-CN/LICENSE.md)

Project Delivery 帮助编码 Agent 维护项目的真实工作和证据：已有记录就沿用，缺少记录就从小处建立，老旧系统则渐进接管。

## 覆盖内容

- 项目总览、已有能力、里程碑及有证据支持的进度。
- 任务与问题的责任、依赖、验收标准和恢复点。
- 临时需求、范围变更及被中断工作的接续。
- PRD、原型、UI/UX、开发、测试、验收及发布门槛。
- 模块职责、输入输出合同、状态归属和交接。
- 场景覆盖、验证边界、视觉检查和未解决的缺口。
- 复发问题、预防措施及改进效果复验。

## 三种接入方式

| 项目情况 | 处理方式 |
| --- | --- |
| 已有台账或任务系统 | 沿用权威来源、编号与状态，补齐缺口，不建立第二份可变任务表。 |
| 没有台账 | 根据代码、文档和反馈建立最小总览及任务/问题记录；无法证实的历史标为未知。 |
| 老旧或资料不全的项目 | 先建立现状基线，再逐步完善本次触达的范围。缺少 PRD、测试、Git 历史或运行环境，不等于必须立即重写。 |

小项目可以从一份文档开始，内容增长后再按维护需要拆分。不要求固定团队、技术栈、模块数量或发布方式。

## 安装

实际安装单元是 **`skills/project-delivery/`**。仓库根目录包含发布及维护资料，不是 skill 的安装目录。

### 使用 Codex 的 skill installer

如果当前 Codex 环境提供 `$skill-installer`，可以请求：

```text
使用 $skill-installer 安装以下地址中的 skill：
https://github.com/Jack-Kunlun/project-delivery-skill/tree/main/skills/project-delivery
```

需要固定版本时，把 `main` 替换为仓库 [Releases](https://github.com/Jack-Kunlun/project-delivery-skill/releases) 中的标签。已有安装时先比较差异，再明确更新原副本，不重复安装另一份。

### 手动安装（macOS / Linux）

先克隆仓库：

```sh
git clone https://github.com/Jack-Kunlun/project-delivery-skill.git
cd project-delivery-skill
```

在仓库根目录执行以下命令，复制到 Codex skills 目录。目标已存在时会停止，不覆盖原安装：

```sh
(
  destination="${CODEX_HOME:-$HOME/.codex}/skills/project-delivery"
  if [ -e "$destination" ] || [ -L "$destination" ]; then
    printf '%s\n' "Already exists: $destination. Compare it before updating."
    exit 1
  fi
  mkdir -p "$(dirname "$destination")"
  cp -R skills/project-delivery "$destination"
)
```

后续任务中调用该 skill。其他 Agent 的发现目录可能不同，按其安装机制放置完整 skill 文件夹。

## 使用示例

在目标项目内请求：

```text
使用 $project-delivery，为当前项目建立或补齐研发交付流程与台账。
先梳理现状，沿用已有记录。
```

接管老旧项目：

```text
使用 $project-delivery 接管这个老项目，整理已有能力、证据缺口、
已知问题和下一步。本轮只整理文档，不恢复运行环境，不升级依赖。
```

处理插单或复发问题：

```text
使用 $project-delivery 记录这项临时需求和重复出现的 UI 问题，
评估影响，保留原任务恢复点，追踪调查、预防措施和验收证据。
```

它适合项目接入与交付管理。普通单文件修改不会因此自动触发全项目审计或重建流程。

## 初始化与后续任务

初始化默认包含项目持续接续，不需要在请求中额外说明“写入 AGENTS”“持续维护台账”或“后续自动使用”。

Skill 会创建或更新**实际生效的项目级 Agent 指令**（通常是 `AGENTS.md`，同时考虑适用的覆盖文件），关联真实记录，并写入开工、过程更新、验收和收工规则。原有规则和编号保留；重复初始化更新原接入内容，不复制规则块或台账。仅在 README 放链接不算完成接入。

初始化后，可以直接提出正常工作请求：

```text
修复空库存列表的摘要，保留现有非空列表输出。
```

项目指令要求实质工作读取当前任务和相关经验，登记或关联工作项，记录变更与问题，完成适用检查，并留下结果和恢复点。用户无需反复点名 skill 或提醒记账。Skill 暂时不可用时，项目内的具体规则仍可执行，同时记录可用性缺口。

初始化验收包括一次不带流程提醒的新上下文接续检查。记录必须区分指令/链接检查、隔离 Agent 遵循指令的结果，以及实际宿主自动发现；三者不能互相替代。无法执行的检查明确保留为未验证。

旧版本已接入的项目，在下次使用 skill 时会于已授权项目范围内补齐缺失的接续规则。仅安装或更新 skill 不会静默修改既有项目。自动匹配保持开启；这套流程不会创建后台服务，也不会拦截每条包初始化命令。

## 工作方式

1. 找到实际项目，读取适用约定和权威记录；初始化时安装并验证项目持续接续入口。
2. 实质工作关联任务，文档整理和首次接入也要留痕。
3. 明确范围、责任、依赖、可观察的验收条件和有限验证计划。
4. 按项目自己的合同及要求执行和交接。
5. 回填实际结果、未验证项、决定和下一次恢复点。

参考资料按需读取。**已实现、已验收、已发布、线上已验证**分别记录。测试覆盖率需要明确的场景分母；源码判断、mock、浏览器检查、视觉审阅和真实集成不能相互替代。

## 接入项目中的 UI 验收

初始化会将 UI 专项规则写入项目本地指令：涉及 UI 时，读取当前设计与验收记录，按真实渲染状态对比后再验收。从受影响的条件区域及共享样式使用方选择用例，覆盖相关相邻区块、宽度和换行；记录预期与实际、候选及证据。构建、单元测试或路由巡检通过，不能替代必需的视觉检查。

必需检查缺失或失败时，UI 验收保持未通过。重复布局问题需要定向回归检查及后续效果复验。随包可执行门禁接入项目后可以阻断无依据的本地完成状态；它不等于远端分支保护，也不保证 UI 永远无错。已接入项目在下次获授权使用 skill 时补齐本地规则；仅更新安装包不会重写项目指令。详见[交付门槛](docs/zh-CN/references/delivery-gates.md)和[记录模板](docs/zh-CN/references/record-templates.md)。

## 可执行验收与复用

初始化现在会安装项目自有门禁，并接入真实检查和既有台账。输入、设计、工具、环境未变且完整有效的证据直接复用；只运行缺失、失效或失败的检查。没有证据时运行本任务完整适用范围，不自动跑全仓库测试。`complete` 在全部必需检查通过前阻止状态转换；`audit` 检出缺少有效历史完成证明的受管理已完成条目，并保留既有历史。

详见[配置、适配合同及命令](docs/zh-CN/references/automated-acceptance.md)。UI 检查必须返回所需用例结果，仅退出码为 0 不够；历史证据必须能核验关联，人工视觉审阅与自动测量分开。本地命令不能防止恶意改写文件，受保护 CI 或工单规则仍需实际接入。

## 语言与兼容性

主 README 使用英文，本文件提供中文说明。Skill 指令、参考资料和 Codex 显示元数据统一使用**英文**；[中文指令说明](docs/zh-CN/guide.md)及其配套参考资料提供对应的中文阅读版本，普通文档链接保持在中文文档内；需要切换语言时使用明确标注的英文原文入口。中文说明位于安装目录之外，不注册第二个 skill。

安装包包含英文 Markdown 指令、Codex UI 元数据和仅依赖 Python 3.9+ 标准库的验收执行器（写操作支持 macOS/Linux）；它运行已审阅项目命令并控制配置中的本地台账转换，不新增包管理依赖或后台服务。实际工具与发现机制取决于使用它的 Agent 环境。

## 文档导航

- [Skill 指令说明](docs/zh-CN/guide.md)
- [项目接入与持续初始化](docs/zh-CN/references/adopt-project.md)
- [老旧项目接管](docs/zh-CN/references/legacy-project.md)
- [记录模板](docs/zh-CN/references/record-templates.md)
- [交付、UI/UX 与测试验收](docs/zh-CN/references/delivery-gates.md)
- [自动验收与证据复用](docs/zh-CN/references/automated-acceptance.md)
- [持续改进](docs/zh-CN/references/improvement.md)
- [项目记录](docs/zh-CN/PROJECT.md)

## 目录结构

```text
skills/project-delivery/
  SKILL.md                       指令入口与资料导航
  agents/openai.yaml             Codex 显示元数据
  scripts/acceptance_gate.py      可执行证据与完成门禁
  references/
    adopt-project.md             沿用已有记录与首次建账
    legacy-project.md            老旧项目渐进接管
    record-templates.md          任务、问题、变更、交接、证据
    delivery-gates.md            生命周期、UI/UX、测试与验收
    improvement.md               复发问题与改进效果复验
    automated-acceptance.md      自动门禁配置与证据复用

docs/PROJECT.md                  权威维护记录（英文）
docs/zh-CN/                     中文阅读文档
  guide.md                       Skill 指令中文说明
  references/                    对应中文参考资料
  PROJECT.md                     同步的项目记录中文视图
  LICENSE.md                     MIT 许可证中文说明
```

## 验证与限制

翻译前的中文指令包在两个隔离样例中演练过：一个有既有台账，一个是无台账且暂不可运行的旧项目。首轮发现的接入工作漏入账、复发问题改进接续不足，已补强并复查。这是有限样例验证，不代表所有项目中的效果都已证明。英文包进行了语义、结构和安装检查，未重新执行英文行为演练。

发布检查覆盖文件一致性、skill 元数据、内部链接、文档中的手动安装步骤及已有安装保护。本次初始化/接续改动的专项行为证据与原演练分开记录。实际结果和发布状态见 [项目记录](docs/zh-CN/PROJECT.md)。

可执行门禁已通过 18 项定向行为测试及一次接入项目演练：14 个渲染布局用例、故意破坏间距的负例，以及通过实际项目命令复用未变证据。边界与审查修正记录于 PD-005，不代表全站 UI 已覆盖。

仅安装 skill 不会自动接通项目门禁、远端 CI 保护、持续监控或不可篡改审计系统；项目初始化须按上述流程配置并验证可执行接入。它也不会自动接入其他项目、修复缺陷，或授权提交、部署、生产访问和对外发送消息。项目约定与用户的实际授权仍然有效。

## 参与改进

提交 Issue 时说明具体场景、期望、实际结果及相关证据；不要上传凭据、私有项目资料或生产数据。

保持修改聚焦。公共使用方式变化时同步中英文 README，英文来源变更时同步对应中文说明。保持同语言导航和精简入口，并检查参考文件仍可使用。行为变化应以真实的隔离场景验证，不仅检查指令中是否出现某些文字。

## 许可证

[MIT](docs/zh-CN/LICENSE.md) © 2026 Fenglan。
