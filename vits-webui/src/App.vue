<template lang="pug">
div(ref='app')
  template(
    v-if="!userStore.needLogin"
  )
    NavBar(
      title='语音合成系统'
    )
    HomeView
  Dialog(
    v-model:show="userStore.needLogin"
    title='登录系统'
    :showConfirmButton="false"
  )
    Form(
      @submit="handleLogin"
    )
      div(style='height: 16px')
      CellGroup
        Space(
          direction='vertical'
        )
          Field(
            v-model='userNameInput'
            required
            label='用户名'
            placeholder="请输入用户名"
            :rules="[{ required: true, message: '请输入用户名' }]"
          )
          Field(
            v-model='userPasswordInput'
            required
            label='密码'
            type="password"
            placeholder="请输入密码"
            :rules="[{ required: true, message: '请输入密码' }]"
          )
          Cell
            Button(
              round
              block 
              type='primary'
              native-type='submit'
            ) 登录
</template>

<script setup lang="ts">
import { ref } from 'vue'

import HomeView from './views/HomeView.vue'
import { NavBar, Button, Dialog, Cell, CellGroup, Space, Form, Field } from 'vant'

import { useUserStore } from '@/stores/user'
const userStore = useUserStore()

const userNameInput = ref('')
const userPasswordInput = ref('')

const handleLogin = async () => {
  await userStore.login!(userNameInput.value, userPasswordInput.value)
}
</script>

<style>
html {
  height: 100%;
  background-color: white;
}
#app {
  height: 100vh;
  width: 100vw;
  display: block;
  margin: 0;
  padding: 0;
  background-color: white;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
