# Donna - your badass AI Secretary 

Donna screens your calls, rejecting the spam and preserving your sanity by sending callers your scheduling / Calendly link when you're busy. Using the latest [Realtime API](https://openai.com/index/introducing-the-realtime-api/) from OpenAI in conjunction with function calling to Google Calendar and Twilio, Donna knows when you're busy in real time and can handle multiple callers at once in 85 different languages!

**Monorepo Stack**:
- FastAPI backend written in Python
  - processes phone calls and audio streaming between both Twilio and OpenAI usings websockets
  - powers both inbound and outbound calls to and from Donna
  - reads from Google Calendar
  - sends scheduling text messages
  - reports live call status
- Next.js frontend written in Typescript
  - `/status` page that visualizes calls in real-time
  - integration with EdgeDB to handle user preferences and (in the future) semantic searching over previous conversations
 
![Screen Recording 2024-10-13 at 1 55 01 AM](https://github.com/user-attachments/assets/6cceb50d-c4a2-4fc7-a8ae-b2d903cdfab9)

## Running the apps
`.env` file:
```env
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=   ←dedicated Twilio number
HARVEY_PHONE_NUMBER=   ←your cell phone
STREAM_URL=            ←backend websockets URL
OPENAI_API_KEY=
CALENDLY_URL=          ←meeting scheduling link of your choice
```
You'll need a dedicated Twilio phone number and to either deploy the server or run it locally through a tunnel (ie via `ngrok`) to expose the API to Twilio.
We used [Poetry](https://python-poetry.org/) to handle Python dependencies on the backend and [pnpm](https://pnpm.io/) for the frontend.

1. clone the repo
2. `cd frontend`
3. `pnpm install && pnpm dev` to start the frontend
4. navigate to `localhost:3000/status` to view the live status page
5. `cd ../backend`
6. `poetry install`
7. `poetry shell`
    now, you can run our custom scripts:
   - `f` or `format` to run Ruff formatting
   - `l` or `lint` to run Mypy and Ruff linting
   - `fl` to run both
   - `dev` to start the dev server
8. call Donna!



 
