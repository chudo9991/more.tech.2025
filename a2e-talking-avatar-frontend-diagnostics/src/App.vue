<template>
  <main class="container">
    <h1>A2E Talking Avatar — Pure Frontend</h1>
    <p class="muted">
      Тестовый режим: браузер шлёт запросы в A2E API напрямую. Токен хранится на клиенте — только для локального теста.
    </p>

    <!-- 0) Настройки -->
    <section class="card">
      <h2>0) Настройки соединения</h2>
      <div class="row">
        <label>API Base
          <input v-model="apiBase" placeholder="https://video.a2e.ai" />
        </label>
        <label>Bearer Token
          <input v-model="token" placeholder="вставьте A2E_TOKEN" />
        </label>
        <label><input type="checkbox" v-model="remember" /> запомнить</label>
        <button @click="saveSettings">Сохранить</button>
      </div>
    </section>

    <!-- 1) Аватар -->
    <section class="card">
      <h2>1) Аватар</h2>
      <p class="muted">Используется готовый аватар ID: <code>68af59a86eeedd0042ca7e27</code></p>
      <div class="preview">
        <img src="https://d1tzkvq5ukphug.cloudfront.net/adam2eve/stable/video_twin/63076d83-d345-4caa-be8a-19fc7c9338c8.png" alt="avatar preview" style="max-width: 200px;" />
      </div>
    </section>

    <!-- 2) Голоса и TTS -->
    <section class="card">
      <h2>2) Голоса (ru-RU) и TTS</h2>
      <div class="row">
        <button :disabled="loadingVoices" @click="loadVoices">{{ loadingVoices ? 'Загрузка голосов…' : 'Загрузить голоса' }}</button>
        <span v-if="voices.length" class="muted">Найдено: {{ voices.length }}</span>
        <span v-else-if="!loadingVoices" class="muted">Нет элементов</span>

        <label v-if="voices.length">Голос
          <select v-model="ttsId">
            <option v-for="v in voices" :key="v.id" :value="v.id">
              {{ v.name }} — {{ v.gender }}
            </option>
          </select>
        </label>
        <label v-else>tts_id <input v-model="ttsId" placeholder="например ru_RU_001" /></label>

        <label>speechRate <input type="number" step="0.1" v-model.number="speechRate" /></label>
      </div>

      <textarea v-model="text" rows="4" placeholder="Введите русскую реплику…"></textarea>
      <button :disabled="!text || ttsing" @click="makeTTS">{{ ttsing ? 'Синтез…' : 'Синтезировать речь' }}</button>
      <p v-if="audioSrc"><b>audioSrc:</b> <code>{{ audioSrc }}</code></p>
      <audio v-if="audioSrc" :src="audioSrc" controls></audio>
    </section>

    <!-- 3) Видео -->
    <section class="card">
      <h2>3) Видео</h2>
      <div class="row">
        <label>resolution
          <select v-model.number="resolution">
            <option :value="720">720</option>
            <option :value="1080">1080</option>
          </select>
        </label>
      </div>
      <p class="muted">debug: anchorId={{ String(anchorId) }} · anchorType={{ Number(anchorType) }} · audioSrc={{ audioSrc ? 'yes' : 'no' }} · generating={{ generating }}</p>
      <button :disabled="generating || !audioSrc || !String(anchorId)" @click="generateVideo">{{ generating ? 'Генерация…' : 'Сгенерировать видео' }}</button>
      <p v-if="videoTaskId"><b>task_id:</b> <code>{{ videoTaskId }}</code></p>
      <button v-if="videoTaskId" :disabled="checkingVideo" @click="checkVideo">Проверить статус видео</button>
      <div v-if="videoUrl" class="preview"><video :src="videoUrl" controls playsinline></video></div>
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// settings
const apiBase = ref('https://video.a2e.ai')
const token = ref('')
const remember = ref(true)

// avatar (fixed)
const anchorId = ref('68af59a86eeedd0042ca7e27')
const anchorType = ref(1) // 1 = user twin

// voices
const voices = ref([])
const loadingVoices = ref(false)
const text = ref('')
const ttsId = ref('')
const speechRate = ref(1.0)
const audioSrc = ref('')
const ttsing = ref(false)

// video
const resolution = ref(1080)
const generating = ref(false)
const checkingVideo = ref(false)
const videoTaskId = ref('')
const videoUrl = ref('')

onMounted(() => {
  const saved = localStorage.getItem('a2e_front_settings')
  if (saved) {
    try {
      const j = JSON.parse(saved)
      apiBase.value = j.apiBase || apiBase.value
      token.value = j.token || ''
      remember.value = !!j.remember
    } catch {}
  }
})

