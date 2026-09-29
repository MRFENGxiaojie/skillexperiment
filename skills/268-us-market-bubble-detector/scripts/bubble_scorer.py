#!/usr/bin/env python3
"""
Bubble-O-Meter: Script for multi-faceted evaluation of U.S. stock market bubble risk

DEPRECATED (v1.x): this script implements the old 8-indicator Bubble-O-Meter on
a 0-16 point scale. The current framework (SKILL.md v2.1) scores 6 quantitative
indicators (Phase 2, 0-12) plus 3 qualitative adjustments (Phase 3, 0 to +3),
maximum 15 points, with a 5-phase judgment including "Elevated Risk" (8-9).
Use this script only for historical v1.x estimates; for v2.1 evaluations follow
SKILL.md.

For reference, the v2.1 phase mapping is applied to the total score below:
- 0-4: Normal
- 5-7: Caution
- 8-9: Elevated Risk
- 10-12: Euphoria
- 13-16: Critical

Usage:
    python bubble_scorer.py --manual
    python bubble_scorer.py --scores '{"mass_penetration":2,"media_saturation":1}'
    python bubble_scorer.py --scores '{"mass_penetration":2}' --output json
"""

import argparse
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple


class BubbleScorer:
    """Bubble Scoring System"""
    
    def __init__(self):
        self.indicators = {
            "mass_penetration": {
                "name": "Mass Penetration",
                "weight": 2,
                "description": "Recommendations/mentions from non-investor segments"
            },
            "media_saturation": {
                "name": "Media Saturation",
                "weight": 2,
                "description": "Surge in search, social media, and media exposure"
            },
            "new_accounts": {
                "name": "New Entrants",
                "weight": 2,
                "description": "Acceleration in account openings and fund inflows"
            },
            "new_issuance": {
                "name": "New Issuance Flood",
                "weight": 2,
                "description": "Proliferation of IPOs/SPACs/related products"
            },
            "leverage": {
                "name": "Leverage",
                "weight": 2,
                "description": "Imbalances in margin, credit, and funding rates"
            },
            "price_acceleration": {
                "name": "Price Acceleration",
                "weight": 2,
                "description": "Returns reaching upper end of historical distribution"
            },
            "valuation_disconnect": {
                "name": "Valuation Disconnect",
                "weight": 2,
                "description": "Fundamental explanations replaced entirely by narrative"
            },
            "breadth_expansion": {
                "name": "Correlation & Breadth",
                "weight": 2,
                "description": "Broad rally extending to low-quality stocks"
            }
        }
    
    def calculate_score(self, scores: Dict[str, int]) -> Dict:
        """
        Calculate overall assessment from individual indicator scores

        Args:
            scores: Dictionary of scores per indicator (0-2 points)

        Returns:
            Dictionary of evaluation results
        """
        total_score = sum(scores.values())
        max_score = len(self.indicators) * 2
        
        # Determine bubble phase (v2.1 mapping; see module docstring)
        if total_score <= 4:
            phase = "Normal"
            risk_level = "Low"
            action = "Continue normal investment strategy"
        elif total_score <= 7:
            phase = "Caution"
            risk_level = "Medium"
            action = "Begin partial profit-taking, reduce new position sizing"
        elif total_score <= 9:
            phase = "Elevated Risk"
            risk_level = "Medium-High"
            action = "Increase profit-taking, new positions highly selective, build cash reserves"
        elif total_score <= 12:
            phase = "Euphoria"
            risk_level = "High"
            action = "Accelerate stair-step profit-taking, tighten ATR trailing stops, no new long positions except on major pullbacks"
        else:
            phase = "Critical"
            risk_level = "Extremely High"
            action = "Major profit-taking or full hedge, halt new entries, consider short positions after confirming reversal"
        
        # Estimate Minsky phase
        minsky_phase = self._estimate_minsky_phase(scores, total_score)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_score": total_score,
            "max_score": max_score,
            "percentage": round(total_score / max_score * 100, 1),
            "phase": phase,
            "risk_level": risk_level,
            "minsky_phase": minsky_phase,
            "recommended_action": action,
            "indicator_scores": scores,
            "detailed_indicators": self._format_indicator_details(scores)
        }
    
    def _estimate_minsky_phase(self, scores: Dict[str, int], total: int) -> str:
        """Estimate Minsky/Kindleberger phase"""
        mass_pen = scores.get("mass_penetration", 0)
        media = scores.get("media_saturation", 0)
        price_acc = scores.get("price_acceleration", 0)

        if total <= 4:
            return "Displacement/Early Boom (trigger / early expansion)"
        elif total <= 7:
            if media >= 1 and price_acc >= 1:
                return "Boom (expansion phase)"
            else:
                return "Displacement/Early Boom (trigger / early expansion)"
        elif total <= 9:
            if mass_pen >= 2 and media >= 2:
                return "Late Boom/Early Euphoria (late expansion / early euphoria)"
            else:
                return "Boom/Early Euphoria (expansion / early euphoria)"
        elif total <= 12:
            if mass_pen >= 2 and media >= 2:
                return "Euphoria (euphoria phase) - FOMO becomes institutionalized"
            else:
                return "Late Boom/Early Euphoria (late expansion / early euphoria)"
        else:
            if mass_pen >= 2:
                return "Peak Euphoria/Profit Taking (euphoria peak / profit-taking begins) - reversal imminent"
            else:
                return "Euphoria (euphoria phase)"
    
    def _format_indicator_details(self, scores: Dict[str, int]) -> List[Dict]:
        """Format detailed indicator information"""
        details = []
        for key, value in scores.items():
            indicator = self.indicators.get(key, {})
            status = "🔴High" if value == 2 else "🟡Medium" if value == 1 else "🟢Low"
            details.append({
                "indicator": indicator.get("name", key),
                "score": value,
                "status": status,
                "description": indicator.get("description", "")
            })
        return details
    
    def get_scoring_guidelines(self) -> str:
        """Return scoring guidelines for each indicator"""
        guidelines = """
## Bubble Scoring Guidelines

### 1. Mass Penetration
- 0 points: Discussion limited to experts and investors
- 1 point: Recognized by general public but still limited as an investment target
- 2 points: Non-investors (taxi drivers, barbers, family members) actively recommending/mentioning

### 2. Media Saturation
- 0 points: Normal levels of coverage and search trends
- 1 point: Search trends and social media mentions 2-3x normal
- 2 points: TV specials, magazine covers, search trends surging (5x+ normal)

### 3. New Accounts & Inflows
- 0 points: Normal levels of account openings and deposits
- 1 point: Account openings up 50-100% YoY
- 2 points: Account openings up 200%+ YoY, mass influx of "first-time investor" segment

### 4. New Issuance Flood
- 0 points: Normal levels of IPOs and product creation
- 1 point: IPOs/SPACs/related ETFs up 50%+ YoY
- 2 points: Proliferation of low-quality IPOs, indiscriminate creation of "XYZ-related" funds and ETFs

### 5. Leverage Indicators
- 0 points: Margin balances and credit valuation gains/losses within normal range
- 1 point: Margin balances 1.5x historical average, futures position imbalances
- 2 points: Margin balances at all-time highs, persistently elevated funding rates, extreme position imbalances

### 6. Price Acceleration
- 0 points: Annualized returns near median of historical distribution
- 1 point: Annualized returns exceeding 90th percentile historically
- 2 points: Annualized returns in 95th-99th percentile historically, or acceleration (2nd derivative) positive and increasing

### 7. Valuation Disconnect
- 0 points: Reasonably explainable by fundamentals
- 1 point: High valuation but tentatively explainable by "growth expectations"
- 2 points: Explanation entirely dependent on "narrative," "revolution," "paradigm shift"; "this time is different"

### 8. Breadth & Correlation
- 0 points: Only select leading stocks rising
- 1 point: Spreading across entire sector, mid-caps rising
- 2 points: Broad rally extending to low-quality/low-cap stocks, "zombie companies" also rising (last buyers entering)
"""
        return guidelines
    
    def format_output(self, result: Dict) -> str:
        """Format results for readability"""
        output = f"""
{'='*60}
🔍 U.S. Market Bubble Assessment - Bubble-O-Meter
{'='*60}

Evaluation Date/Time: {result['timestamp']}

[Total Score]
{result['total_score']}/{result['max_score']} points ({result['percentage']}%)

[Market Phase]
Current: {result['phase']} (Risk: {result['risk_level']})
Minsky Phase: {result['minsky_phase']}

[Recommended Action]
{result['recommended_action']}

{'='*60}
[Scores by Indicator]
{'='*60}
"""
        for detail in result['detailed_indicators']:
            output += f"\n{detail['status']} {detail['indicator']}: {detail['score']}/2 points\n"
            output += f"   └─ {detail['description']}\n"

        output += f"\n{'='*60}\n"

        return output


