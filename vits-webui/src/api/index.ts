import axios from 'axios'
import type { AxiosResponse } from 'axios'

import { useUserStore } from '@/stores/user'

export enum ErrorCode {
  OK = 0,
  EmptyText = 100,
  Unknown = 199
}

export enum Dialect {
  gb = 'en-gb',
  uk = gb,
  us = 'en-us'
}

export interface TTSConfig {
  dialect?: Dialect
  slow_punctuation?: number
  noise_scale?: number
  noise_scale_w?: number
  length_scale?: number
}

export interface TTSRequest {
  config?: TTSConfig
  text: string
}

export interface MarkedSentence {
  content: string
  start_time: number
  end_time: number
  is_punctuation: boolean
}

export interface TTSResponseData {
  marked_sentences: Array<MarkedSentence>
  voice: string
}

export interface APIResponse<T> {
  code: ErrorCode
  msg?: string
  data?: T
}

export interface UserLoginRequest {
  name: string
  password: string
}

export interface UserLoginResponseData {
  token: string
}

const BASE_URL = ''

export function postTTSRequest(
  data: TTSRequest
): Promise<AxiosResponse<APIResponse<TTSResponseData>>> {
  const userStore = useUserStore()
  return axios.post(BASE_URL + '/tts/syn', data, {
    headers: { Authorization: 'Bearer ' + userStore.token }
  })
}

export function postUserLoginRequest(
  data: UserLoginRequest
): Promise<AxiosResponse<APIResponse<UserLoginResponseData>>> {
  return axios.post(BASE_URL + '/tts/login', data)
}
