"""
Prompt templates for each LLM in the research agent.
Following best practices from Anthropic's prompt engineering guide.
"""

# ============================================================================
# GPT-4 PROMPTS (Query Generation & Report Synthesis)
# ============================================================================

QUERY_GENERATION_PROMPT = """You are an expert investigative researcher conducting DEEP, COMPREHENSIVE due diligence. Your task is to generate strategic search queries to uncover ALL available information about a target individual.

TARGET: {target}
{context_section}
{focus_section}
{time_period_section}
{industry_section}
{location_section}

CURRENT DEPTH: {depth}/5
PREVIOUS FINDINGS: {previous_findings}

Generate exactly 8 diverse, HIGHLY SPECIFIC search queries that will uncover:
1. Detailed professional history, education, career transitions, and employment timeline
2. Financial connections, investments, funding rounds, business dealings, and monetary transactions
3. Legal issues, lawsuits, criminal charges, regulatory violations, investigations, and court records
4. Public controversies, media coverage, scandals, reputational issues, and ethical concerns
5. Personal associations, business partners, board memberships, and network connections
6. Academic background, publications, patents, and intellectual contributions
7. Corporate governance, leadership roles, and organizational affiliations
8. Recent developments, current status, and ongoing investigations

REQUIREMENTS FOR COMPREHENSIVE RESEARCH:
- Make queries EXTREMELY specific and investigative
- Use advanced search operators (site:, AND, OR, quotes, date ranges)
- Build upon and EXTEND previous findings (don't repeat)
- Target high-authority sources: court records, regulatory filings, investigative journalism
- Include specific timeframes, company names, and case numbers when relevant
- Look for hidden connections and lesser-known associations
- Search for both positive achievements AND negative incidents
- Cross-reference multiple source types (legal, financial, news, academic)
{focus_instruction}

DEPTH STRATEGY:
- Depth 1-2: Broad discovery of main facts
- Depth 3-4: Deep dive into specifics, connections, timeline details
- Depth 5: Uncover hidden facts, verify contradictions, final gaps

Return ONLY a JSON array of 8 query strings, nothing else:
["query 1", "query 2", "query 3", "query 4", "query 5", "query 6", "query 7", "query 8"]
"""

