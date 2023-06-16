<template lang="pug">
CellGroup(
  title='语音合成输入'
)
  Form(
    @submit="handleSyn"
  )
    Collapse(
      v-model="collapseTTSConfig"
      accordion
    )
      CollapseItem(
          title='文本输入'
        )
        Field(
          v-model='textInput'
          rows='5'
          autosize
          label='文本'
          type='textarea'
          maxlength='1024'
          show-word-limit
          required
          placeholder="请输入英文文本"
          :rules="[{ required: true, message: '请输入英文文本' }]"
          
        )
      CollapseItem(
        title='合成选项'
      )
        RadioGroup(
          v-model='dialect'
        )
          CellGroup(
            inset
            title='口音'
          )
            Cell(title='英式英语' clickable @click="dialect = Dialect.gb")
              template(#right-icon)
                Radio(name='en-gb')
            Cell(title='美式英语' clickable @click="dialect = Dialect.us")
              template(#right-icon)
                Radio(name='en-us')
        CellGroup(
          inset
          title='速度'
        )
          Cell(title='朗读速度')
            Stepper(
              v-model="speed"
              min='0.1'
              max='5.0'
              step='0.1'
              :decimal-length='1'
            )
        CellGroup(
          inset
          title='模型选项'
        )
          Cell(title='模型噪声')
            Stepper(
              v-model="noise"
              min='0.0'
              max='1.0'
              step='0.1'
              :decimal-length='1'
            )
          Cell(title='时长噪声')
            Stepper(
              v-model="noiseW"
              min='0.0'
              max='1.0'
              step='0.1'
              :decimal-length='1'
            )
          Cell(title='标点停顿长度')
            Stepper(
              v-model="slowPunctuation"
              min='0.0'
              max='10.0'
              step='0.5'
              :decimal-length='1'
            )
    Cell(
      center
    )
      Button(
        type='primary'
        block
        size='normal'
        :loading='isLoading'
        native-type='submit'
      ) 合成语音
CellGroup(
  v-if="sentences.length > 0"
  title='语音合成结果'
)
  SentencePlayer(
    ref='sentencePlayer'
    :sentences='sentences'
    :voiceb64='voiceb64'
  )
</template>

<script setup lang="ts">
import {
  Collapse,
  CollapseItem,
  Stepper,
  CellGroup,
  Cell,
  Form,
  Field,
  Button,
  RadioGroup,
  Radio,
  showFailToast,
  showLoadingToast,
  showSuccessToast,
  closeToast
} from 'vant'
import { ref } from 'vue'
import { Dialect } from '@/api'
import type { MarkedSentence } from '@/api'
import { postTTSRequest } from '@/api'
import SentencePlayer from '@/components/SentencePlayer.vue'
const sentencePlayer = ref<typeof SentencePlayer | null>(null)

import { useUserStore } from '@/stores/user'
const userStore = useUserStore()

const collapseTTSConfig = ref(0)
const isLoading = ref<boolean>(false)

const textInput = ref('')
const dialect = ref<Dialect>('en-us' as Dialect)
const speed = ref<number>(1.0)
const noise = ref<number>(0.0)
const noiseW = ref<number>(0.0)
const slowPunctuation = ref<number>(2.0)

const sentences = ref<Array<MarkedSentence>>([])
const voiceb64 = ref<String>('')

async function handleSyn() {
  sentences.value = []
  voiceb64.value = ''
  isLoading.value = true
  const loadingToast = showLoadingToast({
    message: '合成中...',
    forbidClick: true
  })

  const ret = await postTTSRequest({
    text: textInput.value,
    config: {
      dialect: dialect.value,
      length_scale: 1.0 / speed.value,
      noise_scale: noise.value,
      noise_scale_w: noiseW.value,
      slow_punctuation: slowPunctuation.value / speed.value
    }
  })

  isLoading.value = false
  closeToast()
  if (ret.status != 200) {
    showFailToast('服务器返回错误, ' + ret.status + ', ' + ret.statusText)
  }

  const response = ret.data
  console.log(response)
  if (response.code == 0) {
    console.log('response.data!.marked_sentences', response.data)
    showSuccessToast({ message: '合成成功', duration: 1.5 })
    sentences.value = response.data!.marked_sentences
    voiceb64.value = response.data!.voice
    collapseTTSConfig.value = -1
  } else if (response.code == 100) {
    userStore.logout()
  } else {
    showFailToast('服务器返回错误, ' + response.msg)
  }
}
</script>
