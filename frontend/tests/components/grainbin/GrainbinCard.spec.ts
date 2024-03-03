import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'

import GrainbinCard from '@/components/grainbin/GrainbinCard.vue'
import { type Grainbin } from '@/interfaces/grainbin.interface'

const grainbin: Grainbin = {
  id: 1,
  name: 'Grainbin 1',
  lastUpdated: new Date(),
  averageTemp: '0',
  userConfigured: false,
  busNumber: 0,
  device: 0,
  sensorType: 'temperature',
  totalUpdates: 0,
  description: 'new grainbin',
  url: '/grainbin/1/',
  busNumberString: '0',
  grainbinType: 'temperature'
}

describe('GrainbinCard', () => {
  it('renders properly', () => {
    const wrapper = mount(GrainbinCard, {
      props: {
        grainbin: grainbin
      }
    })
    expect(wrapper.text()).toContain('Grainbin 1')
    expect(wrapper.find('div.card-footer').text()).toContain('Last Update:')
  })
})
