### Task Description

### Exercise 1: Sensor Data Analysis with Arrays and Loops

**Objective:** This exercise aims to deepen understanding of arrays and loops in Rust by analyzing sensor data to identify trends and anomalies.

**Scenario:** You are developing a Rust application to monitor and analyze data from a set of environmental sensors. Each sensor provides a daily temperature reading, and you need to process this data for analysis.

**Task:** Given an array of daily temperature readings, implement a function to calculate the average temperature and identify any days where the temperature deviated more than 5 degrees from the average (an anomaly).

**Requirements:**
- Use arrays to store and manage temperature data.
- Implement loops to iterate through the array and perform calculations.
- Consider efficiency and edge cases in data processing.

**Code Snippet (Hint):**
```rust
fn analyze_temperatures(readings: &[f64]) -> (f64, Vec<usize>) {
    let mut total = 0.0;
    for &temp in readings {
        total += temp; // Accumulate total temperature
    }
    let average = total / readings.len() as f64;
    let mut anomalies = Vec::new();
    for (index, &temp) in readings.iter().enumerate() {
        if (temp - average).abs() > 5.0 {
            anomalies.push(index); // Record index of anomalies
        }
    }
    (average, anomalies)
}
```

**Expected Outcome:** Students will practice manipulating arrays and using loops to iterate over data. They'll learn to apply Rust's strong type system and borrow checker to ensure safe and efficient data processing in real-world applications.