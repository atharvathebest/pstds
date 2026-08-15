import os
from flask import Flask, render_template, request, jsonify
from openai import AzureOpenAI

app = Flask(__name__)

# Configure your Azure OpenAI credentials
endpoint = "https://ppallavi1978-8495-resource.services.ai.azure.com/"
api_version = "2025-04-01-preview"
deployment = "gpt-image-2"
api_key = "2L75WNfiVC4BBiU3LihlHOza2xsDEcZRga1vBHUfNaYJeT5uwX8zJQQJ99CEACHYHv6XJ3w3AAAAACOGQcAT"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=api_key,
)

@app.route("/")
def home():
    return render_index()

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    user_prompt = data.get("prompt", "")
    
    if not user_prompt:
        return jsonify({"error": "Prompt cannot be empty"}), 400

    try:
        # Call Azure OpenAI to generate the image
        result = client.images.generate(
            model=deployment,
            prompt=user_prompt,
            n=1,
            quality="high",
        )
        
        response_dict = result.model_dump()
        print("FULL API RESPONSE:", response_dict)
        
        data_item = response_dict.get("data", [{}])[0]
        
        # Check if the model returned a URL or base64 data
        image_url = data_item.get("url")
        b64_data = data_item.get("b64_json")
        
        if image_url:
            return jsonify({"image_url": image_url})
        elif b64_data:
            return jsonify({"image_url": f"data:image/png;base64,{b64_data}"})
        else:
            return jsonify({"error": "Failed to retrieve image data from response."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def render_index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)