#!/usr/bin/env python3
"""
Meta-Analysis Report Generator: Data-Efficient Reasoning in LLMs (2025)
Focuses on short, high-impact papers
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, ListFlowable, ListItem
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT


def create_styles():
    """Create custom styles for the document."""
    styles = getSampleStyleSheet()

    # Title style
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Title'],
        fontSize=18,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1a1a2e')
    ))

    # Section heading
    styles.add(ParagraphStyle(
        name='SectionHeading',
        parent=styles['Heading1'],
        fontSize=14,
        spaceBefore=16,
        spaceAfter=10,
        textColor=colors.HexColor('#16213e'),
        borderWidth=0,
        borderPadding=0,
    ))

    # Subsection heading
    styles.add(ParagraphStyle(
        name='SubHeading',
        parent=styles['Heading2'],
        fontSize=12,
        spaceBefore=12,
        spaceAfter=6,
        textColor=colors.HexColor('#0f3460')
    ))

    # Body text - justified
    styles.add(ParagraphStyle(
        name='CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceBefore=4,
        spaceAfter=8
    ))

    # Bullet style
    styles.add(ParagraphStyle(
        name='BulletText',
        parent=styles['Normal'],
        fontSize=10,
        leading=13,
        leftIndent=20,
        spaceBefore=2,
        spaceAfter=2
    ))

    # Abstract/quote style
    styles.add(ParagraphStyle(
        name='Abstract',
        parent=styles['Normal'],
        fontSize=10,
        leading=13,
        leftIndent=30,
        rightIndent=30,
        fontName='Helvetica-Oblique',
        textColor=colors.HexColor('#333333'),
        spaceBefore=8,
        spaceAfter=8
    ))

    # Caption style
    styles.add(ParagraphStyle(
        name='Caption',
        parent=styles['Normal'],
        fontSize=9,
        alignment=TA_CENTER,
        textColor=colors.gray,
        spaceBefore=4,
        spaceAfter=12
    ))

    return styles


def build_document():
    """Build the complete PDF document."""
    doc = SimpleDocTemplate(
        "./meta_analysis_llms.pdf",
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    styles = create_styles()
    story = []

    # =========================================================================
    # TITLE PAGE
    # =========================================================================
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph(
        "Meta-Analysis of LLM Research Papers",
        styles['CustomTitle']
    ))
    story.append(Paragraph(
        "Data-Efficient Reasoning: Breakthroughs in 2025",
        ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=14,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#4a4a4a'),
            spaceAfter=30
        )
    ))
    story.append(Paragraph(
        "January 2026",
        ParagraphStyle(
            'Date', parent=styles['Normal'], alignment=TA_CENTER, fontSize=11)
    ))
    story.append(Spacer(1, 0.5*inch))

    # Papers analyzed box
    papers_text = """
    <b>Papers Analyzed (all ≤20 pages):</b><br/><br/>
    1. <b>s1: Simple test-time scaling</b> (Muennighoff et al., Jan 2025)<br/>
    2. <b>LIMO: Less is More for Reasoning</b> (Ye et al., Feb 2025)<br/>
    3. <b>Coconut: Chain of Continuous Thought</b> (Hao et al., Dec 2024/ICLR 2025)
    """
    story.append(Paragraph(papers_text, ParagraphStyle(
        'PapersBox',
        parent=styles['Normal'],
        fontSize=10,
        leading=16,
        leftIndent=40,
        rightIndent=40,
        borderWidth=1,
        borderColor=colors.HexColor('#e0e0e0'),
        borderPadding=15,
        backColor=colors.HexColor('#f8f9fa')
    )))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 1: INTRODUCTION
    # =========================================================================
    story.append(Paragraph("1. Introduction", styles['SectionHeading']))

    intro_text = """
    The year 2025 has witnessed a paradigm shift in how we approach reasoning capabilities 
    in Large Language Models. While the previous generation of research focused on scaling 
    model size and training data, three influential papers have demonstrated that 
    <b>sophisticated reasoning can emerge from remarkably minimal interventions</b>—whether 
    through small curated datasets, simple test-time techniques, or reasoning in latent space.
    """
    story.append(Paragraph(intro_text, styles['CustomBody']))

    intro_text2 = """
    This meta-analysis examines three concise yet highly impactful papers 
    that collectively challenge the conventional wisdom of "more is better" in machine learning. 
    Together, they reveal a unifying insight: <b>the reasoning capabilities we seek may already 
    exist within foundation models</b>, waiting to be elicited through precise, minimal interventions 
    rather than massive computational investment.
    """
    story.append(Paragraph(intro_text2, styles['CustomBody']))

    # Theme
    story.append(Paragraph(
        "Unifying Theme: Minimal Interventions, Maximal Reasoning", styles['SubHeading']))
    theme_text = """
    Each paper attacks the problem from a different angle—test-time compute, training data 
    efficiency, and latent space reasoning—yet arrives at the same conclusion: less can 
    indeed be more. This convergence suggests we are witnessing a fundamental shift in our 
    understanding of how reasoning emerges in neural networks.
    """
    story.append(Paragraph(theme_text, styles['CustomBody']))

    # =========================================================================
    # SECTION 2: PAPER SUMMARIES
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("2. Paper Summaries", styles['SectionHeading']))

    # --- Paper 1: s1 ---
    story.append(
        Paragraph("2.1 s1: Simple test-time scaling", styles['SubHeading']))
    story.append(Paragraph(
        "<i>Muennighoff et al., Stanford/FAIR, January 2025 | arXiv:2501.19393 | EMNLP 2025</i>",
        styles['Caption']
    ))

    s1_problem = """
    <b>Problem:</b> OpenAI's o1 demonstrated that test-time scaling—using additional compute 
    during inference—could dramatically improve reasoning. However, the methodology remained 
    proprietary, leaving the research community without a reproducible approach.
    """
    story.append(Paragraph(s1_problem, styles['CustomBody']))

    s1_solution = """
    <b>Solution:</b> The s1 paper identifies the <i>simplest possible</i> approach to achieve 
    test-time scaling through two key innovations:
    """
    story.append(Paragraph(s1_solution, styles['CustomBody']))

    s1_bullets = [
        "<b>s1K Dataset:</b> Just 1,000 carefully curated questions with reasoning traces, selected for difficulty, diversity, and quality from Gemini Flash Thinking outputs.",
        "<b>Budget Forcing:</b> A novel technique that controls test-time compute by (a) forcefully terminating thinking when over budget, or (b) appending 'Wait' tokens when the model tries to stop early, inducing self-correction."
    ]
    for bullet in s1_bullets:
        story.append(Paragraph(f"• {bullet}", styles['BulletText']))

    s1_key = """
    <b>Key Insight:</b> The 'Wait' token doesn't simply extend generation time—it triggers 
    genuine reconsideration. When the model says "The answer is 2" and is forced to continue 
    with "Wait", it often responds: "let me re-check...actually, the answer is 3." This 
    self-correction mechanism is <i>latent</i> in the base model, not explicitly trained.
    """
    story.append(Paragraph(s1_key, styles['CustomBody']))

    s1_results = """
    <b>Results:</b> After supervised fine-tuning Qwen2.5-32B-Instruct on s1K (26 minutes on 
    16 H100s), the resulting s1-32B model exceeded o1-preview by up to 27% on competition 
    math (MATH, AIME24). Budget forcing further improved AIME24 from 50% to 57%.
    """
    story.append(Paragraph(s1_results, styles['CustomBody']))

    # --- Paper 2: LIMO ---
    story.append(Spacer(1, 0.15*inch))
    story.append(
        Paragraph("2.2 LIMO: Less is More for Reasoning", styles['SubHeading']))
    story.append(Paragraph(
        "<i>Ye et al., GAIR-NLP, February 2025 | arXiv:2502.03387 | COLM 2025</i>",
        styles['Caption']
    ))

    limo_problem = """
    <b>Problem:</b> Conventional wisdom held that complex mathematical reasoning required 
    massive training datasets (>100,000 examples). This created substantial computational 
    costs and data collection burdens.
    """
    story.append(Paragraph(limo_problem, styles['CustomBody']))

    limo_solution = """
    <b>Solution:</b> LIMO demonstrates that with only <b>817 carefully curated training samples</b>, 
    a model can achieve competition-level mathematical reasoning. The key is quality over quantity:
    """
    story.append(Paragraph(limo_solution, styles['CustomBody']))

    limo_bullets = [
        "<b>Cognitive Templates:</b> High-quality reasoning chains that serve as templates for how to utilize existing knowledge.",
        "<b>Difficulty-Based Selection:</b> Problems where DeepSeek-R1 succeeded only 1-3 out of 32 attempts were retained.",
        "<b>Structural Quality:</b> Solutions with clear organization, progressive depth, and self-verification steps."
    ]
    for bullet in limo_bullets:
        story.append(Paragraph(f"• {bullet}", styles['BulletText']))

    limo_hypothesis = """
    <b>LIMO Hypothesis:</b> "In foundation models where domain knowledge has been comprehensively 
    encoded during pre-training, sophisticated reasoning can emerge through minimal but 
    strategically designed demonstrations of cognitive processes."
    """
    story.append(Paragraph(limo_hypothesis, styles['Abstract']))

    limo_results = """
    <b>Results:</b> Using Qwen2.5-32B-Instruct as base, LIMO achieved 63.3% on AIME24 and 
    95.6% on MATH500—surpassing previous SFT models (6.5% and 59.2%) while using only 1% 
    of the training data. Crucially, LIMO showed 45.8% absolute improvement on out-of-distribution 
    benchmarks, demonstrating genuine generalization rather than memorization.
    """
    story.append(Paragraph(limo_results, styles['CustomBody']))

    # --- Paper 3: Coconut ---
    story.append(Spacer(1, 0.15*inch))
    story.append(
        Paragraph("2.3 Coconut: Chain of Continuous Thought", styles['SubHeading']))
    story.append(Paragraph(
        "<i>Hao et al., Meta FAIR, December 2024 | arXiv:2412.06769 | ICLR 2025</i>",
        styles['Caption']
    ))

    coconut_problem = """
    <b>Problem:</b> Traditional Chain-of-Thought (CoT) reasoning is constrained to language 
    space, where most tokens ensure textual coherence rather than contributing to reasoning. 
    This mirrors findings that human reasoning doesn't heavily engage language brain areas.
    """
    story.append(Paragraph(coconut_problem, styles['CustomBody']))

    coconut_solution = """
    <b>Solution:</b> Coconut (Chain of Continuous Thought) allows LLMs to reason in an 
    <b>unrestricted latent space</b> instead of generating language tokens:
    """
    story.append(Paragraph(coconut_solution, styles['CustomBody']))

    coconut_bullets = [
        "<b>Continuous Thought:</b> The model's last hidden state becomes a 'continuous thought' fed directly as the next input embedding—no decoding to tokens.",
        "<b>Multi-Stage Curriculum:</b> Training progressively replaces language reasoning steps with latent thoughts.",
        "<b>Emergent BFS:</b> Continuous thoughts can encode multiple alternative next steps, enabling breadth-first search rather than committing to a single path."
    ]
    for bullet in coconut_bullets:
        story.append(Paragraph(f"• {bullet}", styles['BulletText']))

    coconut_results = """
    <b>Results:</b> On logical reasoning tasks (ProntoQA, ProsQA) requiring substantial 
    backtracking, Coconut outperformed standard CoT while generating significantly fewer 
    tokens. On GSM8k math problems, performance increased with more continuous thoughts 
    per step (c=1 to c=2), demonstrating scalable latent reasoning.
    """
    story.append(Paragraph(coconut_results, styles['CustomBody']))

    # =========================================================================
    # SECTION 3: COMPARATIVE ANALYSIS
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("3. Comparative Analysis",
                 styles['SectionHeading']))

    # Comparison table
    table_data = [
        ['Aspect', 's1', 'LIMO', 'Coconut'],
        ['Core Innovation', 'Budget forcing\n(test-time)',
         'Cognitive templates\n(817 samples)', 'Latent reasoning\n(no language)'],
        ['Training Cost', '26 min / 16 H100s',
            'Standard SFT', 'Multi-stage\ncurriculum'],
        ['Key Metric', 'AIME24: 57%\n(+27% vs o1-preview)',
         'AIME24: 63.3%\n(1% of data)', 'Fewer tokens,\nhigher accuracy'],
        ['Base Model', 'Qwen2.5-32B', 'Qwen2.5-32B',
            'GPT-2 (proof\nof concept)'],
        ['Open Source', 'Full (MIT)', 'Full (MIT)', 'Full (MIT)'],
    ]

    table = Table(table_data, colWidths=[
                  1.3*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a2e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
         [colors.white, colors.HexColor('#f8f9fa')]),
    ]))
    story.append(table)
    story.append(Paragraph(
        "Table 1: Comparative overview of the three papers", styles['Caption']))

    # Complementary approaches
    story.append(
        Paragraph("Complementary Approaches to the Same Goal", styles['SubHeading']))

    comp_text = """
    These papers attack reasoning enhancement from three orthogonal angles, yet converge 
    on the same insight:
    """
    story.append(Paragraph(comp_text, styles['CustomBody']))

    comp_bullets = [
        "<b>s1 (Test-Time):</b> Reasoning capabilities are latent in the model; we just need to give it permission to 'think longer' via budget forcing.",
        "<b>LIMO (Training Data):</b> Reasoning capabilities are latent in the model; we just need a few high-quality cognitive templates to activate them.",
        "<b>Coconut (Architecture):</b> Reasoning capabilities are latent in the model; we just need to free them from the constraints of language space."
    ]
    for bullet in comp_bullets:
        story.append(Paragraph(f"• {bullet}", styles['BulletText']))

    convergence = """
    <b>Convergence:</b> All three papers demonstrate that foundation models have internalized 
    substantial reasoning capabilities during pre-training. The challenge is not to <i>teach</i> 
    reasoning but to <i>elicit</i> it through minimal, precise interventions.
    """
    story.append(Paragraph(convergence, styles['CustomBody']))

    # =========================================================================
    # SECTION 4: INSIGHTS & REFLECTION
    # =========================================================================
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("4. Insights and Reflection",
                 styles['SectionHeading']))

    story.append(Paragraph("Key Takeaways", styles['SubHeading']))

    takeaway1 = """
    <b>1. The Superficial Alignment Hypothesis Extends to Reasoning:</b> Just as LIMA showed 
    that alignment requires only ~1,000 examples, these papers show that reasoning elicitation 
    may require similarly minimal data. The knowledge exists; the question is how to access it.
    """
    story.append(Paragraph(takeaway1, styles['CustomBody']))

    takeaway2 = """
    <b>2. Quality Over Quantity at Every Level:</b> s1 uses 1,000 questions, LIMO uses 817, 
    and Coconut shows that latent thoughts can replace verbose language chains. The pattern 
    is consistent: careful curation beats brute-force scaling.
    """
    story.append(Paragraph(takeaway2, styles['CustomBody']))

    takeaway3 = """
    <b>3. Emergent Behaviors Without Explicit Training:</b> s1's 'Wait' token triggers 
    self-correction that was never explicitly trained. Coconut's continuous thoughts enable 
    BFS-like search without being taught to do so. These emergent capabilities suggest that 
    reasoning architectures may be more flexible than previously believed.
    """
    story.append(Paragraph(takeaway3, styles['CustomBody']))

    story.append(
        Paragraph("Limitations and Open Questions", styles['SubHeading']))

    limit_bullets = [
        "All three papers focus primarily on mathematical and logical reasoning with verifiable answers. Extension to open-ended reasoning remains challenging.",
        "Base model quality matters enormously—LIMO and s1 both rely on Qwen2.5-32B-Instruct, while Coconut's GPT-2 experiments may not scale to harder tasks.",
        "The 'elicitation vs. teaching' dichotomy may be false—larger-scale interventions might still unlock additional capabilities.",
        "Latent reasoning (Coconut) sacrifices interpretability, which may limit adoption in high-stakes applications."
    ]
    for bullet in limit_bullets:
        story.append(Paragraph(f"• {bullet}", styles['BulletText']))

    story.append(Paragraph("Future Directions", styles['SubHeading']))

    future_text = """
    These papers open exciting research directions: Can budget forcing and latent reasoning 
    be combined? Can LIMO-style cognitive templates be generated automatically? How do 
    these techniques interact with reinforcement learning approaches like DeepSeek-R1's GRPO?
    """
    story.append(Paragraph(future_text, styles['CustomBody']))

    # =========================================================================
    # SECTION 5: CONCLUSION
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("5. Conclusion", styles['SectionHeading']))

    conclusion = """
    The three papers analyzed in this meta-analysis—s1, LIMO, and Coconut—represent a 
    crystallization of a new paradigm in LLM reasoning research. They collectively demonstrate 
    that the path to better reasoning may not lie in scaling up training data, model parameters, 
    or reinforcement learning signals, but in understanding and exploiting the latent capabilities 
    that modern foundation models already possess.
    """
    story.append(Paragraph(conclusion, styles['CustomBody']))

    conclusion2 = """
    The implications are profound: if reasoning can be elicited with 817 training examples, 
    a single 'Wait' token, or by bypassing language entirely, then our current understanding 
    of what LLMs 'know' versus what they can 'do' requires revision. These are not just 
    incremental improvements—they are hints at a deeper truth about the nature of learned 
    representations in large neural networks.
    """
    story.append(Paragraph(conclusion2, styles['CustomBody']))

    final_thought = """
    "Less is more" is not merely an optimization strategy—it may be the key to unlocking 
    the full potential of foundation models.
    """
    story.append(Paragraph(final_thought, styles['Abstract']))

    # References
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("References", styles['SubHeading']))

    refs = [
        "[1] Muennighoff, N., et al. (2025). s1: Simple test-time scaling. arXiv:2501.19393. EMNLP 2025.",
        "[2] Ye, Y., et al. (2025). LIMO: Less is More for Reasoning. arXiv:2502.03387. COLM 2025.",
        "[3] Hao, S., et al. (2024). Training Large Language Models to Reason in a Continuous Latent Space. arXiv:2412.06769. ICLR 2025.",
    ]
    for ref in refs:
        story.append(Paragraph(ref, ParagraphStyle(
            'Reference',
            parent=styles['Normal'],
            fontSize=9,
            leftIndent=20,
            firstLineIndent=-20,
            spaceBefore=3,
            spaceAfter=3
        )))

    # Build the PDF
    doc.build(story)
    print("PDF generated successfully: /mnt/user-data/outputs/meta_analysis_llms.pdf")


if __name__ == "__main__":
    build_document()
