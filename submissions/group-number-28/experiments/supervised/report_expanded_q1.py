"""Build report section/figures from the expanded immutable evidence bundle."""
import argparse
import json
import os
from pathlib import Path
import tempfile

os.environ.setdefault("MPLCONFIGDIR",str(Path(tempfile.gettempdir())/"q1_matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME",str(Path(tempfile.gettempdir())/"q1_xdg_cache"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from human_ai.data import ROOT,read_csv

SHORT={"lr":"Logistic regression","nb":"Multinomial NB","svm":"Linear SVM + sigmoid",
       "tree":"Decision tree","forest":"Random forest","boost":"Gradient boosting",
       "mlp":"Neural network (MLP)","lr_svd":"LR (SVD control)"}
REPS={"sparse":"TF-IDF","dense":"SVD-128","scaled_dense":"SVD + scale"}


def tex(text):
    return str(text).replace("_",r"\_").replace("%",r"\%").replace("&",r"\&")


def compact(params):
    names={"C":"C","alpha":"alpha","max_depth":"depth","min_samples_leaf":"leaf",
           "n_estimators":"trees","max_features":"features","max_iter":"rounds",
           "learning_rate":"rate","max_leaf_nodes":"leaves","l2_regularization":"L2",
           "hidden_layer_sizes":"hidden","learning_rate_init":"rate"}
    parts=[]
    for key,value in params.items():
        if isinstance(value,float): value=f"{value:.5g}"
        if value is None:value="unlimited"
        if isinstance(value,list):value="-".join(str(v) for v in value)
        parts.append(f"{names.get(key,key)}={value}")
    return ", ".join(parts)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prefix",required=True)
    args=parser.parse_args()
    study=ROOT/"results/supervised"/f"{args.prefix}_study"
    rows=read_csv(study/"comparison.csv")
    cv=json.loads((study/"cv_results.json").read_text())
    progress=json.loads((study/"cv_progress.json").read_text())
    plan=json.loads((study/"q1_expanded_plan.json").read_text())
    chosen=json.loads((study/"chosen_parameters.json").read_text())
    selection=json.loads((study/"selection.json").read_text())
    uncertainty=json.loads((study/"bootstrap.json").read_text())
    seeds=json.loads((study/"mlp_secondary_seeds.json").read_text())
    winner=selection["winner"]
    ranked=sorted(rows,key=lambda r:float(r["validation_auroc"]),reverse=True)
    best,second=ranked[:2]
    low,high=uncertainty["winner_minus_other_95_intervals"][second["model"]]
    result_rows="\n".join(f"{SHORT[r['model']]} & {REPS[r['representation']]} & {float(r['train_auroc']):.6f} & {float(r['validation_auroc']):.6f} & {float(r['fit_seconds']):.2f}\\\\" for r in rows)
    tuning_rows=[]
    for r in rows:
        family=r["model"]
        candidates=[v for v in cv if v["model"]==family]
        bestcv=max(candidates,key=lambda v:v["mean_cv_auroc"])
        tuning_rows.append(f"{SHORT[family]} & {len(candidates)} & {tex(compact(chosen[family]))} & {bestcv['mean_cv_auroc']:.6f}\\\\")
    seed_aucs=[float(next(r for r in rows if r["model"]=="mlp")["validation_auroc"])]+[r["validation"]["auroc"] for r in seeds["runs"]]
    interval_claim=("This interval does not distinguish their ranking performance." if low<=0<=high else
                    "The conditional interval favors the selected model, but omits training and selection uncertainty.")
    body=r"""% Main author: Lin. Generated from actual expanded Q1 evidence.
\section{Model comparison and selection}
\noindent\textbf{Q1.1 [3 points]. How did you preprocess and represent the text? Specify tokenization, normalization, word/character features or embeddings, and any feature extraction choices. Why?}

We lowercase passages and extract Unicode word tokens of at least two characters
using \verb|(?u)\b\w\w+\b|. Word unigram/bigram TF-IDF uses minimum document
frequency two, at most 60,000 features, sublinear term frequency, smoothed IDF,
and L2 normalization. We retain stop words and apply no stemming, lemmatization,
or accent stripping, preserving function-word and local phrasing signals.
Linear models, NB, decision trees, and random forests use sparse TF-IDF directly.
Histogram gradient boosting uses 128 randomized SVD components because its
implementation requires dense input. The neural network uses those components
followed by standardization to keep optimization practical on a laptop. A scaled
SVD logistic-regression control helps separate representation effects from model
effects. Every learned transform is refitted inside each training fold; no
fixed-validation text or labels fit features. Different representations remain
a comparison limitation; character features are reserved for Q5.

\medskip
\noindent\textbf{Q1.2 [5 points]. Which three or more modeling approaches did you try? Keep the labeled validation partition fixed across models.}

\begin{center}\small
\begin{tabularx}{\linewidth}{@{}lXrrr@{}}
\toprule
Model & Representation & Train AUROC & Val. AUROC & Fit (s)\\
\midrule
__RESULT_ROWS__
\bottomrule
\end{tabularx}\end{center}
All models use the canonical 8,000 training and 2,000 validation IDs, balanced
by class. Timing includes all feature fitting and SVM calibration, excludes
search, and uses one CPU thread on macOS ARM64. These are single-run timings.
SVM probabilities use training-only three-fold sigmoid calibration of the entire
TF-IDF/classifier pipeline, with \texttt{ensemble=False}. MLP uses ReLU/Adam and
an internal stratified 10\% early-stopping split; its input transforms use 8,000
rows, while gradient updates use the other 90\%. No GPU, external weights,
unlabeled training, test fitting, or Kaggle feedback is used.
MLP's training diagnostic includes its internal stopping rows.

The single tree (__TREE_AUC__) trails the forest (__FOREST_AUC__), supporting
aggregation over this tree configuration. However, the forest takes __FOREST_TIME__
seconds versus __SVM_TIME__ for SVM, without improving held-out ranking.
Within the scaled SVD representation, MLP (__MLP_AUC__) outperforms the LR
control (__CONTROL_AUC__). Even after separate tuning, that LR control trails
sparse LR (__LR_AUC__); compression is a plausible limitation, not a demonstrated
cause. Forest and boosting training AUROCs are almost one while validation
AUROCs remain near 0.94, so added capacity does not eliminate generalization gaps.

\medskip
\ifdefined\QOnePreview\clearpage\fi
\noindent\textbf{Q1.3 [4 points]. For at least two approaches, which hyperparameters and candidate values did you try? How did you select the final settings without using Kaggle test labels?}

\begin{center}\small
\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}p{1.5in}rXr@{}}
\toprule
Model & Tried & Chosen configuration & CV AUROC\\
\midrule
__TUNING_ROWS__
\bottomrule
\end{tabularx}\end{center}
We searched __N_CANDIDATES__ distinct configurations with three identical stratified,
shuffled folds inside the 8,000 training rows (seed 142), giving __N_FITS__
candidate-fold fits. A coarse grid was followed by one predeclared local
refinement around each family's best mean training-CV AUROC; exact ties retain
the first candidate. The appendix lists all initial values and refinement
rules; machine-readable files retain every exact tested configuration and
fold score. Vocabulary, SVD, and scaling are refitted per fold. Model and SVD
seeds are 42; SVM calibration uses seed 242. Parameter selection is completed
before the expanded held-out comparison. These settings are best among those
tested, not proven global optima; further tuning on the same folds could
overfit cross-validation.

\medskip
\noindent\textbf{Q1.4 [3 points]. Which approach did you choose for your final submission? Explain using validation performance, computational cost and/or stability. If you later changed the model, explain why.}

The expanded Q1 candidate is __WINNER__ with validation AUROC __BEST_AUC__.
Its lead over __SECOND__ is __DELTA__; 1,000 stratified paired bootstrap
replicates give a 95\% difference interval [__LOW__, __HIGH__]. __INTERVAL_CLAIM__
The old validation set was already inspected in the initial three-model study,
so this extension is a development comparison rather than an untouched final
estimate. Bootstrap intervals condition on fitted models and omit model-selection
correction. Fit times and training/validation gaps inform cost and overfitting
trade-offs; unsuccessful tree, ensemble, and neural settings are retained.
MLP validation AUROC ranges from __MLP_MIN__ to __MLP_MAX__ across seeds 42, 7,
and 142; seed 42 remains the primary result, without selecting the best seed.
The team-wide choice remains open after Q3/Q5. Hidden-domain performance and
near-duplicate/source leakage are still unresolved; no private-test score is claimed.

{\footnotesize Evidence: study \texttt{__STUDY__} under \texttt{results/supervised/};
all eight final 8,000-row checkpoints and validation predictions are retained.
Any full-data submission refit is separate and has no honest score on the former validation rows.}
"""
    substitutions={"__RESULT_ROWS__":result_rows,"__TUNING_ROWS__":"\n".join(tuning_rows),
                   "__N_CANDIDATES__":str(len(cv)),"__N_FITS__":str(len(progress)),
                   "__WINNER__":SHORT[winner],"__SECOND__":SHORT[second["model"]],
                   "__BEST_AUC__":f"{float(best['validation_auroc']):.6f}",
                   "__DELTA__":f"{float(best['validation_auroc'])-float(second['validation_auroc']):.6f}",
                   "__LOW__":f"{low:.6f}","__HIGH__":f"{high:.6f}","__INTERVAL_CLAIM__":interval_claim,
                   "__MLP_MIN__":f"{min(seed_aucs):.6f}","__MLP_MAX__":f"{max(seed_aucs):.6f}",
                   "__STUDY__":tex(study.name)}
    by_family={r["model"]:r for r in rows}
    for name,family in (("TREE","tree"),("FOREST","forest"),("MLP","mlp"),("CONTROL","lr_svd"),("LR","lr")):
        substitutions[f"__{name}_AUC__"]=f"{float(by_family[family]['validation_auroc']):.6f}"
    substitutions["__FOREST_TIME__"]=f"{float(by_family['forest']['fit_seconds']):.2f}"
    substitutions["__SVM_TIME__"]=f"{float(by_family['svm']['fit_seconds']):.2f}"
    for key,value in substitutions.items():body=body.replace(key,value)
    (ROOT/"report/sections/q1.tex").write_text(body)

    appendix=[r"\section*{Supplement: actual search ranges and limitations}"]
    for family in plan["families"]:
        initial=plan["initial_grids"][family]
        ranges="; ".join(f"{tex(key)}: {tex(str(values))}" for key,values in initial.items())
        refined=[r for r in cv if r["model"]==family and r["stage"]==2]
        extra="; ".join(compact(r["parameters"]) for r in refined)
        appendix.append(r"\textbf{"+SHORT[family]+r".} Initial grid: "+ranges+r".\par "+
                        r"Refinement configurations: "+tex(extra)+r".\par\medskip")
    warnings_count=sum(len(r["warnings"]) for r in progress)
    convergence_count=sum(w["category"]=="ConvergenceWarning" for r in progress for w in r["warnings"])
    appendix.append(r"\textbf{MLP and convergence.} ReLU/Adam; at most 500 epochs, internal early stopping on accuracy, "+
                    r"validation fraction 0.1, patience 20, tolerance $10^{-4}$. Candidate-fold fitting warnings recorded: "+str(warnings_count)+r"; convergence warnings: "+str(convergence_count)+r". "+
                    r"All warnings, stopping iterations, and exact floating-point settings are stored in the run evidence.\par")
    appendix.append(r"\textbf{Interpretation.} Representation changes are explicit, and the SVD LR control is included. "+
                    r"Neither a single random split nor these development-set scores establishes performance on unfamiliar domains or generators. "+
                    r"The original v1 plan and artifacts remain unchanged. No seed or hyperparameter was selected using Kaggle feedback.")
    (ROOT/"report/sections/q1_expanded_search.tex").write_text("\n\n".join(appendix)+"\n")

    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"axes.spines.top":False,"axes.spines.right":False})
    out=ROOT/"report/figures"
    fig,ax=plt.subplots(figsize=(10,5.5),constrained_layout=True)
    for i,row in enumerate(rows):
        f=row["model"];value=float(row["validation_auroc"])
        low,high=uncertainty["auroc_95_intervals"][f]
        color="#147d92" if row["representation"]=="sparse" else "#b16c30"
        ax.errorbar(value,i,xerr=[[value-low],[high-value]],fmt="o",capsize=3,color=color)
        ax.scatter(float(row["train_auroc"]),i,marker="^",color="#9099a1",s=30)
        ax.annotate(f"{value:.6f}",(value,i),xytext=(0,10),textcoords="offset points",ha="center",fontsize=8)
    ax.set_yticks(range(len(rows)),[SHORT[r["model"]] for r in rows])
    ax.set_ylim(len(rows)-0.4,-0.65)
    ax.set_xlim(min(uncertainty["auroc_95_intervals"][r["model"]][0] for r in rows)-0.03,1.01)
    ax.set_xlabel("AUROC");ax.grid(axis="x",alpha=.2)
    ax.set_title("Expanded Q1: fixed 8,000 / 2,000 development split",loc="left",fontweight="bold",pad=15)
    fig.suptitle("Dots/whiskers: validation + conditional 95% bootstrap CI; triangles: training\nBlue: sparse TF-IDF; orange: SVD representations; intervals are not selection-adjusted",y=-.02,fontsize=9)
    fig.savefig(out/f"q1_{args.prefix}_comparison.png",dpi=180,bbox_inches="tight");plt.close(fig)
    fig,ax=plt.subplots(figsize=(10,4.5),constrained_layout=True)
    for i,family in enumerate(plan["families"]):
        candidates=[r for r in cv if r["model"]==family]
        for stage,color in ((1,"#a9b5c2"),(2,"#cf7b36")):
            values=[r["mean_cv_auroc"] for r in candidates if r["stage"]==stage]
            ax.scatter(values,[i]*len(values),color=color,s=27,alpha=.8,label=f"Stage {stage}" if i==0 else None)
        bestcv=max(candidates,key=lambda r:r["mean_cv_auroc"])
        ax.scatter(bestcv["mean_cv_auroc"],i,s=110,facecolors="none",edgecolors="#17364d",lw=1.5)
    ax.set_yticks(range(len(plan["families"])),[SHORT[f] for f in plan["families"]]);ax.invert_yaxis()
    ax.set_xlabel("Mean training-only CV AUROC (3 shared folds)");ax.grid(axis="x",alpha=.2)
    ax.set_title(f"{len(cv)} distinct configurations; rings mark the selected settings",loc="left",fontweight="bold")
    ax.legend(frameon=False,fontsize=9)
    fig.savefig(out/f"q1_{args.prefix}_search.png",dpi=180,bbox_inches="tight");plt.close(fig)
    print(f"Updated report Q1 and expanded figures from {study.name}")


if __name__=="__main__":main()