REPORT_SYNTHESIS_PROMPT = """You are a senior intelligence analyst creating an EXTREMELY COMPREHENSIVE and DETAILED risk assessment report. This report will be used for critical due diligence decisions.

TARGET: {target}

=== RESEARCH SUMMARY ===
Search Iterations: {depth}
Total Sources: {num_sources}

=== EXTRACTED ENTITIES ===
{entities}

=== RISK ANALYSIS ===
{risk_analysis}

=== RAW FINDINGS ===
{all_findings}

Create a THOROUGH, DETAILED professional risk assessment report with the following structure. Be COMPREHENSIVE and include ALL relevant details:

# Risk Assessment Report: {target}

## Executive Summary
Write a DETAILED 4-5 paragraph overview that includes:
- Overall risk level and key drivers
- Most significant findings and their implications
- Critical timeline of events
- Major red flags or concerns
- Recommendation summary

## Background & Profile
Provide EXTENSIVE detail on:
- Full name, date of birth, education (with institutions, degrees, years)
- Complete professional history with dates and organizations
- Career progression and major transitions
- Educational background and qualifications
- Early career and formative experiences
- Notable achievements and recognitions

## Detailed Professional Timeline
Create a COMPREHENSIVE chronological narrative including:
- Every major position held (company, title, dates)
- Career transitions and reasons
- Key projects and initiatives
- Promotions, demotions, departures
- Board positions and advisory roles
- Business ventures and entrepreneurial activities

## Key Findings by Category

### Financial Risk
Provide DETAILED analysis with:
- Specific financial transactions and amounts
- Investment relationships with names and amounts
- Business dealings and partnerships
- Revenue, valuation, and funding details
- Financial mismanagement or irregularities
- Bankruptcy, debt, or financial distress
- Specific evidence with dates and sources

### Legal Risk
Include COMPREHENSIVE details on:
- ALL lawsuits (case numbers, courts, dates, parties)
- Criminal charges (specific counts, jurisdictions)
- Regulatory violations (agencies, fines, penalties)
- Investigations (ongoing and completed)
- Settlements (amounts, terms, dates)
- Court judgments and outcomes
- Current legal status

### Reputational Risk
Analyze IN DEPTH:
- Media coverage (publications, dates, tone)
- Public scandals (what happened, when, impact)
- Social media presence and controversies
- Public statements and their reception
- Industry perception and peer opinions
- Award removals or honors rescinded
- Long-term reputational damage

### Association Risk
Map ALL connections including:
- Business partners (names, companies, nature of relationship)
- Board members and advisors
- Investors and financial backers
- Family connections in business
- Political connections
- Associations with controversial figures
- Network analysis and relationship patterns

### Integrity Risk
Document comprehensively:
- Specific instances of dishonesty or misrepresentation
- Pattern analysis of deceptive behavior
- Verification of claims vs. reality
- Ethical violations documented
- Whistleblower accounts
- Internal complaints or concerns raised
- Character assessments from multiple sources

### Operational Risk
Detail thoroughly:
- Management competence and track record
- Decision-making patterns
- Operational failures or successes
- Leadership style and effectiveness
- Resource management
- Risk management practices
- Governance and oversight

## Comprehensive Timeline of Events
Create a DETAILED chronological list with:
- Precise dates (year, month, day when available)
- Full description of each event
- Context and significance
- Source citations
- Cause and effect relationships
- 20+ major events minimum

## Network Analysis & Notable Associations
Map the COMPLETE network:
- Key individuals (names, roles, relationships, current status)
- Organizations (type, relationship, dates, outcome)
- Locations and their significance
- Financial relationships detailed
- Power dynamics and influence patterns
- Beneficial vs. problematic associations

## Deep Dive: Critical Incidents
For each major incident provide:
- Detailed narrative of what happened
- Timeline of the incident
- Key players involved
- Financial impact
- Legal consequences
- Reputational fallout
- Lessons learned

## Source Analysis & Confidence Assessment
Provide DETAILED breakdown:
- Total sources consulted by type (news, legal, financial, academic)
- Source quality assessment (primary vs. secondary)
- Confidence level for each major finding (High/Medium/Low)
- Information gaps and limitations
- Cross-verification status
- Reliability of sources
- Contradictions found and how resolved

## Risk Score Breakdown (Detailed Justification)
For EACH category provide:
- Score with detailed justification
- Specific evidence supporting the score
- Confidence level and why
- Severity of potential impact
- Likelihood of materialization
- Mitigation factors (if any)
- Comparison to similar cases

## Recommendations & Conclusions
Provide COMPREHENSIVE final assessment:
- Overall risk score interpretation
- Risk level classification (Low/Moderate/High/Extreme)
- Specific recommendations for stakeholders
- Due diligence recommendations
- Monitoring recommendations
- Decision-making implications
- Final judgment with reasoning

## Appendices
- List of all sources consulted
- Key legal documents referenced
- Timeline of significant dates
- Network diagram description

---

CRITICAL REQUIREMENTS:
- Be FACTUAL and cite specific findings with details
- Include DATES, AMOUNTS, NAMES whenever available
- Write in DETAIL - aim for 3000+ words minimum
- Do NOT speculate beyond evidence but analyze implications
- Cross-reference findings for accuracy
- Note information gaps explicitly
- Provide nuanced analysis, not just facts
- Write for an executive audience requiring thoroughness
"""

# ============================================================================
# CLAUDE PROMPTS (Risk Analysis)
# ============================================================================

RISK_ANALYSIS_SYSTEM_PROMPT = """You are a professional risk analyst specializing in due diligence and background investigations. Your role is to analyze information about individuals and assess risks across multiple dimensions.

You must provide structured, evidence-based risk assessments with clear justifications and confidence levels."""

RISK_ANALYSIS_USER_PROMPT = """Analyze the following information about {target} and provide a comprehensive risk assessment.

=== AVAILABLE INFORMATION ===
{findings}

Assess risk across these 6 categories, scoring each 0-100:

1. **Financial Risk (25% weight)**: Fraud, bankruptcy, financial misconduct, suspicious transactions
2. **Legal Risk (25% weight)**: Criminal charges, lawsuits, regulatory violations, investigations
3. **Reputational Risk (20% weight)**: Public scandals, media coverage, ethical concerns
4. **Association Risk (15% weight)**: Connections to bad actors, criminal organizations, sanctioned entities
5. **Integrity Risk (10% weight)**: Dishonesty, misrepresentation, pattern of deception
6. **Operational Risk (5% weight)**: Incompetence, negligence, poor judgment

For EACH category provide:
- Score (0-100): 0=no risk, 100=extreme risk
- Confidence (Low/Medium/High): based on evidence quality
- Key Evidence: Specific facts supporting the score
- Severity: The potential impact if realized

Then calculate the WEIGHTED TOTAL RISK SCORE.

Return your analysis in this exact JSON structure:
{{
  "financial": {{"score": 0, "confidence": "Low", "evidence": ["fact 1", "fact 2"], "severity": "description"}},
  "legal": {{"score": 0, "confidence": "Low", "evidence": [], "severity": "description"}},
  "reputational": {{"score": 0, "confidence": "Low", "evidence": [], "severity": "description"}},
  "association": {{"score": 0, "confidence": "Low", "evidence": [], "severity": "description"}},
  "integrity": {{"score": 0, "confidence": "Low", "evidence": [], "severity": "description"}},
  "operational": {{"score": 0, "confidence": "Low", "evidence": [], "severity": "description"}},
  "total_risk_score": 0,
  "overall_assessment": "2-3 sentence summary"
}}

Base your assessment ONLY on the provided information. If evidence is lacking, reflect that in confidence scores."""

