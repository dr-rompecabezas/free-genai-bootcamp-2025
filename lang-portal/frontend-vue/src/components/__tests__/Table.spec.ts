import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Table from '../Table.vue'
import TableHeader from '../TableHeader.vue'
import TableRow from '../TableRow.vue'
import TableCell from '../TableCell.vue'

describe('Table Components', () => {
  it('renders table with header and rows', () => {
    const wrapper = mount(Table, {
      slots: {
        default: `
          <thead>
            <tr>
              <th>Name</th>
              <th>Age</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>John</td>
              <td>25</td>
            </tr>
          </tbody>
        `
      }
    })

    expect(wrapper.find('table').exists()).toBe(true)
    expect(wrapper.find('thead').exists()).toBe(true)
    expect(wrapper.find('tbody').exists()).toBe(true)
  })

  it('renders sortable header with correct classes', async () => {
    const wrapper = mount(TableHeader, {
      props: {
        sortKey: 'name',
        currentSortKey: 'name',
        sortDirection: 'asc',
        onClick: () => {}
      },
      slots: {
        default: 'Name'
      }
    })

    expect(wrapper.classes()).toContain('cursor-pointer')
    expect(wrapper.find('svg').exists()).toBe(true)
  })

  it('renders row with hover effect', () => {
    const wrapper = mount(TableRow, {
      slots: {
        default: `
          <td>John</td>
          <td>25</td>
        `
      }
    })

    expect(wrapper.classes()).toContain('hover:bg-gray-50')
  })

  it('renders cell with correct padding', () => {
    const wrapper = mount(TableCell, {
      slots: {
        default: 'Content'
      }
    })

    expect(wrapper.classes()).toContain('px-6')
    expect(wrapper.classes()).toContain('py-4')
  })
})
