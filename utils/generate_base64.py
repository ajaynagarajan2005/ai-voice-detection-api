import base64
import os
import sys

def file_to_base64(file_path):
    """Reads an audio file and converts it to a Base64 string."""
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return None
    
    with open(file_path, "rb") as audio_file:
        encoded_string = base64.b64encode(audio_file.read()).decode('utf-8')
    return encoded_string

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_base64.py <audio_file_path>")
        print("Example: python generate_base64.py sample.mp3")
    else:
        file_path = sys.argv[1]
        base64_str = file_to_base64(file_path)
        if base64_str:
            print("\n✅ Success! Copy the string below for the hackathon tester:\n")
            print(base64_str)
            
            # save to a file for easy copying
            with open("base64_output.txt", "w") as f:
                f.write(base64_str)
            print("\n(Also saved to 'base64_output.txt' for easy copying)")