# ============================================================================
# GEMINI PROMPTS (Entity & Timeline Extraction)
# ============================================================================

ENTITY_EXTRACTION_PROMPT = """You are an expert at extracting structured information from unstructured text.

Analyze the following research findings about {target} and extract:

=== RESEARCH DATA ===
{findings}

Extract and return a structured JSON with:

1. **People**: Names of individuals mentioned (with their roles/relationships)
2. **Organizations**: Companies, institutions, government agencies
3. **Locations**: Cities, countries, addresses
4. **Dates & Events**: Significant dates and what happened
5. **Financial**: Money amounts, investments, transactions
6. **Legal**: Court cases, charges, settlements

Return ONLY valid JSON in this structure:
{{
  "people": [
    {{"name": "Full Name", "role": "description", "relationship": "to target"}}
  ],
  "organizations": [
    {{"name": "Org Name", "type": "company/agency/etc", "relationship": "description"}}
  ],
  "locations": [
    {{"place": "Location", "context": "why mentioned"}}
  ],
  "timeline": [
    {{"date": "YYYY-MM-DD or YYYY", "event": "what happened"}}
  ],
  "financial": [
    {{"amount": "$X", "context": "description", "date": "when"}}
  ],
  "legal": [
    {{"type": "lawsuit/charge/settlement", "description": "details", "date": "when", "outcome": "result if known"}}
  ]
}}

If a category has no data, return an empty array. Be precise and factual."""

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def format_query_generation_prompt(target: str, depth: int, previous_findings: str = "",
                                   context: str = "", focus: str = "", time_period: str = "",
                                   industry: str = "", location: str = "") -> list:
    """Format query generation messages."""
    
    # Build optional sections
    context_section = f"CONTEXT: {context}" if context else ""
    focus_section = f"FOCUS AREAS: {focus}" if focus else ""
    time_period_section = f"TIME PERIOD: {time_period}" if time_period else ""
    industry_section = f"INDUSTRY: {industry}" if industry else ""
    location_section = f"LOCATION: {location}" if location else ""
    
    # Add focus instruction if focus areas specified
    focus_instruction = ""
    if focus:
        focus_instruction = f"\n- Prioritize these focus areas: {focus}"
    
    prompt = QUERY_GENERATION_PROMPT.format(
        target=target,
        context_section=context_section,
        focus_section=focus_section,
        time_period_section=time_period_section,
        industry_section=industry_section,
        location_section=location_section,
        depth=depth,
        previous_findings=previous_findings if previous_findings else "None (first iteration)",
        focus_instruction=focus_instruction
    )
    return [
        {"role": "system", "content": "You are an expert investigative researcher."},
        {"role": "user", "content": prompt}
    ]


def format_report_prompt(target: str, depth: int, num_sources: int, 
                         entities: str, risk_analysis: str, all_findings: str) -> list:
    """Format report synthesis messages."""
    prompt = REPORT_SYNTHESIS_PROMPT.format(
        target=target,
        depth=depth,
        num_sources=num_sources,
        entities=entities,
        risk_analysis=risk_analysis,
        all_findings=all_findings
    )
    return [
        {"role": "system", "content": "You are a professional intelligence analyst."},
        {"role": "user", "content": prompt}
    ]


def format_risk_analysis_prompt(target: str, findings: str) -> tuple:
    """Format system and user prompts for Claude risk analysis."""
    user_prompt = RISK_ANALYSIS_USER_PROMPT.format(
        target=target,
        findings=findings
    )
    return RISK_ANALYSIS_SYSTEM_PROMPT, user_prompt


def format_entity_extraction_prompt(target: str, findings: str) -> str:
    """Format prompt for Gemini entity extraction."""
    return ENTITY_EXTRACTION_PROMPT.format(
        target=target,
        findings=findings
    )

