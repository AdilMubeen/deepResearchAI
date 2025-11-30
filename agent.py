"""LangGraph-based research workflow with iterative deepening."""
import json
from typing import TypedDict
from langgraph.graph import StateGraph, END
from models import models
from tools import batch_search, format_search_results
from prompts import (
    format_query_generation_prompt, format_risk_analysis_prompt,
    format_entity_extraction_prompt, format_report_prompt
)


class ResearchState(TypedDict):
    """State object passed between workflow nodes."""
    target: str
    context: str
    focus: str
    time_period: str
    industry: str
    location: str
    depth: int
    max_depth: int
    all_findings: str
    entities: str
    risk_analysis: str
    final_report: str
    num_sources: int


def _clean_json_response(response):
    """Strip markdown code blocks from LLM JSON responses."""
    response = response.strip()
    if response.startswith("```json"):
        response = response[7:]
    if response.startswith("```"):
        response = response[3:]
    if response.endswith("```"):
        response = response[:-3]
    return response.strip()


def search_node(state: ResearchState) -> ResearchState:
    """Generate queries via GPT-4, execute via Perplexity."""
    state['depth'] = state.get('depth', 0) + 1
    print(f"\n{'='*60}")
    print(f"SEARCH - Depth {state['depth']}/{state['max_depth']}")
    print(f"{'='*60}")
    
    messages = format_query_generation_prompt(
        target=state['target'], depth=state['depth'],
        previous_findings=state.get('all_findings', ''),
        context=state.get('context', ''), focus=state.get('focus', ''),
        time_period=state.get('time_period', ''), industry=state.get('industry', ''),
        location=state.get('location', '')
    )
    
    print("Generating queries...")
    query_response = models.gpt4_call(messages, temperature=0.7, max_tokens=1000)
    
    if not query_response:
        return state
    
    try:
        queries = json.loads(_clean_json_response(query_response))
        print(f"Generated {len(queries)} queries")
    except json.JSONDecodeError:
        queries = [
            f"{state['target']} biography career timeline",
            f"{state['target']} controversy scandal investigation",
            f"{state['target']} lawsuit legal criminal charges",
            f"{state['target']} company business financial",
            f"{state['target']} news recent developments",
            f"{state['target']} education background",
            f"{state['target']} board members associates",
            f"{state['target']} regulatory violations SEC FTC"
        ]
    
    print("Executing searches...")
    search_results = batch_search(queries, max_results_per_query=3)
    
    formatted_results = []
    for query, results in search_results.items():
        formatted_results.append(f"\n[Query: {query}]")
        formatted_results.append(format_search_results(results))
    
    state['all_findings'] = state.get('all_findings', '') + "\n\n" + "\n".join(formatted_results)
    state['num_sources'] = state.get('num_sources', 0) + sum(len(r) for r in search_results.values())
    print(f"Total sources: {state['num_sources']}")
    
    return state


def extract_node(state: ResearchState) -> ResearchState:
    """Extract entities and timeline via Gemini."""
    print(f"\n{'='*60}")
    print("EXTRACT - Entity & Timeline Extraction")
    print(f"{'='*60}")
    
    prompt = format_entity_extraction_prompt(
        target=state['target'], findings=state['all_findings'][-8000:]
    )
    
    print("Extracting entities...")
    entity_response = models.gemini_call(prompt, temperature=0.3, max_tokens=2000)
    
    if not entity_response:
        state['entities'] = json.dumps({"error": "Extraction failed"})
        return state
    
    try:
        entities = json.loads(_clean_json_response(entity_response))
        state['entities'] = json.dumps(entities, indent=2)
        print(f"Extracted: {len(entities.get('people', []))} people, "
              f"{len(entities.get('organizations', []))} orgs, "
              f"{len(entities.get('timeline', []))} events")
    except json.JSONDecodeError:
        state['entities'] = entity_response
    
    return state


def risk_node(state: ResearchState) -> ResearchState:
    """Analyze risks across 6 categories via Claude."""
    print(f"\n{'='*60}")
    print("RISK - Multi-Category Analysis")
    print(f"{'='*60}")
    
    system_prompt, user_prompt = format_risk_analysis_prompt(
        target=state['target'], findings=state['all_findings'][-10000:]
    )
    
    print("Analyzing risks...")
    risk_response = models.claude_call(system_prompt, user_prompt, temperature=0.3, max_tokens=3000)
    
    if not risk_response:
        state['risk_analysis'] = json.dumps({"error": "Analysis failed"})
        return state
    
    try:
        risk_data = json.loads(_clean_json_response(risk_response))
        state['risk_analysis'] = json.dumps(risk_data, indent=2)
        print(f"Total Risk Score: {risk_data.get('total_risk_score', 0)}/100")
    except json.JSONDecodeError:
        state['risk_analysis'] = risk_response
    
    return state


def report_node(state: ResearchState) -> ResearchState:
    """Synthesize final report via GPT-4."""
    print(f"\n{'='*60}")
    print("REPORT - Synthesizing Final Report")
    print(f"{'='*60}")
    
    messages = format_report_prompt(
        target=state['target'], depth=state['depth'], num_sources=state['num_sources'],
        entities=state.get('entities', 'N/A'), risk_analysis=state.get('risk_analysis', 'N/A'),
        all_findings=state['all_findings'][-25000:]
    )
    
    print("Generating report...")
    report = models.gpt4_call(messages, temperature=0.6, max_tokens=8000)
    
    state['final_report'] = report if report else "Report generation failed"
    print(f"Report generated ({len(state['final_report'])} chars)")
    
    return state


def should_continue(state: ResearchState) -> str:
    """Decide whether to loop or proceed to final report."""
    if state.get('depth', 0) < state.get('max_depth', 3):
        print(f"\nContinuing to depth {state['depth'] + 1}...")
        return "continue"
    print("\nProceeding to final report...")
    return "report"


def create_research_graph():
    """Build the LangGraph workflow: search → extract → risk → (loop or report)."""
    workflow = StateGraph(ResearchState)
    workflow.add_node("search", search_node)
    workflow.add_node("extract", extract_node)
    workflow.add_node("risk", risk_node)
    workflow.add_node("report", report_node)
    
    workflow.set_entry_point("search")
    workflow.add_edge("search", "extract")
    workflow.add_edge("extract", "risk")
    workflow.add_conditional_edges("risk", should_continue, {"continue": "search", "report": "report"})
    workflow.add_edge("report", END)
    
    return workflow.compile()


def run_research(target: str, max_depth: int = 3, context: str = '', focus: str = '',
                 time_period: str = '', industry: str = '', location: str = '') -> dict:
    """Execute the full research workflow and return final state."""
    print(f"\n{'#'*60}")
    print(f"DEEP RESEARCH AGENT")
    print(f"Target: {target}")
    if context:
        print(f"Context: {context}")
    print(f"Max Depth: {max_depth}")
    print(f"{'#'*60}\n")
    
    initial_state = {
        "target": target, "context": context, "focus": focus, "time_period": time_period,
        "industry": industry, "location": location, "depth": 0, "max_depth": max_depth,
        "all_findings": "", "entities": "", "risk_analysis": "", "final_report": "", "num_sources": 0
    }
    
    try:
        graph = create_research_graph()
        final_state = graph.invoke(initial_state, {"recursion_limit": 100})
        
        print(f"\n{'#'*60}")
        print("RESEARCH COMPLETE")
        print(f"{'#'*60}\n")
        
        return final_state
    except Exception as e:
        print(f"\n ERROR: {e}")
        import traceback
        traceback.print_exc()
        return initial_state
