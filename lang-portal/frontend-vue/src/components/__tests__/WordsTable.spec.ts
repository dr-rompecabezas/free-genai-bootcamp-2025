import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import WordsTable from '../WordsTable.vue'
import { router } from '@/router'

const testWords = [
  {
    id: 1,
    kanji: '日',
    romaji: 'hi',
    english: 'sun',
    correct_count: 5,
    wrong_count: 2
  },
  {
    id: 2,
    kanji: '月',
    romaji: 'tsuki',
    english: 'moon',
    correct_count: 3,
    wrong_count: 1
  }
]

describe('WordsTable', () => {
  it('renders all words with correct data', () => {
    const wrapper = mount(WordsTable, {
      props: {
        words: testWords,
        sortKey: 'kanji',
        sortDirection: 'asc',
        onSort: () => {}
      },
      global: {
        plugins: [router]
      }
    })

    // Check if all words are rendered
    testWords.forEach(word => {
      expect(wrapper.text()).toContain(word.kanji)
      expect(wrapper.text()).toContain(word.romaji)
      expect(wrapper.text()).toContain(word.english)
      expect(wrapper.text()).toContain(word.correct_count.toString())
      expect(wrapper.text()).toContain(word.wrong_count.toString())
    })
  })

  it('calls onSort when header is clicked', async () => {
    const onSort = vi.fn()
    const wrapper = mount(WordsTable, {
      props: {
        words: testWords,
        sortKey: 'kanji',
        sortDirection: 'asc',
        onSort
      },
      global: {
        plugins: [router]
      }
    })

    await wrapper.find('th').trigger('click')
    expect(onSort).toHaveBeenCalledWith('kanji')
  })

  it('shows sort direction indicator', () => {
    const wrapper = mount(WordsTable, {
      props: {
        words: testWords,
        sortKey: 'kanji',
        sortDirection: 'asc',
        onSort: () => {}
      },
      global: {
        plugins: [router]
      }
    })

    expect(wrapper.find('svg').exists()).toBe(true)
  })
})
