# Modern Full-Stack Development Skills - TODO App Implementation

## Project Overview

Complete production-ready TODO application featuring neural network UI theme, AI-powered task management, search & filters, dark/light mode, and comprehensive analytics.

**Tech Stack**: Next.js 14, FastAPI, PostgreSQL, Better Auth, Tailwind CSS

---

## UI/UX Design Patterns

### Neural Network Theme

**Aesthetic**: Cyberpunk/neural network inspired design language

**Color Palette**:
- **Dark Mode** (Default):
  - Primary: Cyan (#00F0FF) 
  - Background: Deep Dark (#0A0D14)
  - Text: Light Slate (#B0C0D0)
  - Accent: Glow effects with shadows

- **Light Mode**:
  - Primary: Blue (#0078B4)
  - Background: White (#FFFFFF)
  - Text: Dark Slate (#1E293B)
  - Surfaces: Light Gray (#F8FAFC)

**Typography**: Space Grotesk (Google Fonts) - mono-spaced aesthetic

###  Component Library

#### 1. Cyber Panel
```css
.cyber-panel {
  background: slate-900/50;
  backdrop-blur-sm;
  border: 1px solid cyan-500/30;
  border-radius: 0.125rem; /* Sharp corners */
}
```

**Usage**: Main containers, cards, modals

#### 2. Neural Column
```css
.neural-column {
  background: linear-gradient(180deg, rgba(0,240,255,0.05), rgba(0,240,255,0.01));
  border: 1px solid rgba(0, 240, 255, 0.1);
  box-shadow: 0 0 10px rgba(0, 240, 255, 0.1);
}
```

**Usage**: Kanban columns, sectioned areas

#### 3. Node Card
```css
.node-card {
  /* Extends cyber-panel */
  cursor: grab;
  transition: all 0.2s;
}

.node-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
}
```

**Usage**: Task cards, draggable items

#### 4. Cyber Input
```css
.cyber-input {
  background: slate-900/70;
  border: 1px solid slate-800;
  font-family: monospace;
  transition: all 0.2s;
}

.cyber-input:focus {
  border-color: cyan-500;
  ring: 1px cyan-500;
}
```

**Usage**: Form inputs, search bars

### Animations

**Glow Pulse**:
```css
@keyframes glow-pulse {
  0%, 100% {
    opacity: 0.8;
    box-shadow: 0 0 5px rgba(0, 240, 255, 0.6);
  }
  50% {
    opacity: 1;
    box-shadow: 0 0 10px rgba(0, 240, 255, 0.8), 
                0 0 20px rgba(0, 240, 255, 0.6);
  }
}
```

**Usage**: Data indicators, status badges, priority markers

**Node Sparkle**:
```css
@keyframes node-sparkle {
  0%, 100% { opacity: 0.8; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.02); }
}
```

**Usage**: Floating visualization nodes, attention indicators

---

## State Management

### Client-Side State

**React Hooks Pattern**:
```tsx
// Task state
const [tasks, setTasks] = useState<Task[]>([]);
const [filteredTasks, setFilteredTasks] = useState<Task[]>([]);

// UI state
const [view, setView] = useState<'list' | 'kanban'>('kanban');
const [editingTask, setEditingTask] = useState<Task | null>(null);

// Filter state
const [filters, setFilters] = useState<TaskFilters>({
  search: '',
  priority: 'all',
  status: 'all',
  category: ''
});
```

### Context API Usage

**Theme Context**:
```tsx
// contexts/ThemeContext.tsx
const ThemeContext = createContext<ThemeContextType>();

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');
  
  // Persist in localStorage
  useEffect(() => {
    const saved = localStorage.getItem('theme');
    if (saved) setTheme(saved);
  }, []);
  
  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
  };
  
  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}
```

---

## API Integration Patterns

### API Client Setup

```typescript
// lib/api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8002';

const getAuthHeaders = async () => {
  const session = await authClient.getSession();
  const userId = session?.data?.user?.id;
  
  return {
    'Content-Type': 'application/json',
    ...(userId && { 'X-User-ID': userId }),
  };
};

export const api = {
  getTasks: async () => {
    const headers = await getAuthHeaders();
    const res = await fetch(`${API_URL}/api/tasks/`, { headers });
    if (!res.ok) throw new Error('Failed to fetch tasks');
    return res.json();
  },
  
  createTask: async (data) => {
    const headers = await getAuthHeaders();
    const res = await fetch(`${API_URL}/api/tasks/`, {
      method: 'POST',
      headers,
      body: JSON.stringify(data),
    });
    return res.json();
  },
  
  // ... other methods
};
```

### Error Handling Pattern

```tsx
const fetchTasks = async () => {
  try {
    setLoading(true);
    const response = await api.getTasks();
    setTasks(response.data.tasks || []);
    setError(null);
  } catch (err: any) {
    console.error('Error fetching tasks:', err);
    setError(err.message || 'Failed to fetch tasks');
  } finally {
    setLoading(false);
  }
};
```

---

## Advanced Features

### 1. Search & Filter System

**Implementation**:
```tsx
// Debounced search
useEffect(() => {
  const timer = setTimeout(() => {
    onFilterChange({ search, priority, status, category });
  }, 300); // 300ms debounce
  
  return () => clearTimeout(timer);
}, [search, priority, status, category]);

// Local filtering
useEffect(() => {
  let result = [...tasks];
  
  if (filters.search) {
    const searchLower = filters.search.toLowerCase();
    result = result.filter(task =>
      task.title.toLowerCase().includes(searchLower) ||
      task.description?.toLowerCase().includes(searchLower)
    );
  }
  
  if (filters.priority !== 'all') {
    result = result.filter(task => task.priority === filters.priority);
  }
  
  setFilteredTasks(result);
}, [tasks, filters]);
```

### 2. Drag & Drop with dnd-kit

```tsx
import { DndContext, closestCorners } from '@dnd-kit/core';

const handleDragEnd = async (event: DragEndEvent) => {
  const { active, over } = event;
  if (!over) return;
  
  const taskId = active.id as string;
  const newStatus = over.id as string;
  
  // Update task status
  await onTaskUpdate(taskId, { status: newStatus });
};
```

### 3. Real-Time Analytics

```tsx
// Calculate metrics
const totalTasks = tasks.length;
const completionRate = totalTasks > 0 
  ? Math.round((doneTasks.length / totalTasks) * 100) 
  : 0;
  
const completedToday = doneTasks.filter(t => {
  if (!t.completed_at) return false;
  const completedDate = new Date(t.completed_at);
  return completedDate.toDateString() === new Date().toDateString();
}).length;

const overdueTasks = tasks.filter(t => {
  if (!t.due_date || t.status === 'completed') return false;
  return new Date(t.due_date) < new Date();
}).length;
```

### 4. Dark Mode Toggle

**CSS Variables Approach**:
```css
:root {
  --primary: 0 240 255;
  --background: 10 13 20;
}

[data-theme='light'] {
  --primary: 0 120 180;
  --background: 255 255 255;
}
```

**Dynamic Theme Switching**:
```tsx
const toggleTheme = () => {
  const newTheme = theme === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', newTheme);
};
```

---

## Mobile Responsiveness

### Breakpoint Strategy

```css
/* Mobile first */
.container {
  width: 100%;
}

/* Tablet */
@media (min-width: 768px) {
  .container {
    width: 768px;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    max-width: 1280px;
  }
}
```

### Mobile-Specific Patterns

**Collapsible Sidebar**:
```tsx
<div className="hidden md:block">
  <Sidebar />
</div>
```

**Responsive Grid**:
```tsx
<div className="grid grid-cols-1 md:grid-cols-4 gap-6">
  {/* Stacks on mobile, 4 columns on desktop */}
</div>
```

---

## Performance Optimization

### Code Splitting

```tsx
// Dynamic imports for heavy components
const EditTaskModal = dynamic(() => import('@/components/EditTaskModal'));
```

### Memoization

```tsx
const filteredTasks = useMemo(() => {
  return tasks.filter(/* ... */);
}, [tasks, filters]);
```

### Debouncing

```typescript
const debouncedSearch = useCallback(
  debounce((value: string) => {
    setFilters(prev => ({ ...prev, search: value }));
  }, 300),
  []
);
```

---

## Security Patterns

### Authentication

**Better Auth Integration**:
```tsx
import { useSession } from '@/lib/auth-client';

const { data: session, isPending } = useSession();

useEffect(() => {
  if (!isPending && !session) {
    router.push('/auth');
  }
}, [session, isPending]);
```

### API Request Authentication

```tsx
const getAuthHeaders = async () => {
  const session = await authClient.getSession();
  return {
    'X-User-ID': session?.data?.user?.id
  };
};
```

---

## Testing Strategies

### Component Testing

```tsx
describe('TaskCard', () => {
  it('renders task title', () => {
    render(<TaskCard task={mockTask} />);
    expect(screen.getByText(mockTask.title)).toBeInTheDocument();
  });
});
```

### API Testing

```python
def test_create_task():
    response = client.post('/api/tasks/', json={
        'title': 'Test Task',
        'priority': 'high'
    })
    assert response.status_code == 200
```

---

## Deployment Checklist

- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] Static assets optimized
- [ ] API CORS configured
- [ ] Error tracking enabled
- [ ] Analytics integrated
- [ ] Performance tested
- [ ] Security audit complete

---

## Key Learnings

1. **Component-First Design**: Build reusable UI components
2. **State Management**: Use Context for global state, hooks for local
3. **API Integration**: Centralize API calls, handle errors gracefully
4. **Theme System**: CSS variables + data attributes = flexible theming
5. **Performance**: Debounce, memo, lazy load heavy components
6. **User Experience**: Loading states, error messages, success feedback
7. **Accessibility**: Keyboard navigation, ARIA labels, color contrast

---

**Last Updated**: 2025-12-19  
**Version**: 2.0 - Production Ready  
**Status**: ✅ Complete Implementation
