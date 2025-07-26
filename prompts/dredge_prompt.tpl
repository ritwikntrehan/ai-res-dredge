### SYSTEM
You are pulling resume‑ready bullets from documents from new healthcare grads.

### USER
From the **Candidate Text** and **Job Posting** below, extract ONLY facts that will strengthen
the resume for THIS job.

Return exactly this JSON

```json
{
  "facts": [
    {
      "bullet": "<bullet text already phrased for resume>",
      "tags": ["<categorizing word>"],
      "source": "<document and line>"
    }
  ]
}
Candidate Text:
<<<{{candidate_text}}>>>

Job Posting:
<<<{{job_posting}}>>>
