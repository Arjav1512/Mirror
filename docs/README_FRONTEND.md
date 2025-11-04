# Mirror Frontend - React + Tailwind CSS

Modern React frontend built with Vite, React, and Tailwind CSS.

## Development Setup

### Prerequisites
- Node.js 18+ and npm

### Install Dependencies
```bash
cd frontend
npm install
```

### Development Server
```bash
npm run dev
```
Runs on http://localhost:3000 with hot reload.

### Build for Production
```bash
npm run build
```
Builds to `frontend/dist/` directory.

## Integration

The frontend integrates with:
- **Landing Page Server**: Port 5000 (serves React build)
- **API Server**: Port 5001 (Flask backend for form submissions)
- **Streamlit App**: Port 8501 (journal interface)

## Project Structure

```
frontend/
├── src/
│   ├── components/     # React components
│   │   ├── Hero.jsx
│   │   ├── HowItWorks.jsx
│   │   ├── SignupForm.jsx
│   │   └── Footer.jsx
│   ├── pages/          # Page components
│   │   └── LandingPage.jsx
│   ├── utils/          # Utilities
│   │   └── api.js      # API functions
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── public/
├── dist/               # Production build
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## Features

- ✅ Modern React 18 with hooks
- ✅ Tailwind CSS for styling
- ✅ Responsive design
- ✅ Smooth animations
- ✅ Form validation
- ✅ API integration
- ✅ Error handling

