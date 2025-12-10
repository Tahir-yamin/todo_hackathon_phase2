---
id: 4
title: "Redesign Frontend UI Todoist Style"
stage: "general"
date_iso: "2025-12-09"
surface: "agent"
model: "claude-3-5-sonnet"
feature: "none"
branch: "001-in-memory-todo-app"
user: "linux"
command: "/sp.implement"
labels: ["ui", "ux", "frontend", "design", "todoist"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - frontend/src/app/globals.css
  - frontend/src/app/page.tsx
  - frontend/src/components/TaskForm.tsx
  - frontend/src/components/TaskList.tsx
tests_yaml: |
  -
prompt_text: |
  "Redesign the Frontend UI to match a modern 'Todoist-style' aesthetic.

  Context:
  The current UI is too stark (high contrast black/white) and unpolished.
  We want a clean, user-friendly interface with better visual hierarchy.

  Requirements:
  1. Update `frontend/src/app/globals.css`:
     - Replace the pure black background with a dark gray theme (bg-gray-900) for Dark Mode.
     - Set a default sans-serif font (Inter).

  2. Refactor `frontend/src/app/page.tsx` (Layout):
     - Center the main content in a `max-w-3xl` container with `mx-auto`.
     - Add a distinct Header section with the App Title.

  3. Refactor `frontend/src/components/TaskForm.tsx`:
     - Redesign the form to look like a 'card' with a subtle shadow (`shadow-lg`).
     - Use rounded corners (`rounded-lg`) and softer borders (`border-gray-700`).
     - Style the 'Create Task' button to be prominent (e.g., `bg-red-500` or `bg-blue-600`) with hover effects.
     - Organize inputs (Title, Priority, Date) into a clean grid or flex layout, not just a vertical stack.

  4. Refactor `frontend/src/components/TaskList.tsx`:
     - Render tasks as individual rows with a border-bottom separator.
     - Use color-coded badges for Priority (e.g., Red for High, Yellow for Medium).
     - Display the Due Date in small, muted text next to the title.
     - Make the 'Delete' and 'Complete' buttons icon-based or cleaner text buttons that appear on hover.

  5. General UX:
     - Add simple transitions/animations for hover states.
     - Ensure the 'Empty State' (No tasks yet) looks inviting, perhaps with an illustration or friendly text centered on the screen.
"
response_text: |
  Successfully redesigned the frontend UI to match a modern 'Todoist-style' aesthetic:

  1. Updated globals.css:
     - Implemented dark gray theme (bg-gray-900 equivalent: rgb(17, 17, 17))
     - Set default font to Inter

  2. Refactored page.tsx:
     - Centered main content in max-w-3xl container
     - Added distinct header section with app title and subtitle

  3. Redesigned TaskForm.tsx:
     - Created card-like appearance with shadow-lg and rounded-lg
     - Added subtle border and hover effects
     - Implemented grid layout for inputs
     - Styled button with blue color, hover effects, and loading spinner
     - Added smooth transitions and hover animations

  4. Redesigned TaskList.tsx:
     - Changed to row-based layout with dividers
     - Added color-coded priority badges (red/yellow/green)
     - Displayed due dates in muted text
     - Implemented icon-based buttons that appear on hover
     - Added status badges with appropriate colors
     - Created inviting empty state with centered content

  5. General UX improvements:
     - Added hover effects and transitions throughout
     - Implemented smooth animations for interactive elements
     - Improved visual hierarchy and spacing
     - Enhanced accessibility with proper titles and semantic structure
outcome: "Successfully implemented modern Todoist-style UI with improved visual hierarchy, hover effects, and better user experience."
evaluation: "All requirements met: dark theme, Inter font, centered layout, card-styled form, row-based task display, color-coded badges, icon buttons, hover effects, and inviting empty state."
---

# Frontend UI Redesign - Todoist-Style Aesthetic

## Summary
Successfully redesigned the frontend UI to match a modern 'Todoist-style' aesthetic with improved visual hierarchy and user experience.

## Changes Made

### 1. globals.css
- Updated to dark gray theme (bg-gray-900 equivalent)
- Set default font to Inter

### 2. page.tsx
- Centered main content in max-w-3xl container
- Added distinct header section with app title and subtitle

### 3. TaskForm.tsx
- Redesigned as card with shadow-lg and rounded-lg
- Implemented grid layout for inputs
- Styled button with blue color and hover effects
- Added loading spinner and smooth transitions

### 4. TaskList.tsx
- Changed to row-based display with dividers
- Added color-coded priority badges
- Displayed due dates in muted text
- Implemented icon-based buttons that appear on hover
- Created inviting empty state

## Result
The application now has a modern, polished UI with improved visual hierarchy, hover effects, and better user experience following Todoist-style design principles.