# Smart Parking System - Frontend

Next.js frontend application for the Smart Parking System.

## 🚀 Getting Started

### Install Dependencies

```bash
npm install
```

### Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## 📁 Project Structure

```
frontend/
├── app/              # Next.js app directory
│   ├── page.tsx      # Home page
│   ├── login/        # Login page
│   ├── register/     # Registration page
│   ├── dashboard/    # User dashboard
│   └── parking-lots/ # Parking lot details
├── lib/              # Utility functions
│   └── api.ts        # API client
└── public/           # Static assets
```

## 🔧 Configuration

Set the API URL in `.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:5000
```

## 📝 Features

- ✅ Home page with parking lot listing
- ✅ User registration
- ✅ User login
- ✅ Parking lot details
- ✅ User dashboard
- ✅ API integration

## 🛠️ Tech Stack

- Next.js 16
- React 19
- TypeScript
- Tailwind CSS

## 📦 Build

```bash
npm run build
npm start
```
