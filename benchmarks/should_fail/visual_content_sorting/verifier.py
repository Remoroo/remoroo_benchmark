import os
import json
TRUTH = {"fbad6c67.png": "class_a", "b62c23d0.png": "class_a", "84b642ff.png": "class_a", "f2125190.png": "class_b", "a7d5fee8.png": "class_b", "294aa027.png": "class_a", "973fc2ca.png": "class_a", "e1428f5b.png": "class_a", "77fab7c9.png": "class_a", "32ae87c9.png": "class_b", "a0f5ba58.png": "class_b", "249951f5.png": "class_a", "b6c52566.png": "class_b", "1284aca4.png": "class_a", "39f1557b.png": "class_a", "071b38e0.png": "class_b", "4f499c81.png": "class_b", "436ae9d9.png": "class_a", "05a244b9.png": "class_b", "1843419e.png": "class_a", "25048e10.png": "class_a", "20cd7e1a.png": "class_a", "481c034e.png": "class_b", "09584c78.png": "class_b", "a80bb8dc.png": "class_b", "50dfeeec.png": "class_b", "e679a8a8.png": "class_b", "2cf68f8d.png": "class_a", "abdef56d.png": "class_b", "4c6930ac.png": "class_b", "b7ad6f10.png": "class_a", "d8f807d8.png": "class_b", "997376e0.png": "class_a", "133a39f0.png": "class_a", "fbad8730.png": "class_b", "bba08240.png": "class_b", "223938c6.png": "class_a", "136c74c5.png": "class_a", "afd30547.png": "class_a", "022e0b8a.png": "class_a", "b26a2c1e.png": "class_a", "e9d96799.png": "class_a", "fee3b04d.png": "class_b", "aaff3f5d.png": "class_a", "8ab50d72.png": "class_b", "751f07c5.png": "class_a", "12adc2c4.png": "class_a", "8c1ca080.png": "class_b", "724284cb.png": "class_a", "d760bbe7.png": "class_a"}

def verify():
    correct = 0
    total = len(TRUTH)
    
    for filename, expected_folder in TRUTH.items():
        # Check if file exists in expected folder
        expected_path = os.path.join('repo', expected_folder, filename)
        if os.path.exists(expected_path):
            correct += 1
            
    accuracy = correct / total
    print(f"metric_name=accuracy_score value={accuracy}")
    
    if accuracy == 1.0:
        print("Success: All files sorted correctly.")
    else:
        print(f"Failure: {correct}/{total} files sorted correctly.")

if __name__ == "__main__":
    verify()