def manual_assessment() -> Dict[str, int]:
    """Interactive manual assessment"""
    scorer = BubbleScorer()
    print("\n" + "="*60)
    print("🔍 U.S. Market Bubble Assessment - Manual Assessment")
    print("="*60)
    print("\nPlease evaluate each indicator on a 0-2 scale:")
    print(scorer.get_scoring_guidelines())
    
    scores = {}
    for key, indicator in scorer.indicators.items():
        while True:
            try:
                score = int(input(f"\n{indicator['name']} (0-2): "))
                if 0 <= score <= 2:
                    scores[key] = score
                    break
                else:
                    print("Please enter 0, 1, or 2")
            except ValueError:
                print("Please enter a number")
    
    return scores


def main():
    parser = argparse.ArgumentParser(
        description="Bubble-O-Meter for evaluating U.S. market bubble risk"
    )
    parser.add_argument(
        "--manual",
        action="store_true",
        help="Interactive manual assessment mode"
    )
    parser.add_argument(
        "--scores",
        type=str,
        help="Score string in JSON format (e.g., '{\"mass_penetration\":2,\"media_saturation\":1,...}')"
    )
    parser.add_argument(
        "--output",
        choices=["text", "json"],
        default="text",
        help="Output format"
    )
    
    args = parser.parse_args()
    scorer = BubbleScorer()
    
    # Score collection
    if args.manual:
        scores = manual_assessment()
    elif args.scores:
        try:
            scores = json.loads(args.scores)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format")
            return 1
    else:
        print("Error: Please specify --manual or --scores")
        print("\nDisplaying guidelines:")
        print(scorer.get_scoring_guidelines())
        return 1

    # Run evaluation
    result = scorer.calculate_score(scores)

    # Output
    if args.output == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(scorer.format_output(result))
    
    return 0


if __name__ == "__main__":
    exit(main())
