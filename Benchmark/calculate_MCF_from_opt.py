def calculate_MCF_from_opt(filename):
    total = 0
    count = 0

    # Open the file and read line by line
    with open(filename, 'r') as file:
        for line in file:
            # Strip whitespace from the line
            line = line.strip()
            if line:  # Check if the line is not empty
                try:
                    # Convert the line to a float and add to the total
                    number = float(line)
                    total += number
                    count += 1
                except ValueError:
                    # If the line cannot be converted to float, skip it
                    print(f"Skipping invalid line: {line}")

    # Calculate the mean if at least one number was successfully read
    if count > 0:
        mean = total / count
    else:
        mean = 0  # Default to 0 if no valid numbers were found

    return mean


# Example usage
filename = "/traffic-matrices/perturbated/Abilene/Gaussian_Multiplicative_Noise/0.4/test.opt"  # Specify the path to your file
mean_value = calculate_MCF_from_opt(filename)
print(f"The mean value is: {mean_value}")
