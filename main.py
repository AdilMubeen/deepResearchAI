"""Command-line interface for the research agent."""
import argparse
import json
from agent import run_research
from config import Config


def display_summary(state):
    """Print research results summary."""
    print(f"\n{'='*50}")
    print("RESEARCH SUMMARY")
    print(f"{'='*50}")
    print(f"\nTarget: {state.get('target')}")
    print(f"Iterations: {state.get('depth')}")
    print(f"Sources: {state.get('num_sources')}")
    
    try:
        risk_data = json.loads(state.get('risk_analysis', '{}'))
        print(f"\nOverall Risk Score: {risk_data.get('total_risk_score', 'N/A')}/100")
        print("\nRisk Breakdown:")
        for cat in ['financial', 'legal', 'reputational', 'association', 'integrity', 'operational']:
            if cat in risk_data:
                print(f"  {cat.capitalize()}: {risk_data[cat].get('score', 'N/A')}/100")
    except:
        pass
    
    try:
        entities = json.loads(state.get('entities', '{}'))
        print(f"\nEntities: {len(entities.get('people', []))} people, "
              f"{len(entities.get('organizations', []))} orgs, "
              f"{len(entities.get('timeline', []))} events")
    except:
        pass
    
    print(f"\n{'='*50}\n")


def main():
    """Parse arguments and run research."""
    parser = argparse.ArgumentParser(description="Deep Research AI Agent")
    parser.add_argument('--target', required=True, help='Person to research')
    parser.add_argument('--context', default='', help='Additional context')
    parser.add_argument('--focus', default='', help='Focus areas')
    parser.add_argument('--time-period', default='', help='Time period')
    parser.add_argument('--industry', default='', help='Industry')
    parser.add_argument('--location', default='', help='Location')
    parser.add_argument('--depth', type=int, default=5, help='Max depth (default: 5)')
    
    args = parser.parse_args()
    
    print(f"\n{'#'*50}")
    print("DEEP RESEARCH AI AGENT")
    print(f"{'#'*50}")
    print(f"\nTarget: {args.target}")
    print(f"Max Depth: {args.depth}")
    
    try:
        input("\nPress ENTER to start...")
    except KeyboardInterrupt:
        print("\nCancelled")
        return
    
    try:
        state = run_research(
            target=args.target, max_depth=args.depth, context=args.context,
            focus=args.focus, time_period=args.time_period,
            industry=args.industry, location=args.location
        )
        display_summary(state)
        print("Done! Run via web: http://localhost:5001\n")
    except KeyboardInterrupt:
        print("\nInterrupted")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()
