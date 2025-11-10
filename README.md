# Mirror - AI-Powered Self-Reflection Journal

Mirror is an intelligent journaling application that helps users gain deeper insights into their emotional patterns and cognitive biases through AI-powered analysis. Built with React, Vite, and Supabase, Mirror provides real-time sentiment analysis, bias detection, and emotional timeline tracking.

## Core Features

### 1. Intelligent Journal Entry System
- Write and save journal entries with a clean, distraction-free interface
- Automatic sentiment analysis on every entry
- Real-time emotional state detection (Positive, Neutral, Negative)
- Secure cloud storage with Supabase

### 2. Emotional Timeline
- Visual representation of emotional patterns over time
- Interactive bar chart showing sentiment trends
- Statistics dashboard with:
  - Average mood score
  - Positive days count
  - Neutral days count
  - Challenging days count
- Color-coded emotions (Green: Positive, Yellow: Neutral, Red: Negative)

### 3. Cognitive Bias Detection
Mirror automatically identifies five types of cognitive biases in your writing:

- **Catastrophizing** - Magnifying negative events and expecting worst outcomes
- **Black-and-white Thinking** - Binary extremes without considering middle ground
- **Emotional Reasoning** - Treating feelings as facts
- **Fortune Telling** - Predicting negative outcomes without evidence
- **Overgeneralization** - Treating isolated incidents as universal patterns

Each detected bias includes:
- Visual indicators with icons
- Clear explanations
- Actionable tips for reframing thoughts
- Historical tracking across all entries

### 4. Self-Awareness Growth Tracking
- Total entries counter
- Streak tracking
- Total biases detected counter
- Recent bias detections with context
- Progress insights and encouragement

## Technology Stack

### Frontend
- **React 18** - Modern UI library
- **Vite** - Fast build tool and dev server
- **React Router** - Client-side routing
- **Tailwind CSS** - Utility-first styling
- **Responsive Design** - Mobile-first approach

### Backend
- **Supabase** - PostgreSQL database and Edge Functions
- **Edge Functions** - Serverless functions for analysis
- **Row Level Security (RLS)** - Secure data access policies

### AI Analysis
- **Sentiment Analysis** - Word-based emotional detection
- **Pattern Recognition** - Regex-based bias detection
- **Real-time Processing** - Analysis on entry creation

## Project Structure

```
mirror/
├── src/
│   ├── components/
│   │   ├── BiasInsights.jsx       # Cognitive bias visualization
│   │   ├── EmotionalTimeline.jsx  # Sentiment timeline chart
│   │   ├── Footer.jsx             # Footer component
│   │   ├── Hero.jsx               # Landing page hero
│   │   ├── HowItWorks.jsx         # Feature showcase
│   │   └── SignupForm.jsx         # User registration form
│   ├── pages/
│   │   ├── ContactPage.jsx        # Contact page
│   │   ├── DashboardPage.jsx      # Main dashboard with tabs
│   │   ├── LandingPage.jsx        # Landing page
│   │   ├── PrivacyPage.jsx        # Privacy policy
│   │   ├── SignInPage.jsx         # User sign-in
│   │   └── TermsPage.jsx          # Terms of service
│   ├── utils/
│   │   └── api.js                 # API client functions
│   ├── App.jsx                    # Main app component
│   └── main.jsx                   # App entry point
├── supabase/
│   ├── functions/
│   │   ├── create-journal-entry/  # Entry creation with analysis
│   │   ├── get-journal-entries/   # Fetch entries with biases
│   │   └── signup/                # User registration
│   └── migrations/
│       └── *.sql                  # Database schema migrations
├── backend/                       # Python backend (local development)
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## Database Schema

### Tables

#### users
- `id` (uuid) - Primary key
- `email` (text) - Unique user email
- `name` (text) - User's full name
- `created_at` (timestamp) - Account creation date
- `onboarding_data` (jsonb) - User profile information

#### journal_entries
- `id` (uuid) - Primary key
- `user_id` (uuid) - Foreign key to users
- `entry_text` (text) - Journal entry content
- `timestamp` (timestamp) - Entry creation time
- `sentiment_score` (real) - Sentiment analysis score (-1 to 1)
- `valence` (real) - Combined sentiment valence (-1 to 1)

#### biases
- `id` (uuid) - Primary key
- `entry_id` (uuid) - Foreign key to journal_entries
- `bias_type` (text) - Type of cognitive bias
- `detected_pattern` (text) - Pattern that triggered detection
- `explanation` (text) - User-friendly explanation

#### weekly_summaries
- `id` (uuid) - Primary key
- `user_id` (uuid) - Foreign key to users
- `week_start` (date) - Week start date
- `summary_text` (text) - AI-generated summary
- `themes` (jsonb) - Detected themes
- `emotions` (jsonb) - Detected emotions

## Getting Started

### Prerequisites
- Node.js 18+ and npm
- Supabase account (for cloud deployment)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd mirror
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
Create a `.env` file in the root directory:
```env
VITE_SUPABASE_URL=your_supabase_project_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

4. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### Building for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

## Usage

### Creating an Account
1. Navigate to the landing page
2. Click "Start Reflecting" or scroll to the signup form
3. Fill out the profile information including:
   - Name and email
   - Age group and occupation
   - Journaling experience
   - Primary goals
   - Emotional challenges (optional)
   - Preferred reflection time
4. Submit the form to create your account

### Writing Journal Entries
1. After signing up, you'll be redirected to your dashboard
2. Click on the "Journal" tab (default view)
3. Type your thoughts in the text area
4. Click "Save & Analyze Entry"
5. Your entry will be analyzed for sentiment and cognitive biases

### Viewing Emotional Timeline
1. Navigate to the "Timeline" tab
2. View your emotional journey over time
3. See statistics about your mood patterns
4. Identify trends in your emotional states

### Understanding Cognitive Biases
1. Navigate to the "Biases" tab
2. Review detected biases across all entries
3. Read explanations and tips for each bias type
4. Track your self-awareness growth over time

### Signing In
1. Click "Sign In" on the landing page
2. Enter your registered email address
3. Access your dashboard with all your entries

## API Endpoints

### Edge Functions

#### POST /functions/v1/signup
Create a new user account with profile data.

#### POST /functions/v1/create-journal-entry
Create a new journal entry with automatic sentiment analysis and bias detection.

**Request:**
```json
{
  "userId": "uuid",
  "entryText": "string"
}
```

**Response:**
```json
{
  "success": true,
  "entry": {
    "id": "uuid",
    "entry_text": "string",
    "sentiment_score": 0.5,
    "valence": 0.5,
    "biases": [
      {
        "type": "Catastrophizing",
        "pattern": "string",
        "explanation": "string"
      }
    ]
  }
}
```

#### GET /functions/v1/get-journal-entries?userId={uuid}
Fetch all journal entries for a user with associated biases.

**Response:**
```json
{
  "success": true,
  "entries": [
    {
      "id": "uuid",
      "user_id": "uuid",
      "entry_text": "string",
      "timestamp": "timestamp",
      "sentiment_score": 0.5,
      "valence": 0.5,
      "biases": [...]
    }
  ]
}
```

## Security

- **Row Level Security (RLS)** enabled on all database tables
- **Service role policies** for Edge Function operations
- **Secure session management** with sessionStorage
- **CORS headers** properly configured
- **No authentication tokens** exposed in client code

## Contributing

This is a personal project, but suggestions and feedback are welcome. Please contact arjav.jain1512@icloud.com for inquiries.

## Support

For questions or issues, please contact:
- Email: arjav.jain1512@icloud.com

## License

All rights reserved. This project is not open source.

## Acknowledgments

- Sentiment analysis algorithms inspired by VADER and TextBlob
- Cognitive bias detection patterns based on CBT research
- UI/UX design following modern web best practices
