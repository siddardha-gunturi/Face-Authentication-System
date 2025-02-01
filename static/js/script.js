let webcam = document.getElementById("webcam");
let captureBtn = document.getElementById("captureBtn");
let recognizeBtn = document.getElementById("recognizeBtn");
let nameInput = document.getElementById("nameInput");
let statusMessage = document.getElementById("statusMessage");

let videoStream;

function startWebcam() {
  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then((stream) => {
      videoStream = stream;
      webcam.srcObject = stream;
    })
    .catch((error) => {
      console.error("Error accessing webcam: ", error);
      statusMessage.textContent = "Error accessing webcam.";
    });
}

function stopWebcam() {
  if (videoStream) {
    let tracks = videoStream.getTracks();
    tracks.forEach((track) => track.stop());
  }
}

function captureImage() {
  let canvas = document.createElement("canvas");
  let ctx = canvas.getContext("2d");
  canvas.width = webcam.videoWidth;
  canvas.height = webcam.videoHeight;
  ctx.drawImage(webcam, 0, 0, canvas.width, canvas.height);
  return canvas.toDataURL("image/jpeg");
}

function registerFace() {
  let name = document.getElementById("name").value;
  if (!name) {
    statusMessage.textContent = "Please enter a name.";
    return;
  }

  let imageData = captureImage();

  $.ajax({
    url: "/.netlify/functions/capture_face",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({ name: name, image: imageData }),
    success: (response) => {
      statusMessage.textContent = response.message;
      nameInput.style.display = "none";
    },
    error: (error) => {
      statusMessage.textContent = error.responseJSON.error;
    },
  });
}

function recogniseFace() {
  let name = document.getElementById("name").value;
  statusMessage.textContent = "Recognising....";
}

function recognizeFace() {
  let imageData = captureImage();

  $.ajax({
    url: "/.netlify/functions/recognize_face",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({ image: imageData }),
    success: (response) => {
      statusMessage.textContent = response.message;
    },
    error: (error) => {
      console.log(error);
      statusMessage.textContent = error.responseJSON.message;
    },
  });
}

captureBtn.addEventListener("click", () => {
  nameInput.style.display = "block";
});

recognizeBtn.addEventListener("click", recognizeFace);

startWebcam();
