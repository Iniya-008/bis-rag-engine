import argparse
import json

def calculate_metrics(ground_truth, predictions):
    """
    Calculates Hit Rate @3, MRR @5, and Avg Latency based on the hackathon formula.
    """
    pred_dict = {p.get("id", p.get("query_id")): p for p in predictions}
    
    correct_queries = 0
    total_queries = len(ground_truth)
    mrr_sum = 0
    total_latency = 0
    
    for gt in ground_truth:
        q_id = gt.get("id", gt.get("query_id"))
        
        # We assume the GT contains an 'expected_standards' list. Adjust if the actual schema differs.
        expected_stds = gt.get("expected_standards", []) 
        
        if q_id not in pred_dict:
            continue
            
        pred = pred_dict[q_id]
        retrieved = pred.get("retrieved_standards", [])
        total_latency += pred.get("latency_seconds", 0)
        
        # Hit Rate @3
        top_3 = retrieved[:3]
        hit = False
        for expected in expected_stds:
            if expected in top_3:
                hit = True
                break
        if hit:
            correct_queries += 1
            
        # MRR @5
        top_5 = retrieved[:5]
        for rank, item in enumerate(top_5, start=1):
            if item in expected_stds:
                mrr_sum += (1.0 / rank)
                break
                
    hit_rate = (correct_queries / total_queries) * 100 if total_queries > 0 else 0
    mrr = mrr_sum / total_queries if total_queries > 0 else 0
    avg_latency = total_latency / total_queries if total_queries > 0 else 0
    
    return hit_rate, mrr, avg_latency

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hackathon Official Evaluation Script")
    parser.add_argument("--ground_truth", type=str, required=True, help="Path to ground truth JSON")
    parser.add_argument("--predictions", type=str, required=True, help="Path to team output JSON")
    args = parser.parse_args()
    
    try:
        with open(args.ground_truth, 'r') as f:
            gt_data = json.load(f)
        with open(args.predictions, 'r') as f:
            pred_data = json.load(f)
            
        hr3, mrr5, lat = calculate_metrics(gt_data, pred_data)
        
        print(f"\n======================================")
        print(f"      HACKATHON METRICS RESULTS       ")
        print(f"======================================")
        print(f"Hit Rate @3: {hr3:.2f}%  (Target: >80%)")
        print(f"MRR @5:      {mrr5:.3f}   (Target: >0.7)")
        print(f"Avg Latency: {lat:.3f}s  (Target: <5s)")
        print(f"======================================\n")
        
    except Exception as e:
        print(f"Evaluation crashed: {e}")
