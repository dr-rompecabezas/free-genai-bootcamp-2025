export interface RecentSession {
  id: number
  group_id: number
  activity_name: string
  created_at: string
  correct_count: number
  wrong_count: number
}

export interface StudyStats {
  total_vocabulary: number
  total_words_studied: number
  mastered_words: number
  success_rate: number
  total_sessions: number
  active_groups: number
  current_streak: number
}
