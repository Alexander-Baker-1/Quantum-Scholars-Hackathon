from Baker_HW6 import (
    generate_random_string, 
    generate_alice_state, 
    eavesdrop, 
    bob_evolution, 
    measurement_result, 
    alice_create_secret_key, 
    bob_create_secret_key, 
    check_for_Eve
)

def run_test_suite(n, e):
    detections = 0
    total_sk_len = 0
    success_count = 0

    for i in range(10):
        a = generate_random_string(n)
        state = generate_alice_state(a)
        state = eavesdrop(e, n, state)
        
        b = generate_random_string(n)
        u_b = bob_evolution(b)
        t = measurement_result(b, state, u_b)
        
        sk_a = alice_create_secret_key(a, t)
        sk_b = bob_create_secret_key(b, t)
        
        check = check_for_Eve(sk_a, sk_b)
        if check == "Eve detected!":
            detections += 1
        else:
            success_count += 1
            total_sk_len += len(check)

    avg_sk_len = total_sk_len / success_count if success_count > 0 else 0
    return detections, avg_sk_len

n_small = 9
detections, avg_len = run_test_suite(n_small, True)
print(f"Results for small n={n_small}: Eve detected {detections}/10 times.")

n_large = 15
detections, avg_len = run_test_suite(n_large, True)
print(f"Results for large n={n_large}: Eve detected {detections}/10 times.")