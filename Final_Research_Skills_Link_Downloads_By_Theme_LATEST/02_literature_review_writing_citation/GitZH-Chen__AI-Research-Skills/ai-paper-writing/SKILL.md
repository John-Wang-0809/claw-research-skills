---
name: ai-paper-writing
description: Assist with drafting, polishing, grammar checking, and BibTeX cleaning for AI top-tier conference or journal papers in LaTeX. Use when working on manuscripts targeting venues such as ICLR, NeurIPS, ICML, CVPR, ICCV, ECCV, AAAI, IJCAI, KDD, WWW, IEEE TPAMI, IEEE TMM, IEEE TIP, IEEE TNNLS, IJCV, JMLR, or TMLR.
---

# AI Top Paper Writing

## 1. Project Overview

Treat the manuscript as submission-targeted work for an AI top conference or top journal.
If the user specifies a target venue and year, follow that target strictly.
If unspecified, follow the writing style of top-tier AI conferences such as CVPR, ICCV, NeurIPS, ICML, and ICLR.

At the beginning of each skill invocation, return the checklist below and ask the user to confirm or update each item before writing:

- `./Aux`: manuscript support materials
- `./Aux/Rebuttal`: rebuttal materials
- `./Aux/Rebuttal/{venue}-Reviews.md`: review file (for example `ICLR26-Reviews.md`).
- `preamble.tex`: predefined LaTeX macros
- `xx.bib`: bibliography source (`\bibliography{xx.bib}`)
- `Aux/Guidelines.pdf`: formatting guideline.

All checklist items are optional. If any item is missing, return a concise hint about its purpose and how to provide it, then continue with the available context.

---

## 2. Writing and Formatting Requirements

### 2.1 LaTeX Conventions

When writing equations and text in LaTeX (Overleaf), please follow these specific rules carefully:

- **Do not use prohibited spacing commands.**  Avoid `\;`, `\!`, or `\,` at all times.

- **Adaptive brackets.**  Always use `\left` and `\right` for scalable delimiters (parentheses, brackets, braces, absolute values, etc.). Do **not** use manual size commands such as `\big`, `\Big`, `\bigl`, `\bigr`, `\biggl`, or `\Biggl`, unless i explicitly require so. Use plain `(`, `)`, `[`, `]`, `{`, `}`, and `|` when no scaling is needed, and use `\left.` / `\right.` for invisible delimiters.


- **Predefined macros.**  Use only the macros already defined in `preamble.tex`.  
  Do not redefine or modify them locally within any section.

- **Bibliography management.**  
  Use the following bibliography sources only:  

  ```latex
  \bibliography{xx.bib}
  ```

  Do not create new or fabricated references.  
  If a reference is missing, request the citation so that it can be added.

- **Prohibition of sentence splitting dashes.** Do not use any long dash symbols such as `--` or `---` to separate or cut sentences. When you need a pause or a shift in tone, use commas, conjunctions, or split the content into two sentences instead. You are still allowed to use `-` and `--` in compound words, such as "manifold-valued point", "point-to-horosphere", "ResNet-18", 'Beltrami--Klein' and so on, and to use standard dash notation where it is required.

- Please use `$...$` not `\(...\)` for inline equations; 

- **Display equations.**  Use `\begin{equation} ... \end{equation}` or `\begin{align} ... \end{align}` for display equations instead of `\[ ... \]`. Display equations do not require labels unless they are cited later. In the appendix, do **not** use `align` unless sub-equations must be labeled, or I explicitly require so. Use `aligned` within `equation` for multi-line equations to avoid generating unnecessary equation numbers.


- When introducing the terminology for the first time, please use `\emph{}`. For instance the terminology in `\begin{definition}`, and terminology in the main text when we do not use definition environment. If the terminology first shown in text and then formally defined in `\begin{definition}`, please use `\emph{}` only in the `\begin{definition}`.

- Use `\textbf{xxxx.}` instead of `\paragraph{xxxx}` to highlight the heading of each paragraph.

- When describing a set, use `\{x \mid \text{condition}\}` instead of `\{x : \text{condition}\}`.

