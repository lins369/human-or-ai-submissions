# Lin Q1 handoff

## 当前扩展版（November 8）

Q1 现覆盖 LR、NB、SVM、决策树、随机森林、梯度 boosting、MLP 神经网络，以及
一个 SVD 表示的 LR 对照；64 组配置、192 次训练内折评估均已完成。
新增模型的参数由训练内粗搜索与预先规定的一轮细化自动选择，完整设置和结果见
`experiments/supervised/README.md` 及 `a_q1_expanded_20261108_v2_study`。

- SVM C=1 仍暂选，验证 AUROC 0.943876；LR C 调至 33.33333333333333，AUROC 0.943699。
- 决策树 0.812888，随机森林 0.936392，boosting 0.939490，MLP 0.939616。
- 稀疏 TF-IDF 用于前五种模型；boosting 用 SVD-128，MLP 用 SVD-128＋标准化。
  相同缩放 SVD 上的 LR 对照为 0.922601，不能把全部差异归因于分类器。
- MLP 换种子 7/142 后为 0.936834/0.940165，主结果仍是事先指定的种子 42。
- Alex 最新 Q4 输入：`results/supervised/a_q1_expanded_20261108_v2_svm/validation_predictions.csv`。
  SVM 设置未变，该验证预测文件与初版逐字节相同。
- 所有八模型已独立新建实例重训，验证概率与保存文件完全一致。新增三项模型/表示/
  数据泄漏检查通过，零模型收敛警告；干净环境、跨机器验证仍待 Gabriel 执行。
- 当前全量候选：`submissions/a_q1_expanded_20261108_v2_svm_full10000.csv`。
  由于获选 SVM 未变，该 CSV 的 SHA-256 与初版候选相同，无需重复占用 Kaggle 提交名额。
- 当前报告 `report/sections/q1.tex` 和四页 `output/pdf/q1_results.pdf` 已更新；
  参数附页为 `report/sections/q1_expanded_search.tex`。初版 PDF/source 已归档。
- “最佳”仅指实测搜索内最佳，不是全局最优。验证集已在 v1 查看过，扩展版是开发比较；
  bootstrap 未校正模型选择。没有查看 Kaggle 分数，也未开展 Q5 字符特征实验。
- 本轮 AI 还辅助实现新增模型、参数搜索、表示对照、随机种子稳定性和重新编写报告。
  下方 AI-use disclosure 仍需 Lin 按本人实际检查情况审阅；不代称队员已亲自验证。

## 以下为初版三模型记录（历史）

Q1.1-Q1.4 已完成真实实验和英文正文。分工：Lin Q1/Q5；Alex Q2/Q4；Gabriel Q3/Q6。
本次未开展 Q5，未修改原始数据、共享划分或队友的实验/报告文件。

## 结论与交接

- 当前 Q1 候选 SVM C=1：验证 AUROC 0.943876；训练 AUROC 1.0；验证 accuracy@0.5 为 0.871。
- LR C=10：0.943436；与 SVM 差 0.000440，配对区间跨零，不能声称显著领先。
- NB alpha=0.1：0.906051；相同特征/划分下的有效负结果，不能推论所有 NB 都差。
- 以上来自固定 8,000/2,000 划分，不是 Kaggle Public/Private 分数。
- Alex 的 Q4 输入：`results/supervised/a_q1_20261107_v1_svm/validation_predictions.csv`。
  2,000 行，`id,label,p_ai`，按 ID 对齐；分析中注明阈值。全队换模型后须更新 Q4。
  Q2 可以保留自己的固定基线。
- `..._svm_full10000/` 用到原验证标签，不能拿来做 Q4 留出评估。
- Gabriel 的复现命令、精确依赖见 `experiments/supervised/README.md`。测试 Python 3.12.7。
  共享检查 10 项、监督实验检查 4 项通过。三模型在新实例中重训，验证概率逐项完全相同。
  这是同一现有环境的复跑；干净环境/另一台机器的独立复现仍待执行。

## 本地候选提交

`submissions/a_q1_20261107_v1_svm_full10000.csv` 是 Q1 选定设置后全量重训的
3,000 行候选，`id,label`，label 为 AI 概率，格式已检查。metadata 记录来源和 CSV 哈希。
未上传 Kaggle，未消耗提交额度，未写入 leaderboard 分数。全队最终选择待 Q3/Q5。

## 复现与开发记录

实验基于 scaffold commit `17aba0e1f0c7b87fa597b4afb53e0cf8db61b2f9`，工作区有
未提交改动；真实 dirty 状态和执行源码哈希已记录，study 中存有源码快照。
没有虚构 commit/PR 链接；后续实际提交时保留开发历史。模型和原始文本不进 Git。
原始 `old_rubric.tex` 未改；已考虑其中 Q1 标准与用户提供的 Project Expectations，
但未核实最新模板、最终满分阈值或截止时间。

## AI-use disclosure draft for Lin to review

Codex assisted with experimental design, Python implementation, execution,
automated verification, interpretation, plots, and the English Q1 draft. The
assistant checked source/split hashes, fold-local feature fitting, calibration
boundaries, probability/schema correctness, metric reconstruction and fresh
refits. Team members' personal review has not been observed or claimed. Lin
should review the implementation and explanations and record the checks Lin
personally performed or modified before adapting this disclosure for Q6.3.
Local sklearn models generated predictions; no external LLM API labeled
competition passages, and no hidden test labels were obtained.

## 新增共识与待验证项

采用同表示比较分类器、训练内部调参、固定验证集比较方法，保留全部负结果。
延续各 track 独立运行、按 ID/预测文件交接的偏好。SVM 名义最高，LR 更快且差异不明确。
待验证：字符特征增益、近重复/来源泄漏、跨机器复现、隐藏测试泛化。
Q5 最小实验建议固定 LR C=10 或 SVM C=1 与原划分，仅改变词/字符/组合表示；
收集 AUROC、配对差值区间、耗时和特征数。这是设计，不是已测结果。
