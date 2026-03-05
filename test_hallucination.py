"""Test 5: Hallucination Detection"""
from app.services.hallucination_detector import detect_hallucination

print("[TEST 5] Hallucination Detection")
print("-" * 60)

# Test Case 1: Truthful answer
context1 = "PM Kisan provides 6000 rupees per year."
answer1 = "PM Kisan provides 6000 rupees per year to eligible farmers."

hallucinated1, confidence1 = detect_hallucination(answer1, context1)
print(f"Test Case 1 (Truthful):")
print(f"  Context: {context1}")
print(f"  Answer: {answer1}")
print(f"  Hallucinated: {hallucinated1}, Confidence: {confidence1:.2f}")

# Test Case 2: Hallucinated answer
context2 = "PM Kisan provides 6000 rupees per year."
answer2 = "PM Kisan provides 12000 rupees per year to eligible farmers."

hallucinated2, confidence2 = detect_hallucination(answer2, context2)
print(f"\nTest Case 2 (Hallucinated):")
print(f"  Context: {context2}")
print(f"  Answer: {answer2}")
print(f"  Hallucinated: {hallucinated2}, Confidence: {confidence2:.2f}")

# Results
if not hallucinated1 and hallucinated2:
    print("\n✅ TEST PASSED: Hallucination detection works correctly")
else:
    print("\n⚠️  Partial detection")
    print(f"   Case 1 should be False (truthful): {hallucinated1}")
    print(f"   Case 2 should be True (hallucinated): {hallucinated2}")
