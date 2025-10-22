const boxOptions = document.querySelector('.box-selection')

let msg = document.querySelector('.msg-log')
let count = 0

const data = {
  name: '',
  vehicle: '',
}

const sendScanData = async () => {
  try {
    const response = await fetch('/qr-scan-data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })

    if (response.ok) {
      const result = await response.json()

      msg.innerHTML +=
        '<span style="color: green;">✅ Datos enviados a Odoo.</span><br>'
    } else {
      msg.innerHTML += `<span style="color: red;">❌ Error HTTP: ${response.status}</span><br>`
    }
  } catch (error) {
    msg.innerHTML += `<span style="color: red;">❌ Error de red: ${error.message}</span><br>`
  }
}

function onScanSuccess(decodedText, decodedResult) {
  let currentLabel = count === 0 ? 'Persona: ' : 'Vehículo: '
  msg.innerHTML += currentLabel + decodedText + '<br>'

  count === 0 ? (data.name = decodedText) : (data.vehicle = decodedText)

  count++

  if (count === 2) {
    html5QrcodeScanner.clear()
    boxOptions.style.display = 'flex'

    sendScanData()
  }
}

var html5QrcodeScanner = new Html5QrcodeScanner('reader', {
  fps: 10,
  qrbox: 250,
})

html5QrcodeScanner.render(onScanSuccess)

// Estilos
const divReader = document.querySelector('#reader')
divReader.classList.add('border-0')

const btnPermissionReader = document.querySelector(
  '#html5-qrcode-button-camera-permission'
)
btnPermissionReader.classList.add('py-2', 'px-4', 'btn-primary', 'rounded')
btnPermissionReader.textContent = 'Permiso Camara'

const btnUploadReader = document.querySelector(
  '#html5-qrcode-button-file-selection'
)
btnUploadReader.classList.add('py-2', 'px-4', 'btn-primary', 'rounded')

const iconReader = document.querySelector('#reader > div img')
iconReader.classList.add('d-none')

const spanImgReader = document.querySelector(
  '#html5-qrcode-anchor-scan-type-change'
)

spanImgReader.classList.add('d-none')
