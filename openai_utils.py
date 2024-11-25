import openai
import os

def generate_html(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a programmer only producing high quality HTML code. Always include proper HTML structure with doctype, head, and body tags."},
                {"role": "user", "content": prompt},
            ],
            n=1,
            temperature=0.7,
        )
        
        content = response['choices'][0]['message']['content']
        if not content or not isinstance(content, str):
            raise ValueError("Invalid response from OpenAI API")
            
        # Ensure the content has basic HTML structure
        if not content.strip().startswith('<!DOCTYPE html>'):
            content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Generated Website</title>
</head>
<body>
{content}
</body>
</html>"""
            
        return content
    except Exception as e:
        print(f"Error generating HTML: {str(e)}")
        # Return a basic valid HTML structure
        return """<!DOCTYPE html>
<html>
<head>
    <title>Error Page</title>
</head>
<body>
    <h1>Error Generating Content</h1>
    <p>There was an error generating the content. Please try again.</p>
</body>
</html>"""