- When writing or editing the manuscript, minimize the use of semicolons (“;”) unless strictly necessary, such as when enumerating multiple complex items within a single sentence (e.g., “(1); (2); (3); …”). If the sentence can be clearly expressed as two separate sentences without affecting logical continuity, prefer splitting it rather than connecting with a semicolon. 
---

### 2.2 Writing Style and Editing Rules

When providing academic writing assistance or polishing text, follow these principles:

- **Preserve mathematical and technical accuracy.**  
  Do not change the meaning, symbols, or any LaTeX command within equations.

- **Enhance academic fluency and clarity.**  
  Rewrite in precise and professional English consistent with AI top-tier papers, such as CVPR/ICCV/NeurIPS/ICML/ICLR.

- **Maintain consistency across sections.**  
  Ensure uniform notation, flow, and tone throughout the entire manuscript.

- When asked to write, polish, or rewrite a section, always read the surrounding context to ensure consistency in notation, terminology, and logic.  Adhere to the above LaTeX conventions and writing style rules. 

### 2.3 **Refs**
All Refs as well as the manuscript can be found in `./Aux`.

---

## 3. Collaboration and Writing Procedure

### 3.1 Academic Writing Assistance

I may provide initial drafts, mathematical derivations, or conceptual notes. You will return a refined, publication-ready LaTeX version that meets the formal style of top-tier AI venues. You can revise my latex directly, unless I indicate otherwise.

When working on conceptual notes or bullet points, You will convert them into coherent academic text and ensure consistent mathematical presentation.

If a citation, definition, or formula is missing, You will explicitly note it so that the missing item can be added later.

---

### 3.2 Grammar check
When asked to perform a `grammar check`, only identify and correct grammatical errors without rephrasing or polishing the sentences. Do not alter style, structure, or word choice. Additionally, verify that all LaTeX commands comply with the project’s LaTeX Conventions. 

Also check if there is any place violates the guidelines in `Aux/Guidelines.pdf`. If there are no explicit instructions, you may directly make the necessary corrections in the LaTeX source.

### 3.3 Prompt: Bib Check Instruction

When I say `bib check`, please automatically clean and standardize my `.bib` file according to the following rules:

- Apply the formatting rules **only** to entries from the following top-tier conferences and journals:  
  **ICML, ICLR, NeurIPS, ICCV, CVPR, ECCV, AAAI, IJCAI, KDD, WWW, IEEE TPAMI, IEEE TMM, IEEE TIP, IEEE TNNLS, IJCV, JMLR, TMLR**.

- For each matching entry, keep **only** the following fields: `title`, `author`, `booktitle` (or `journal`), and `year`.

- Remove all other fields (e.g., `abstract`, `pages`, `doi`, `url`, `volume`, `number`, `publisher`, `address`, `organization`, `isbn`, `series`, `note`, `month`).

- Normalize venue names to their official **abbreviated forms**, such as:  
  - NeurIPS, ICML, ICLR, CVPR, ICCV, ECCV, AAAI, IJCAI, KDD, WWW, 
  - IEEE TPAMI, IEEE TIP, IEEE TMM, IEEE TNNLS, IJCV, JMLR, TMLR.  
  Replace full names with abbreviations and auto-fill missing venue info if inferable.

- The cleaned entries must follow this exact structure (no extra fields, no extra blank lines):

\`\`\`bibtex
@inproceedings{bdeir2025robust,
  title = {Robust Hyperbolic Learning with Curvature-Aware Optimization},
  author = {Ahmad Bdeir and Johannes Burchert and Lars Schmidt-Thieme and Niels Landwehr},
  booktitle = {NeurIPS},
  year = {2025}
}
\`\`\`

- Output **only** the cleaned `.bib` content, without comments or explanations.  
- Do **not** reorder keys unless the key is clearly invalid; otherwise preserve original citation keys.
- During bib check, also detect **potential duplicate references**: two entries should be treated as potential duplicates if they have (almost) identical `title` and `author` information, even if their citation keys are different. In such cases, **do not delete or merge them automatically**. Instead, explicitly list and report these suspected duplicates back to me so that I can decide how to modify them.
