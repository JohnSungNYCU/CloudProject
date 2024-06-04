import { mount } from '@vue/test-utils'
import Login from '@/components/index.vue'

describe('index.vue', () => {
    it('emits an event with user data when login is successful', async () => {
        const wrapper = mount(Login)
        const inputUsername = wrapper.find('input[type="text"]')
        const inputPassword = wrapper.find('input[type="password"]')
        await inputUsername.setValue('admin')
        await inputPassword.setValue('123456')
        await wrapper.find('form').trigger('submit.prevent')
        expect(wrapper.emits()).toHaveProperty('login-success')
    })
})



