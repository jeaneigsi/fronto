from trulens import Trulens

# Your variables
r1 = "Description of the page"
r2 = "Generated code based on the description"

# Initialize the Trulens client
client = Trulens("YOUR_API_KEY")

# Prepare the input data
input_data = {
    "description": r1,
    "code": r2
}

# Call the Trulens API
response = client.evaluate(input_data)

# Process the API response
evaluation_score = response["score"]
evaluation_feedback = response["feedback"]

# Use the evaluation results
print(f"Evaluation Score: {evaluation_score}")
print(f"Evaluation Feedback: {evaluation_feedback}")
