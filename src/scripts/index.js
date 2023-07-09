/* eslint-disable array-callback-return */
/* eslint-disable no-eval */
/* eslint-disable no-unexpected-multiline */
/* eslint-disable func-call-spacing */
/* eslint-disable no-undef */
import '../styles/index.css'
import '../styles/responsive.css'
import swRegister from './utils/sw-register'

window.addEventListener('load', () => {
  swRegister()
})

const map = L.map('map', {
  attributionControl: false
}).setView([-2.5489, 118.0149], 5)

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: false,
  maxZoom: 18
}).addTo(map)

// Fungsi untuk mengambil data koordinat polygon dari API dan menampilkan pada peta
async function getPolygonFromAPI () {
  try {
    const response = await fetch('https://kkp-chatbot-test.azurewebsites.net/')
    const data = await response.json()

    if (Array.isArray(data)) {
      data.forEach((item) => {
        if (item.polygon) {
          try {
            // Memformat string polygon dan mengubahnya menjadi array koordinat
            const formattedPolygon = item.polygon
              .replace(/\s/g, '') // Menghapus spasi
              .split('],[') // Memisahkan setiap koordinat menjadi array terpisah
              .map((coord) => {
                const [lat, lng] = coord
                  .replace('[', '')
                  .replace(']', '')
                  .split(',')
                  .map(parseFloat) // Memisahkan latitude dan longitude, lalu mengubahnya menjadi angka
                if (!isNaN(lat) && !isNaN(lng)) {
                  return [lat, lng]
                }
              })

            const validPolygon = formattedPolygon.filter((coord) => coord)

            if (validPolygon.length >= 3) {
              // Menambahkan polygon ke peta
              const polygon = L.polygon(validPolygon, { color: 'red' }).addTo(map)

              polygon.on('mouseover', function (e) {
                // Memfilter item-data yang memiliki polygon yang sesuai dengan polygon yang sedang di-hover
                const matchingItems = data.filter((item) => {
                  const itemPolygon = item.polygon
                    .replace(/\s/g, '')
                    .split('],[')
                    .map((coord) => {
                      const [lat, lng] = coord
                        .replace('[', '')
                        .replace(']', '')
                        .split(',')
                        .map(parseFloat)
                      return [lat, lng]
                    })

                  return matchingPolygons(validPolygon, itemPolygon)
                })

                // Menampilkan data SIGMET yang sesuai pada popup
                matchingItems.forEach((matchingItem) => {
                  if (matchingItem.sigmet) {
                    this.bindPopup(matchingItem.sigmet).openPopup()
                  }
                })
              })
            }
          } catch (error) {
            console.error('Error parsing polygon data:', error)
          }
        }
      })
    }
  } catch (error) {
    console.error('Error fetching polygon data:', error)
  }
}

// Fungsi untuk memeriksa apakah dua polygon cocok/match
function matchingPolygons (polygon1, polygon2) {
  if (polygon1.length !== polygon2.length) {
    return false
  }

  for (let i = 0; i < polygon1.length; i++) {
    const [lat1, lon1] = polygon1[i]
    const [lat2, lon2] = polygon2[i]

    if (Math.abs(lat1 - lat2) > 0.01 || Math.abs(lon1 - lon2) > 0.01) {
      return false
    }
  }

  return true
}

// Panggil fungsi getPolygonFromAPI untuk menampilkan semua polygon dari API
getPolygonFromAPI()

const chatButton = document.getElementById('chat-button')
const chatPopup = document.getElementById('chat-popup')
const closeButton = document.getElementById('close-button')
const chatForm = document.getElementById('chat-form')
const promptInput = document.getElementById('prompt')
const chatContainer = document.getElementById('chat-container')
const blurPageNav = document.querySelector('.navbar')
const blurPageMap = document.getElementById('map')
const blurPageKompas = document.getElementById('kompas')
const blurFooter = document.querySelector('footer')
const initialMessage = 'Hai, apa yang ingin kamu ketahui tentang kondisi SIGMET ?'
addChatBubble(initialMessage, 'bot')

chatPopup.style.display = 'none'

chatButton.addEventListener('click', function () {
  chatPopup.style.display = 'block'
})

closeButton.addEventListener('click', function () {
  chatPopup.style.display = 'none'
})

chatButton.addEventListener('click', () => {
  blurPageNav.classList.add('blur')
})

closeButton.addEventListener('click', () => {
  blurPageNav.classList.remove('blur')
})

