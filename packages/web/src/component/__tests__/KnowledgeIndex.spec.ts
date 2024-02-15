import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import CachePage from '../../page/CachePage.vue'

describe('App', () => {
  it('renders properly', () => {
    const wrapper = mount(CachePage)
    expect(wrapper.text()).toContain('Cache')
  })
})
