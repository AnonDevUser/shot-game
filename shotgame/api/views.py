from rest_framework.response import Response 
from rest_framework.decorators import api_view
from shot.models import Question
from groq import Groq
from django.conf import settings
import json
import re

@api_view(['GET'])
def get_question(request):
    client = Groq(api_key=settings.GROQ_API_KEY)
    prompt = """
         You are generating calculus questions suitable for first-year Civil Engineering students in the Philippines following the CHED curriculum (Calculus 1).

            Topics allowed:
            - Limits
            - Continuity
            - Derivatives of algebraic, trigonometric, exponential, and logarithmic functions
            - Implicit differentiation
            - Related rates
            - Higher-order derivatives
            - Basic antiderivatives
            - Indefinite integrals
            - Definite integrals with simple bounds
            - Algebraic simplification involving polynomials, roots, exponentials, or trig functions

            Requirements:
            1. Generate **4 multiple-choice options** for the answer:
            - Exactly **one** must be correct.
            - The other three should be plausible distractors.
            2. Output the answers in **normal human-readable math notation**, suitable for displaying on a website.  
            - Example: `3x^2 - 2` instead of `3*x**2 - 2`
            3. Output in **JSON** with the following fields:
            - "human": the question in normal math English
            - "options": an array of 4 options (strings), in **human-readable math**
            - "correct_option_index": the **0-based index** of the correct answer in the options array

            Example output:

            {
            "human": "Differentiate: f(x) = x^3 - 2x + 1",
            "options": [
                "3x^2 - 2",
                "x^3 - 2",
                "3x^2 + 2",
                "x^2 - 2"
            ],
            "correct_option_index": 0
            }

            Generate ONE random calculus question per request.

            """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    result = response.choices[0].message.content
    
    # Clean up the response
    result = result.replace(""", '"').replace(""", '"')
    result = result.replace("'", '"')  # Replace single quotes with double quotes
    
    # Remove markdown code blocks if present
    result = re.sub(r'```json\s*', '', result)
    result = re.sub(r'```\s*', '', result)
    result = result.strip()
    
    # Try to parse JSON
    parsed_result = None
    try:
        parsed_result = json.loads(result)
    except json.JSONDecodeError:
        # Try to extract JSON object from the response using a more robust pattern
        # Match balanced braces
        brace_count = 0
        start_idx = -1
        for i, char in enumerate(result):
            if char == '{':
                if start_idx == -1:
                    start_idx = i
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0 and start_idx != -1:
                    json_text = result[start_idx:i+1]
                    try:
                        parsed_result = json.loads(json_text)
                        break
                    except json.JSONDecodeError:
                        start_idx = -1
                        brace_count = 0
                        continue
        
        # If still no match, try regex as fallback
        if parsed_result is None:
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', result)
            if json_match:
                try:
                    parsed_result = json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass

    if parsed_result is None or not isinstance(parsed_result, dict) or "human" not in parsed_result:
        # Return error with the actual response for debugging
        return Response({
            "error": "Failed to parse question from API response",
            "raw_response": result[:500] if len(result) > 500 else result
        }, status=500)
    
    result = parsed_result

    question = result["human"]
    options = result["options"]
    correct_option = result["correct_option_index"]

    q = Question.objects.create(
        human=question,
        options = options,
        correct_option_index=correct_option
    )
    return Response({
        "question_id": q.id,  
        "question": question,
        "options": options
    })

@api_view((['POST']))
def check_answer(request):
    question_id = request.data.get("question_id")
    chosen_answer = request.data.get("chosen_answer")

    actual = Question.objects.get(id=int(question_id))
    if actual.correct_option_index == int(chosen_answer):
        return Response({
        "correct":True
        })
    else: 
        return Response({
        "correct":False
        })