chatButton.addEventListener('click', () => {
  blurPageMap.classList.add('blur')
})

closeButton.addEventListener('click', () => {
  blurPageMap.classList.remove('blur')
})

chatButton.addEventListener('click', () => {
  blurPageKompas.classList.add('blur')
})

closeButton.addEventListener('click', () => {
  blurPageKompas.classList.remove('blur')
})

chatButton.addEventListener('click', () => {
  blurFooter.classList.add('blur')
})

closeButton.addEventListener('click', () => {
  blurFooter.classList.remove('blur')
})

function addChatBubble (message, sender, isLoading = false) {
  // Hapus semua pesan loading sebelum menampilkan hasil dari bot
  const loadingBubbles = chatContainer.querySelectorAll('.chat-bubble.loading')
  loadingBubbles.forEach((bubble) => {
    chatContainer.removeChild(bubble)
  })

  const chatBubble = document.createElement('div')
  chatBubble.classList.add('chat-bubble')

  if (isLoading) {
    chatBubble.classList.add('loading')
  }

  if (sender === 'user') {
    chatBubble.classList.add('user-chat')
  } else {
    chatBubble.classList.add('bot-chat')
  }

  if (!isLoading && sender === 'bot') {
    const lines = message.split('\n')
    lines.forEach((line) => {
      const chatBubbleLine = document.createElement('div')
      chatBubbleLine.textContent = line
      chatBubble.appendChild(chatBubbleLine)
    })
  } else {
    const chatText = document.createElement('span')
    chatText.textContent = message
    chatBubble.appendChild(chatText)
  }

  chatContainer.appendChild(chatBubble)

  // Scroll otomatis ke bagian bawah chat history
  chatContainer.scrollTop = chatContainer.scrollHeight
}

function scrollToTop () {
  document.body.scrollTop = 0
  document.documentElement.scrollTop = 0
}

window.scrollToTop = scrollToTop

function showLoadingAnimation () {
  const loadingText = ''
  addChatBubble(loadingText, 'bot', true)
}

function removeLoadingAnimation () {
  const loadingBubble = chatContainer.querySelector('.chat-bubble.loading')
  if (loadingBubble) {
    chatContainer.removeChild(loadingBubble)
  }
}

function formatBotResponse (data) {
  let formattedResponse = ''
  for (const key in data) {
    const formattedKey = key.replaceAll('_', ' ')
    let formattedValue = data[key]

    // Special formatting for key
    if (key === 'data polygon') {
      formattedValue = formattedValue.replaceAll(' - ', '\n')
    }

    if (key === 'polygon ') {
      formattedValue = formattedValue.replaceAll(' - ', '\n')
    }

    formattedResponse += `${formattedKey}: ${formattedValue}\n`
  }
  return formattedResponse
}

chatButton.addEventListener('click', function () {
  chatButton.classList.add('hidden') // Sembunyikan tombol chatbot
  chatPopup.classList.add('active')
})

closeButton.addEventListener('click', function () {
  chatButton.classList.remove('hidden') // Tampilkan kembali tombol chatbot
  chatPopup.classList.remove('active')
})

async function getBotResponse (message) {
  const apiUrl = `
  https://sigmet-chatbot.azurewebsites.net/chat?question=${encodeURIComponent(message)}
  `

  try {
    showLoadingAnimation() // Menampilkan animasi "..." saat loading

    const response = await fetch(apiUrl)
    const data = await response.json()

    removeLoadingAnimation()

    if (Array.isArray(data)) {
      // Jika data adalah array, itu berarti respons berisi banyak hasil
      data.forEach((result) => {
        const botResponse = formatBotResponse(result)
        addChatBubble(botResponse, 'bot')
      })
    } else if (data.answer) {
      // Jika data adalah objek dengan key 'answer', itu berarti respons hanya satu hasil
      const botResponse = formatBotResponse(data)
      addChatBubble(botResponse, 'bot')
    } else {
      // Jika data tidak ada
      addChatBubble('Data yang anda input tidak dapat diproses', 'bot')
    }
  } catch (error) {
    console.error('Error fetching bot response:', error)
    addChatBubble('Error: Format yang dimasukkan salah!', 'bot')
  }
}

chatForm.addEventListener('submit', function (event) {
  event.preventDefault()

  const userMessage = promptInput.value
  addChatBubble('You: ' + userMessage, 'user')

  getBotResponse(userMessage) // Memanggil fungsi getBotResponse untuk mendapatkan respons dari API

  promptInput.value = ''
})
