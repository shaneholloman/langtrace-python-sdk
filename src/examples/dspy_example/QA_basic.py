import dspy
from langtrace_python_sdk import langtrace
from dotenv import load_dotenv

load_dotenv()

langtrace.init(disable_instrumentations={"all_except": ["dspy", "anthropic"]})

# configure the language model to be used by dspy

lm = dspy.LM('claude-3-opus-20240229')
dspy.configure(lm=lm)

# create a prompt format that says that the llm will take a question and give back an answer
predict = dspy.Predict("question -> answer")
prediction = predict(
    question="who scored the final goal in football world cup finals in 2014?"
)

print(prediction.answer)
