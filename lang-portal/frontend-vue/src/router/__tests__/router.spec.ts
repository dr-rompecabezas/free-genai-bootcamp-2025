import { describe, it, expect } from 'vitest'
import { router } from '../index'

describe('Router', () => {
  it('redirects root to dashboard', () => {
    const route = router.resolve('/')
    expect(route.matched[0].redirect).toEqual({ path: '/dashboard', replace: true })
    expect(route.path).toBe('/')
  })

  it('has all required routes', () => {
    const routes = [
      '/dashboard',
      '/study-activities',
      '/study-activities/1',
      '/study-activities/1/launch',
      '/words',
      '/words/1',
      '/groups',
      '/groups/1',
      '/sessions',
      '/sessions/1',
      '/settings'
    ]

    routes.forEach(path => {
      const route = router.resolve(path)
      expect(route.matched.length).toBeGreaterThan(0)
      expect(route.path).toBe(path)
    })
  })

  it('handles invalid routes', () => {
    const route = router.resolve('/invalid-path')
    expect(route.matched.length).toBe(0)
  })
})
