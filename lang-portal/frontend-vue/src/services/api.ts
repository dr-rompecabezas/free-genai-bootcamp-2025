import axios from 'axios'
import type { RecentSession, StudyStats } from '@/types'

const API_BASE_URL = 'http://localhost:5000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export interface Word {
  id: number
  kanji: string
  romaji: string
  english: string
  correct_count: number
  wrong_count: number
}

export interface StudySession {
  id: number
  activity_id: number
  activity_name: string
  group_id: number
  group_name: string
  start_time: string
  end_time: string
  review_items_count: number
}

export interface PaginatedResponse<T> {
  items: T[]
  total_pages: number
}

export async function fetchRecentStudySession(): Promise<RecentSession | null> {
  try {
    const response = await api.get('/api/v1/dashboard/recent-session')
    return response.data
  } catch (error) {
    console.error('Error fetching recent study session:', error)
    throw error
  }
}

export async function fetchStudyStats(): Promise<StudyStats> {
  try {
    const response = await api.get('/api/v1/dashboard/stats')
    return response.data
  } catch (error) {
    console.error('Error fetching study stats:', error)
    throw error
  }
}

export async function fetchWords(
  page: number,
  sortKey: string,
  sortDirection: 'asc' | 'desc'
): Promise<PaginatedResponse<Word>> {
  try {
    const response = await api.get('/api/v1/words', {
      params: {
        page,
        sort_key: sortKey,
        sort_direction: sortDirection
      }
    })
    return response.data
  } catch (error) {
    console.error('Error fetching words:', error)
    throw error
  }
}

export async function fetchStudySessions(
  page: number,
  itemsPerPage: number
): Promise<PaginatedResponse<StudySession>> {
  try {
    const response = await api.get('/api/v1/study-sessions', {
      params: {
        page,
        items_per_page: itemsPerPage
      }
    })
    return response.data
  } catch (error) {
    console.error('Error fetching study sessions:', error)
    throw error
  }
}
