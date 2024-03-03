import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'

import NavbarMain from '@/components/navigation/NavbarMain.vue'

describe('NavbarMain', () => {
  it('renders Navbar properly', () => {
    const wrapper = mount(NavbarMain)
    expect(wrapper.text()).toContain('Home')
    expect(wrapper.text()).toContain('Devices')
  })
})
