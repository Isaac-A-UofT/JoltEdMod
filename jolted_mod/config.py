prompts = {
    "SeedBlock": "Behave as a {identity} who is explaining {topic} to {target_audience}",
    "ExplanatoryBlock": "This is a {type_of_cell} block in a Jupyter Notebook. Use appropriate headers for chapter sections if of type Markdown. Do not give solutions if this is a Code block. Explain {topic} by {method_of_teaching} in a way that is relatable to {target_audience}. Be careful not to be overly dramatic and not to talk down to the audience.",
    "KnowledgeTestingBlock": {
        "markdown": "Design {n} {question_type} of an appropriate difficulty for {target_audience} about that {topic}",
        "code": "Create code with empty methods that have comments for what they should do but no implementation to answer the following question: {context_content}. After that, create 3 assertion tests that the student will use to test if they have implemented their",
    },
}
