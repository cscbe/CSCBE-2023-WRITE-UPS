import os
import random
import string
import sys

# Check that the correct number of arguments were passed
if len(sys.argv) != 4:
    print("Usage: python generate_chal.py <flag> <amount> <num_file_to_hide_flag>")
    print("Example: python generate_files.py 'Here the real flag: CSC{th3_53cr3t_15_5ug3rcan3}' 1000 555")
    sys.exit(1)

# Get the values of the arguments
flag = sys.argv[1] # "CSC{th3_53cr3t_15_5ug3rcan3}"
num_files = int(sys.argv[2]) # 1000

# Set the name of the hidden file
hidden_file_name = f"file{sys.argv[3]}.txt" # file969.txt

# Set the directory to create the files in
directory = "./html"

# Create the directory if it doesn't exist
if not os.path.exists(directory):
    os.makedirs(directory)

# Create the random files
for i in range(num_files):
    # Generate a random file name
    file_name = f"file{i}.txt"
    file_path = os.path.join(directory, file_name)

    # Generate random file content
    file_content = "".join(random.choices(string.ascii_lowercase, k=100))

    # Write the file content to the file
    with open(file_path, "w") as f:
        f.write(file_content)

    # If this is the file to be hidden, append the hidden text to it
    if file_name == hidden_file_name:
        with open(file_path, "w") as f:
            f.write("\n" + flag)

print("Finished generating files!")