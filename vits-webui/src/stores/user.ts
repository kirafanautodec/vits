import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

import { showFailToast, showSuccessToast } from 'vant'

import { postUserLoginRequest } from '@/api'
import md5 from 'md5'

export const useUserStore = defineStore('user', () => {
  const token = ref('')
  const token_storage = localStorage.getItem('token')
  if (token_storage && token_storage.length > 0) {
    token.value = token_storage
  }

  const needLogin = computed(() => {
    return token.value == ''
  })

  async function login(name_value: string, password_value: string): Promise<boolean> {
    const SALT = 'VITS_SYSTEM_SALT'
    const password_md5 = md5(SALT + password_value + SALT)

    const ret = await postUserLoginRequest({ name: name_value, password: password_md5 })
    if (ret.status != 200) {
      showFailToast('登陆失败, 服务器返回' + ret.status + ', ' + ret.statusText)
      token.value = ''
      localStorage.setItem('token', token.value)
      return false
    } else if (ret.data.code != 0) {
      showFailToast('登陆失败, ' + ret.data.msg)
      token.value = ''
      localStorage.setItem('token', token.value)
      return false
    } else {
      showSuccessToast('登录成功')
      token.value = ret.data.data!.token
      localStorage.setItem('token', token.value)
      return true
    }
  }

  function logout() {
    token.value = ''
    localStorage.setItem('token', token.value)
  }

  return { token, needLogin, login, logout }
})
