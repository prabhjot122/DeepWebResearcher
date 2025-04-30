# Deep Web Researcher - Frontend

This is the frontend application for the **Deep Web Researcher** project, a powerful tool that conducts comprehensive research on any topic, performs fact-checking, and generates polished content in various styles.

---

## Features
- Interactive orbital search interface
- Three content styles: Blog Post, Detailed Report, and Executive Summary
- Real-time research progress tracking
- Content library management
- Draft editing and organization
- Responsive design for desktop and mobile

---

## Prerequisites
- **Node.js** (v16.x or higher)
- **npm** (v8.x or higher)

---

## Installation

### Clone the repository
```bash
git clone https://github.com/sahilsaurav2507/DeepWebResearcher.git
cd DeepWebResearcher/ChatBot
```

### Install dependencies
```bash
npm install
```

---

## Required Dependencies

### Core Libraries
```bash
npm install react react-dom react-router-dom framer-motion
```

### UI Components & Styling
```bash
npm install @radix-ui/react-dialog @radix-ui/react-label @radix-ui/react-select @radix-ui/react-slot @radix-ui/react-toast
npx shadcn@latest init
npm install class-variance-authority clsx tailwindcss-animate lucide-react
npm install tailwindcss postcss autoprefixer
npm install react-icons
```

### Rich Text Editing
```bash
npm install slate slate-react slate-history
```

### Utilities & Types
```bash
npm install next-themes
npm install @types/node @types/react @types/react-dom typescript
```

---

## Configuration

Create a `.env` file in the root directory and add:
```env
VITE_API_BASE_URL=http://localhost:5000
```

> Adjust the API URL if your backend is running on a different port.

---

## Running the Application

### Start the development server
```bash
npm run dev
```

Open your browser and navigate to:
```
http://localhost:5173
```

---

## Building for Production

### Create a production build
```bash
npm run build
```

### Preview the production build locally
```bash
npm run preview
```

---

## Project Structure

| Folder | Description |
|:-------|:------------|
| `/src` | Main source code |
| `/components` | Reusable UI components |
| `/pages` | Page components |
| `/services` | API services |
| `/types` | TypeScript type definitions |
| `/utils` | Utility functions |
| `/hooks` | Custom React hooks |
| `/styles` | Global styles and theme configuration |

---

## Key Components
- **SearchHub**: Interactive orbital search interface
- **EditorPage**: Content editing and management
- **LibraryPage**: Draft organization and browsing
- **ResearchLoadingScreen**: Engaging loading experience showing research progress

---

## Backend Integration

The frontend communicates with the Deep Web Researcher backend API for:
- Starting research queries
- Retrieving research results
- Managing drafts and library content
- Organizing content into playlists

> Ensure the backend server is running before using the application. See the backend README for setup instructions.

---

## Customization
- Modify the theme in `src/components/theme-provider.tsx`
- Adjust the search categories in `src/components/SearchHub.tsx`
- Customize the research steps in `src/components/ResearchLoadingScreen.tsx`

---

## License

This project is licensed under the **MIT License**.

---

## Acknowledgements
- Built with **React**
- UI components powered by **shadcn/ui**
- Animations with **Framer Motion**
- Icons from **Lucide** and **React Icons**

---
