const msg = document.querySelector(".msg-log");
const boxOptions = document.querySelector(".box-selection");
let count = 0;

function onScanSuccess(decodedText, decodedResult) {
  msg.innerHTML +=
    `${count == 0 ? "Persona: " : "Vehiculo: "}` + decodedText + "<br>";
  console.log("Scan result: ", decodedResult);

  if (count == 1) {
    html5QrcodeScanner.clear();
    boxOptions.style.display = "flex";
  }

  count += 1;
}

var html5QrcodeScanner = new Html5QrcodeScanner("reader", {
  fps: 10,
  qrbox: 250,
});

html5QrcodeScanner.render(onScanSuccess);
