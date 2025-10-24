let msg = document.querySelector('.msg-log')
let count = 0
let data = {
  vehicle_id: '',
  port_id: '',
  user_action: '',
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
  let currentLabel = count === 0 ? 'Puerto: ' : 'Vehículo: '
  msg.innerHTML += currentLabel + decodedText + '<br>'

  count === 0 ? (data.port_id = decodedText) : (data.vehicle_id = decodedText)

  count++

  if (count === 2) {
    html5QrcodeScanner.clear()
    let box = document.querySelector('.box-selection')
    box.style.display = 'flex'
  }
}

let html5QrcodeScanner = new Html5QrcodeScanner('reader', {
  fps: 10,
  qrbox: 250,
})

html5QrcodeScanner.render(onScanSuccess)

const btnSubmitData = document.querySelector('.btn-submit-data')
btnSubmitData.addEventListener('click', () => {
  const option = document.querySelector('.form-select')
  data.user_action = option.value
  sendScanData()
})

// Estilos
const divReader = document.querySelector('#reader')
const btnPermissionReader = document.querySelector(
  '#html5-qrcode-button-camera-permission'
)
const btnUploadReader = document.querySelector(
  '#html5-qrcode-button-file-selection'
)
const iconReader = document.querySelector('#reader > div img')
const spanImgReader = document.querySelector(
  '#html5-qrcode-anchor-scan-type-change'
)

divReader.classList.add('border-0')
btnPermissionReader.classList.add('py-2', 'px-4', 'btn-primary', 'rounded')
btnPermissionReader.textContent = 'Permiso Camara'
btnUploadReader.classList.add('py-2', 'px-4', 'btn-primary', 'rounded')
iconReader.classList.add('d-none')
spanImgReader.classList.add('d-none')
