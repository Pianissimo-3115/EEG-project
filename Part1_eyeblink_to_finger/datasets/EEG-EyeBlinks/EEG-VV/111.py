import matplotlib.pyplot as plt

# Step 1: Create data for two line graphs
x1 = [0, 1, 2, 3, 4, 5]
y1 = [0, 1, 4, 9, 16, 25]

x2 = [0, 1, 2, 3, 4, 5]
y2 = [0, 1, 8, 27, 64, 125]

# Step 2: Plot the first line graph
plt.plot(x1, y1, label='y = x^2', color='blue', marker='o')

# Step 3: Plot the second line graph
plt.plot(x2, y2, label='y = x^3', color='red', marker='x')

# Step 4: Add labels and a legend
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Two Line Graphs in One Plot')
plt.legend()

# Step 5: Display the plot
plt.show()