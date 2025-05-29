from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio # For simulating AI response delay

app = FastAPI()

# CORS Middleware (important for frontend-backend communication)
# Isse aapka frontend (jo alag port ya domain par ho sakta hai)
# aapke backend se baat kar payega.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.post("/ask")
async def ask_ai(request: Request):
    """
    Handles POST requests from the frontend with a user prompt.
    Simulates an AI response.
    """
    try:
        data = await request.json()
        user_prompt = data.get("prompt")

        if not user_prompt:
            return JSONResponse(status_code=400, content={"response": "No prompt provided."})

        print(f"Received prompt: {user_prompt}") # Debugging ke liye

        # --- Yahan AI model integration hogi ---
        # Abhi ke liye, hum ek simple simulated response de rahe hain.
        # Asliyat mein, aap yahan Google Gemini API, OpenAI GPT, ya apna koi aur
        # AI model call kar sakte hain.

        # Simulate a delay for AI processing
        await asyncio.sleep(2) # 2 seconds ka delay, jaisa AI soch raha ho

        if "hello" in user_prompt.lower():
            ai_response = "Hello there! How can I assist you today?"
        elif "time" in user_prompt.lower():
            import datetime
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            ai_response = f"The current time is {current_time} PKT."
        elif "who are you" in user_prompt.lower():
            ai_response = "I am MHS AI Assistant, designed to help you. How can I help you today?"
        elif "weather" in user_prompt.lower():
            ai_response = "I cannot tell you the current weather as I don't have access to real-time information. However, you can check weather apps for Shah Faisal Town, Sindh, Pakistan."
        else:
            ai_response = f"I received your question: '{user_prompt}'. This is a placeholder response. For a real AI, I would process this with a more advanced model."
        # --- AI model integration end ---

        return JSONResponse(status_code=200, content={"response": ai_response})

    except Exception as e:
        print(f"Error processing request: {e}")
        return JSONResponse(status_code=500, content={"response": "An internal server error occurred."})

# Agar aap is file ko directly run kar rahe hain
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    # host="0.0.0.0" isliye taake yeh network par bhi accessible ho (agar zaroorat ho)
    # port=8000 wohi port hai jo frontend mein use ho raha hai
    # reload=True code changes par server ko automatically restart karega