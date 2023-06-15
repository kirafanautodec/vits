import axios from 'axios'

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
    dialect?: Dialect,
    slow_punctuation?: number,
    noise_scale?: number,
    noise_scale_w?: number,
    length_scale?: number
}

export interface TTSRequest {
    config?: TTSConfig,
    text: string
}

export interface MarkedSentence {
    content: string,
    start_time: number,
    end_time: number,
    is_punctuation: boolean
}

export interface TTSResponseData {
    marked_sentences: Array<MarkedSentence>,
    voice: string
}

export interface TTSResponse {
    code: ErrorCode,
    msg?: string
    data?: TTSResponseData
}

const BASE_URL = 'http://192.168.0.112:12001/tts'

export function postTTSRequest(data: TTSRequest): Promise<TTSResponse> {
    return axios.post(
        BASE_URL,
        data
    )
}
