// Bubble Animation + Water Wave
const canvas = document.getElementById('bubbleCanvas');
const ctx = canvas.getContext('2d');

let bubbles = [];
let waveOffset = 0;

// Create Bubbles
function createBubbles() {
    for (let i = 0; i < 50; i++) {
        bubbles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            radius: Math.random() * 8 + 2,
            speed: Math.random() * 1 + 0.5,
            dx: (Math.random() - 0.5) * 1,
            dy: (Math.random() - 0.5) * 1,
        });
    }
}

// Draw Water Wave
function drawWave() {
    ctx.beginPath();
    ctx.moveTo(0, canvas.height / 2);

    for (let x = 0; x <= canvas.width; x += 10) {
        let y = canvas.height / 2 + Math.sin((x + waveOffset) * 0.02) * 20;
        ctx.lineTo(x, y);
    }

    ctx.lineTo(canvas.width, canvas.height);
    ctx.lineTo(0, canvas.height);
    ctx.closePath();

    ctx.fillStyle = 'rgba(173, 216, 230, 0.2)'; // Soft light blue wave
    ctx.fill();
}

// Draw Bubbles
function drawBubbles() {
    ctx.fillStyle = 'white';
    bubbles.forEach(bubble => {
        ctx.beginPath();
        ctx.arc(bubble.x, bubble.y, bubble.radius, 0, Math.PI * 2);
        ctx.fill();
    });
}

// Move Bubbles
function moveBubbles() {
    bubbles.forEach(bubble => {
        bubble.x += bubble.dx;
        bubble.y += bubble.dy;

        if (bubble.x < 0 || bubble.x > canvas.width) bubble.dx *= -1;
        if (bubble.y < 0 || bubble.y > canvas.height) bubble.dy *= -1;
    });
}

// Animate
function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawWave();
    drawBubbles();
    moveBubbles();

    waveOffset += 2; // Speed of the wave
    requestAnimationFrame(animate);
}

// Resize Canvas
window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

createBubbles();
animate();

// Sonic Send/Receive Logic
const textInput = document.getElementById('textInput');
const beepSound = document.getElementById('beepSound');
const status = document.getElementById('status');

function sendText() {
    const text = textInput.value.trim();

    if (text === "") {
        alert("Please type some text first!");
        return;
    }

    beepSound.play();
    status.textContent = "Sending text via Ultrasound...";

    setTimeout(() => {
        fetch('/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        })
        .then(res => res.json())
        .then(data => {
            status.textContent = data.msg;
        });
    }, 2000);
}

function receiveData() {
    beepSound.play();
    status.textContent = "Receiving data via Ultrasound...";

    setTimeout(() => {
        fetch('/receive')
        .then(res => res.json())
        .then(data => {
            status.textContent = "Received: " + data.data;
        });
    }, 2500);
}