function saveSettings() {
  if (remember.value) {
    localStorage.setItem('a2e_front_settings', JSON.stringify({
      apiBase: apiBase.value, token: token.value, remember: true
    }))
  } else {
    localStorage.removeItem('a2e_front_settings')
  }
  alert('Сохранено')
}

function authHeaders(json = true) {
  const h = { Authorization: `Bearer ${token.value}` }
  if (json) h['Content-Type'] = 'application/json'
  return h
}

async function loadVoices() {
  loadingVoices.value = true
  try {
    const qs = new URLSearchParams({ country: 'ru', region: 'RU', voice_map_type: 'ru-RU' })
    const r = await fetch(`${apiBase.value}/api/v1/anchor/voice_list?${qs.toString()}`, {
      method: 'GET',
      headers: { Authorization: `Bearer ${token.value}` }
    })
    const j = await r.json()
    if (!r.ok) throw new Error(j?.msg || 'voice_list failed')

    const groups = Array.isArray(j?.data) ? j.data : []
    const flat = []
    for (const g of groups) {
      for (const v of (g.children || [])) {
        flat.push({ id: v.value, name: v.label, gender: g.value, lang: 'ru-RU' })
      }
    }
    voices.value = flat
    if (!ttsId.value && voices.value.length) ttsId.value = voices.value[0].id
  } catch (e) {
    alert('Не удалось загрузить голоса: ' + e.message)
  } finally {
    loadingVoices.value = false
  }
}

async function makeTTS() {
  ttsing.value = true
  try {
    const r = await fetch(`${apiBase.value}/api/v1/video/send_tts`, {
      method: 'POST',
      headers: authHeaders(true),
      body: JSON.stringify({
        msg: text.value,
        tts_id: ttsId.value,
        speechRate: speechRate.value,
        country: 'ru',
        region: 'RU'
      })
    })
    const j = await r.json()
    if (!r.ok) throw new Error(j?.msg || 'tts failed')
    audioSrc.value = j?.data || ''
  } catch (e) {
    alert('TTS failed: ' + e.message)
  } finally {
    ttsing.value = false
  }
}

async function generateVideo() {
  console.log('[generate] anchorId', anchorId.value, 'anchorType', anchorType.value)
  if (!anchorId.value || !audioSrc.value) return alert('Нужны anchor_id и audioSrc.')
  generating.value = true
  try {
    let r = await fetch(`${apiBase.value}/api/v1/video/generate`, {
      method: 'POST',
      headers: authHeaders(true),
      body: JSON.stringify({
        title: `demo-${Date.now()}`,
        anchor_id: anchorId.value,
        anchor_type: Number(anchorType.value),
        audioSrc: audioSrc.value,
        resolution: resolution.value,
        isCaptionEnabled: false
      })
    })
    let j = await r.json()
    if (!r.ok) {
      // Try alternative param name for audio: audio_url
      console.warn('[generate] first attempt failed, trying audio_url', j)
      r = await fetch(`${apiBase.value}/api/v1/video/generate`, {
        method: 'POST', 
        headers: authHeaders(true),
        body: JSON.stringify({ 
          title: `demo-${Date.now()}`, 
          anchor_id: String(anchorId.value), 
          anchor_type: Number(anchorType.value), 
          audio_url: audioSrc.value, 
          resolution: resolution.value, 
          isCaptionEnabled: false 
        })
      })
      j = await r.json()
      if (!r.ok) {
        throw new Error(j?.msg || 'generate failed')
      }
    }
    videoTaskId.value = j?.data?._id || ''
    console.log('Video generation started, task_id:', videoTaskId.value)
  } catch (e) {
    console.error('Generate failed:', e)
    alert('Generate failed: ' + e.message)
  } finally {
    generating.value = false
  }
}

async function checkVideo() {
  checkingVideo.value = true
  try {
    const r = await fetch(`${apiBase.value}/api/v1/video/awsResult`, {
      method: 'POST',
      headers: authHeaders(true),
      body: JSON.stringify({ _id: videoTaskId.value })
    })
    const j = await r.json()
    console.log('Video status check:', j)
    if (!r.ok) throw new Error(j?.msg || 'awsResult failed')
    const item = j?.data?.[0]
    if (item?.status === 'success') {
      videoUrl.value = item?.result
      alert('Видео готово!')
    } else if (item?.status === 'failed') {
      alert('Генерация видео не удалась: ' + (item?.error || 'неизвестная ошибка'))
    } else {
      console.log('Video still processing, status:', item?.status)
    }
  } catch (e) {
    console.error('Video status failed:', e)
    alert('Video status failed: ' + e.message)
  } finally {
    checkingVideo.value = false
  }
}
</script>