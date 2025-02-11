import { defineStore } from 'pinia'
import { ref } from 'vue'

interface Group {
  id: number
  group_name: string
}

interface Word {
  id: number
  kanji: string
}

interface StudyActivity {
  id: number
  title: string
}

export const useNavigationStore = defineStore('navigation', () => {
  const currentGroup = ref<Group | null>(null)
  const currentWord = ref<Word | null>(null)
  const currentStudyActivity = ref<StudyActivity | null>(null)

  function setCurrentGroup(group: Group | null) {
    currentGroup.value = group
  }

  function setCurrentWord(word: Word | null) {
    currentWord.value = word
  }

  function setCurrentStudyActivity(activity: StudyActivity | null) {
    currentStudyActivity.value = activity
  }

  function $reset() {
    currentGroup.value = null
    currentWord.value = null
    currentStudyActivity.value = null
  }

  return {
    currentGroup,
    currentWord,
    currentStudyActivity,
    setCurrentGroup,
    setCurrentWord,
    setCurrentStudyActivity,
    $reset
  }
})
