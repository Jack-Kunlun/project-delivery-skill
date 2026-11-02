# Project Delivery · 项目研发交付流程

一个可复用的 Agent skill，用于追踪需求、设计、开发、测试、验收、上线和持续改进。

[English](README.md) · [Skill 指令](skills/project-delivery/SKILL.md) · [MIT 许可证](LICENSE)

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

## 工作方式

1. 找到实际项目，读取适用约定和权威记录。
2. 实质工作关联任务，文档整理和首次接入也要留痕。
3. 明确范围、责任、依赖、可观察的验收条件和有限验证计划。
4. 按项目自己的合同及要求执行和交接。
5. 回填实际结果、未验证项、决定和下一次恢复点。

参考资料按需读取。**已实现、已验收、已发布、线上已验证**分别记录。测试覆盖率需要明确的场景分母；源码判断、mock、浏览器检查、视觉审阅和真实集成不能相互替代。

## 语言与兼容性

主 README 使用英文，本文件提供中文说明。Skill 指令、参考资料和 Codex 显示元数据统一使用**英文**；本文件提供中文安装与使用说明，不另维护一份中文指令包。

安装包包含 Markdown 指令和可选的 Codex UI 元数据，没有应用运行时、包管理依赖、后台服务或可执行自动化。实际工具与发现机制取决于使用它的 Agent 环境。

## 目录结构

```text
skills/project-delivery/
  SKILL.md                       指令入口与资料导航
  agents/openai.yaml             Codex 显示元数据
  references/
    adopt-project.md             沿用已有记录与首次建账
    legacy-project.md            老旧项目渐进接管
    record-templates.md          任务、问题、变更、交接、证据
    delivery-gates.md            生命周期、UI/UX、测试与验收
    improvement.md               复发问题与改进效果复验

docs/PROJECT.md                  本仓库的维护记录
```

## 验证与限制

原 skill 在两个隔离样例中演练过：一个有既有台账，一个是无台账且暂不可运行的旧项目。首轮发现的接入工作漏入账、复发问题改进接续不足，已补强并复查。这是有限样例验证，不代表所有项目中的效果都已证明。

发布检查覆盖文件一致性、skill 元数据、内部链接、文档中的手动安装步骤及已有安装保护。实际结果和发布状态见 [项目记录](docs/PROJECT.md)。

安装 skill 不会自动创建 CI 门禁、持续监控或不可篡改审计系统，也不会自动接入其他项目、修复缺陷，或授权提交、部署、生产访问和对外发送消息。项目约定与用户的实际授权仍然有效。

## 参与改进

提交 Issue 时说明具体场景、期望、实际结果及相关证据；不要上传凭据、私有项目资料或生产数据。

保持修改聚焦。公共使用方式变化时同步中英文 README，保持入口精简，并检查参考文件仍可使用。行为变化应以真实的隔离场景验证，不仅检查指令中是否出现某些文字。

## 许可证

[MIT](LICENSE) © 2026 Fenglan。
