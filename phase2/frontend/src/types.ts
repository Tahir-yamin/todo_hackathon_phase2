export interface Task {
  id: string;
  title: string;
  description?: string;
  priority: 'low' | 'medium' | 'high';
  due_date?: string;
  status: 'pending' | 'completed';
  completed_at?: string;
  created_at: string;
  updated_at: string;
  user_id: string;
  category?: string;
  tags?: string;
}

export interface TaskFormData {
  title: string;
  description?: string;
  priority: 'low' | 'medium' | 'high';
  due_date?: string;
  category?: string;
  tags?: string;
}
