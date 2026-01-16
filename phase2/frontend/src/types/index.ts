export interface Task {
  id: string;
  title: string;
  description?: string | null;
  priority: 'low' | 'medium' | 'high';
  due_date?: string | null;
  status: 'todo' | 'in_progress' | 'completed';
  category?: string | null;
  tags?: string | null;
  recurrence?: 'NONE' | 'DAILY' | 'WEEKLY' | 'MONTHLY' | 'YEARLY';  // Phase 5
  next_occurrence?: string | null;  // Phase 5
  user_id: string;
  completed_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface TaskFormData {
  title: string;
  description?: string;
  priority: string;
  due_date?: string;
  status?: string;
  category?: string;
  tags?: string;
  recurrence?: string;  // Phase 5
}

// Force rebuild - 2026-01-16
