# Meta-Analysis: Data-Efficient Reasoning in LLMs (2025)

A comprehensive analysis of three short, high-impact papers that demonstrate how sophisticated reasoning can emerge from minimal interventions in Large Language Models.

## 📄 Papers Analyzed

| Paper                                    | Authors            | Date     | arXiv                                          | Venue      |
| ---------------------------------------- | ------------------ | -------- | ---------------------------------------------- | ---------- |
| **s1: Simple test-time scaling**         | Muennighoff et al. | Jan 2025 | [2501.19393](https://arxiv.org/abs/2501.19393) | EMNLP 2025 |
| **LIMO: Less is More for Reasoning**     | Ye et al.          | Feb 2025 | [2502.03387](https://arxiv.org/abs/2502.03387) | COLM 2025  |
| **Coconut: Chain of Continuous Thought** | Hao et al.         | Dec 2024 | [2412.06769](https://arxiv.org/abs/2412.06769) | ICLR 2025  |

## 🎯 Unifying Theme

All three papers converge on the same insight: **reasoning capabilities are latent in foundation models** and can be elicited through minimal, precise interventions rather than massive computational investment.

- **s1**: Uses just 1,000 curated examples + "budget forcing" to exceed o1-preview by 27%
- **LIMO**: Achieves 63.3% on AIME24 with only 817 training samples (1% of prior approaches)
- **Coconut**: Enables reasoning in latent space, bypassing language tokens entirely

## 📊 Key Results

| Model   | AIME24              | Training Data       | Key Innovation             |
| ------- | ------------------- | ------------------- | -------------------------- |
| s1-32B  | 57%                 | 1,000 examples      | Budget forcing (test-time) |
| LIMO    | 63.3%               | 817 examples        | Cognitive templates        |
| Coconut | N/A (logical tasks) | Curriculum learning | Latent reasoning           |

## 📁 Repository Contents

```
├── meta_analysis_llms.pdf    # 6-page report with full analysis
├── README.md                 # This file
└── generate_report.py        # Python script to regenerate the PDF
```

## 🔗 Paper Links

### s1: Simple test-time scaling

- **arXiv**: https://arxiv.org/abs/2501.19393
- **GitHub**: https://github.com/simplescaling/s1
- **Model**: https://huggingface.co/simplescaling/s1-32B

### LIMO: Less is More for Reasoning

- **arXiv**: https://arxiv.org/abs/2502.03387
- **GitHub**: https://github.com/GAIR-NLP/LIMO
- **Model**: https://huggingface.co/GAIR/LIMO-v2

### Coconut: Chain of Continuous Thought

- **arXiv**: https://arxiv.org/abs/2412.06769
- **GitHub**: https://github.com/facebookresearch/coconut

## 📖 Citation

If referencing this analysis:

```bibtex
@misc{meta_analysis_reasoning_2026,
  title={Meta-Analysis: Data-Efficient Reasoning in LLMs},
  year={2026},
  month={January},
  note={Analysis of s1, LIMO, and Coconut papers}
}
```

### Original Papers

```bibtex
@inproceedings{muennighoff2025s1,
  title={s1: Simple test-time scaling},
  author={Muennighoff, Niklas and Yang, Zitong and Shi, Weijia and Li, Xiang Lisa and Fei-Fei, Li and Hajishirzi, Hannaneh and Zettlemoyer, Luke and Liang, Percy and Candes, Emmanuel and Hashimoto, Tatsunori},
  booktitle={EMNLP},
  year={2025}
}

@inproceedings{ye2025limo,
  title={LIMO: Less is More for Reasoning},
  author={Ye, Yixin and Huang, Zhen and Xiao, Yang and Chern, Ethan and Xia, Shijie and Liu, Pengfei},
  booktitle={COLM},
  year={2025}
}

@inproceedings{hao2025coconut,
  title={Training Large Language Models to Reason in a Continuous Latent Space},
  author={Hao, Shibo and Sukhbaatar, Sainbayar and Su, DiJia and Li, Xian and Hu, Zhiting and Weston, Jason and Tian, Yuandong},
  booktitle={ICLR},
  year={2025}
}
```

## 💡 Key Takeaways

1. **Superficial Alignment Hypothesis extends to reasoning**: ~1,000 high-quality examples suffice
2. **Quality beats quantity**: Careful curation outperforms brute-force data scaling
3. **Emergent behaviors**: Self-correction and BFS-like search arise without explicit training
4. **Latent capabilities**: Modern foundation models already "know" how to reason
