prompts = {
    "SeedBlock": "Produce output for a textbook or tutorial module as written by a {identity} who is explaining {topic} to {target_audience}",

    "ExplanatoryBlock": "This is a {type_of_cell} block in a Jupyter Notebook. Use appropriate headers for chapter sections if of type Markdown. Do not give solutions if this is a Code block. Explain {topic} by {instructional_event} in a way that is relatable to {target_audience}. Be careful not to be overly dramatic and not to talk down to the audience.",

    "ExplanatoryBlockKC": "You are producing a jupyter notebook based tutorial for {target_audience} about {knowledge_component} by {instructional_event}. Assume your output is part of a tutorial that covers the other aspects of {topic}. DO NOT REPEAT AN INTRODUCTION, SUMMARY, OR ANY OTHER CONTENT. ONLY PRODUCE CONTENT ON {knowledge_component}",

    "KnowledgeTestingBlock": {
        "markdown": "Design {n} {question_type} of an appropriate difficulty for {target_audience} about that {topic}",
        "code": "Create code with empty methods that have comments for what they should do but no implementation to answer the following question: {context_content}. After that, create 3 assertion tests that the student will use to test if they have implemented their solution correctly",
    },

    "KnowledgeTestingBlockKC": {
        "markdown": "Design {n} {question_type} of an appropriate difficulty for {target_audience} about that {knowledge_component}. Do not produce a solution, just the question. DO NOT REPEAT AN INTRODUCTION, SUMMARY, OR ANY OTHER CONTENT. ONLY PRODUCE CONTENT ON {knowledge_component}",
        "code": "Create code with empty methods that have comments for what they should do but no implementation to answer the following question: {context_content}. After that, create 3 assertion tests that the student will use to test if they have implemented their solution correctly",
    },

}
