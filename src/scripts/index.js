/* eslint-disable no-unexpected-multiline */
/* eslint-disable func-call-spacing */
/* eslint-disable no-undef */
import '../styles/index.css'
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

/*
   * WAAF SIGMET 51 VALID 012350/020550 WAAA- WAAF UJUNG PANDANG FIR
   * VA ERUPTION MT DUKONO PSN N0142 E12754 VA CLD OBS AT 2230Z
   * WI N0143 E12752 - N0139 E12829 - N0121 E12821 - N 0141 E12751 - N0143 E12752
   * SFC/FL080 MOV SE 15KT NC=
   *  */

const certainAreaPolygon = L.polygon
([[1.72, 127.87],
  [1.65, 127.87],
  [1.35, 128.48],
  [1.68, 128.35]],
{ color: 'red' }).addTo(map)

// Menambahkan event hover pada polygon
certainAreaPolygon.on('mouseover', function (e) {
  this.bindPopup('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi imperdiet vestibulum lacus eu volutpat.').openPopup()
})

const chatButton = document.getElementById('chat-button')
const chatPopup = document.getElementById('chat-popup')
const closeButton = document.getElementById('close-button')

chatButton.addEventListener('click', function () {
  chatPopup.classList.add('active')
})

closeButton.addEventListener('click', function () {
  chatPopup.classList.remove('active')
})

const form = document.getElementById('chat-form')
const resultInput = document.getElementById('result')

form.addEventListener('submit', function (event) {
  event.preventDefault()

  const promptInput = document.getElementById('prompt').value
  const result = processPrompt(promptInput)

  resultInput.value = result
  document.getElementById('prompt').value = ''
})

function processPrompt (prompt) {
  return prompt
}
