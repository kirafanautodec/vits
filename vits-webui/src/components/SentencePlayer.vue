<template lang="pug">
Cell
    template(v-slot='value')
        span.marked-sentence(
            v-for='sentence in props.sentences'
        ) {{ sentence.content }}
</template>

<script setup lang="ts">
import { Cell } from 'vant'
import type { MarkedSentence } from '@/api'

const props = defineProps({ sentences: Array<MarkedSentence> })
</script>
