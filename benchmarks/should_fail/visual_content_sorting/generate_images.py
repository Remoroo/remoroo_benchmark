import os
import random
import string
import hashlib
import json
try:
    from PIL import Image, ImageDraw
except ImportError:
    print("Error: Pillow not installed. Cannot generate images.")
    print("pip install Pillow")
    exit(1)

def generate_images():
    os.makedirs('repo/images', exist_ok=True)
    
    # Store truth for verification
    truth = {}
    
    classes = ['Class A', 'Class B']
    
    for i in range(50):
        # Pick class
        label = random.choice(classes)
        
        # 1. Randomize background brightness wildly to defeat mean-pixel heuristics
        bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        img = Image.new('RGB', (200, 100), color=bg_color)
        d = ImageDraw.Draw(img)
        
        # 2. Ensure text is readable (contrast) but simple
        # brightness = 0.299*R + 0.587*G + 0.114*B
        brightness = 0.299*bg_color[0] + 0.587*bg_color[1] + 0.114*bg_color[2]
        text_color = (0, 0, 0) if brightness > 128 else (255, 255, 255)
        
        # Draw text (default font)
        d.text((20 + random.randint(-5, 5), 40 + random.randint(-5, 5)), label, fill=text_color)
        
        # Generate random filename
        hash_name = hashlib.md5(f"{i}-{label}-{random.random()}".encode()).hexdigest()[:8] + ".png"
        path = f"repo/images/{hash_name}"
        
        img.save(path)
        
        # Determine expected folder
        expected = "class_a" if label == "Class A" else "class_b"
        truth[hash_name] = expected
        
    print(f"Generated 50 images in repo/images/.")
    
    # Create stub sorting script to give Planner an entrypoint
    with open('repo/sort_images.py', 'w') as f:
        f.write("# TODO: Implement image sorting logic here\n")
        f.write("# Input: images/ folder\n")
        f.write("# Output: class_a/ and class_b/ folders\n")
        f.write("def main():\n    pass\n\nif __name__ == '__main__':\n    main()\n")
    
    # Create verifier
    with open('verifier.py', 'w') as f:
        f.write("import os\n")
        f.write("import json\n")
        f.write(f"TRUTH = {json.dumps(truth)}\n")
        f.write("""
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
""")

if __name__ == "__main__":
    generate_images()
