# Problem Framing: Indian DPDP Statutory Research Assistant

---

## 1. The Real-World Problem

With the passage of the **Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023)** and the forthcoming **DPDP Rules, 2025**, Indian enterprises, compliance officers, and developers face a substantial regulatory compliance burden:
- **Severe Financial Liabilities:** Failure to take reasonable security safeguards under Section 8(5) risks statutory penalties up to **₹250 crore**; non-reporting of data breaches risks penalties up to **₹200 crore**.
- **Staggered Regulatory Hierarchy:** Compliance requirements cannot be understood from the Act alone. Provisions operate across a strict statutory hierarchy:
  1. *Primary Legislation (Act 2023):* Core obligations and rights.
  2. *Secondary Legislation (Rules 2025):* Operational specifics (consent formats, notice languages, audit criteria).
  3. *Corrigenda & MeitY Timelines:* Staggered enforcement dates ("what is law" vs. "what has taken effect").
- **The LLM Hallucination Trap:** Generic LLM chatbots frequently conflate GDPR principles (e.g., "Legitimate Interests") with DPDP constructs ("Certain Legitimate Uses"), invent non-existent statutory section numbers, or quote provisions that have not yet been notified into force. In regulatory compliance, an ungrounded answer is worse than no answer.

---

## 2. Why Existing Solutions Fail

1. **Fixed-Token Naive Chunking:** Arbitrary chunking (e.g. 500 tokens with 50-token overlap) cuts across legal sections, bisecting statutory definitions, caveats, and sub-clauses `(1)(a)(i)`. This causes retrieval to return incomplete clauses stripped of their statutory conditions.
2. **Ungrounded Conversational Output:** Standard RAG frameworks return freeform text summaries without linking specific claims to deterministic statutory anchors. Reviewers cannot audit which section authorized the statement.
3. **Absence of Abstention:** Typical RAG pipelines force the LLM to synthesize an answer even when the retrieved context lacks sufficient evidence, resulting in plausible-sounding hallucinations that fail legal scrutiny.

---

## 3. Measurable Success Targets (Our Constraints)

To meet production-grade engineering standards, this system is governed by strict non-functional constraints:

* **Strict Citation Grounding:** 100% of generated factual statements must trace to a verified citation in the format `[Document Name, Section/Rule Number]`.
* **Zero-Hallucination & Forced Abstention:** When queried on out-of-scope regulations (e.g. GDPR, HIPAA, or unnotified provisions), the system must explicitly decline to answer rather than fabricate answers.
* **Latency:** End-to-end retrieval and grounded answer synthesis must complete in **$< 1.5$ seconds**.
* **Unit Economics:** Cost per query capped at **$< \$0.005$** via local preprocessing, boundary chunking, and deterministic citation filtering before model synthesis.
* **Zero-Key Local Reproducibility:** The entire indexing and retrieval pipeline must execute with zero cloud API keys (`MOCK_AI=true`), enabling instant local verification and automated CI testing.
