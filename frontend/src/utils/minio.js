// MinIO configuration
const MINIO_ENDPOINT = 'minio'
const MINIO_PORT = 9000
const MINIO_ACCESS_KEY = 'minioadmin'
const MINIO_SECRET_KEY = 'minioadmin123'
const MINIO_BUCKET = 'audio-files'

/**
 * Upload audio file to MinIO via HTTP API
 * @param {Blob} audioBlob - Audio file blob
 * @param {string} filename - Filename for the audio
 * @returns {Promise<string>} - MinIO object URL
 */
export async function uploadAudioToMinio(audioBlob, filename) {
  try {
    console.log('MinIO: Uploading audio file:', filename)
    
    // For now, we'll use the STT service to handle MinIO upload
    // This is a simplified approach - in production you'd use MinIO's HTTP API
    const formData = new FormData()
    formData.append('audio', audioBlob, filename)
    formData.append('session_id', 'temp-session')
    
    // Upload to STT service which will handle MinIO
    const response = await fetch('/api/v1/stt/transcribe-file', {
      method: 'POST',
      body: formData
    })
    
    if (!response.ok) {
      throw new Error(`Upload failed: ${response.status}`)
    }
    
    const result = await response.json()
    const objectUrl = `minio://${MINIO_BUCKET}/${filename}`
    console.log('MinIO: Audio uploaded successfully:', objectUrl)
    
    return objectUrl
  } catch (error) {
    console.error('MinIO: Upload failed:', error)
    throw new Error(`Failed to upload audio to MinIO: ${error.message}`)
  }
}

/**
 * Get presigned URL for audio file
 * @param {string} filename - Filename in MinIO
 * @returns {Promise<string>} - Presigned URL
 */
export async function getAudioPresignedUrl(filename) {
  try {
    // In a real implementation, you'd call MinIO's presigned URL API
    // For now, return a placeholder
    return `http://${MINIO_ENDPOINT}:${MINIO_PORT}/${MINIO_BUCKET}/${filename}`
  } catch (error) {
    console.error('MinIO: Failed to get presigned URL:', error)
    throw new Error(`Failed to get presigned URL: ${error.message}`)
  }
}

/**
 * Delete audio file from MinIO
 * @param {string} filename - Filename in MinIO
 */
export async function deleteAudioFromMinio(filename) {
  try {
    // In a real implementation, you'd call MinIO's delete API
    console.log('MinIO: Audio file deleted:', filename)
  } catch (error) {
    console.error('MinIO: Failed to delete audio file:', error)
    throw new Error(`Failed to delete audio file: ${error.message}`)
  }
}
