<template lang="pug">
Cell
  div#lyric-warpper
    span.marked-sentence(
      v-for='(sentence, index) in props.sentences'
      :key='index'
      v-bind:class='{ "bold-lyric": lyricIndex == index && !sentence.is_punctuation }'
      @click='handleClickLyric(index)'
      v-html='rawHtml(sentence.content)'
    )
Cell
  AudioPlayer(
    ref='audioPlayer'
    :option='getAPOption'
    @playing='handleUpdate'
  )
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { Cell } from 'vant'
import type { MarkedSentence } from '@/api'
import AudioPlayer from 'vue3-audio-player'
import 'vue3-audio-player/dist/style.css'

const props = defineProps({ sentences: Array<MarkedSentence>, voiceb64: String })
const audioPlayer = ref<typeof AudioPlayer>(null)
const lyricIndex = ref<number>(-1)

const getAPOption = computed(() => {
  return {
    src: 'data:audio/mpeg;base64,' + props.voiceb64
  }
})

const reset = () => {
  lyricIndex.value = -1
}

const handleUpdate = () => {
  let i = 0
  if (props.sentences == undefined) {
    lyricIndex.value = -1
    return
  }
  for (
    ;
    i < props.sentences.length && audioPlayer.value.currentTime > props.sentences[i].end_time;
    ++i
  );
  if (lyricIndex.value != i) {
    lyricIndex.value = i
  }
}

const handleClickLyric = (index: number) => {
  if (props.sentences == undefined) {
    return
  }
  audioPlayer.value.play()
  audioPlayer.value.audioPlayer.currentTime = props.sentences[index].start_time - 0.1
}

const rawHtml = (content: string) => {
  return content.replaceAll('\n', '<br/>')
}
</script>

<style>
.bold-lyric {
  color: black;
}

#lyric-warpper {
  text-align: left;
  font-size: 130%;
}
</style>
