<script setup lang="ts">
import { Collapse, CollapseItem, CellGroup, Cell, Form, Field, Button } from 'vant'
import { ref } from 'vue'
import type { MarkedSentence, TTSResponse } from '@/api'
import { postTTSRequest } from '@/api'

import SentencePlayer from '@/components/SentencePlayer.vue'

const isCollapseTTSConfig = ref('0')
const textInput = ref('This is a very simple sample text! Hello, every body, My name is John. Today I am very glad to introduce our brand new product.')
const sentences = ref<Array<MarkedSentence>>([])
const voiceb64 = ref<String>('')

async function handleClickButtonPostTTS() {
  console.log('handleClickButtonPostTTS')
  const ret = await postTTSRequest({ text: textInput.value })
  if (ret.status != 200) {
    return
  }

  const response: TTSResponse = ret.data
  if (response.code == 0) {
    console.log('response.data!.marked_sentences', response.data)
    sentences.value = response.data!.marked_sentences
    voiceb64.value = response.data!.voice
  }
}
</script>

<template lang="pug">
CellGroup(
  title='语音合成输入'
)
  Collapse(
    v-model='isCollapseTTSConfig'
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
      )
    CollapseItem(
      title='asdas'
    )
      Cell(title='asdasda')
      Cell(title='asasdaqasddasda')
  Cell(
    center
  )
    Button(
      type='primary'
      block
      size='normal'
      @click='handleClickButtonPostTTS'
    ) 合成
CellGroup(
  title='语音合成结果'
)
  SentencePlayer(
    :sentences='sentences'
    :voiceb64='voiceb64'
  )
</template>
