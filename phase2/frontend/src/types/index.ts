export interface Task {
  id: string;
  title: string;
  description?: string | null;
  priority: 'low' | 'medium' | 'high';
  due_date?: string | null;
  status: 'todo' | 'in_progress' | 'completed';
  category?: string | null;
  tags?: string | null;
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
}
