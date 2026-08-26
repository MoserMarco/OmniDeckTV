function sendWake() {
    fetch('/wake', { method: 'POST' })
        .then(r => r.json())

}

function sendKey(key) {
    fetch(`/key/${key}`, { method: 'POST' })
        .then(r => r.json())

}

function mouse(){
    window.location.href = "/mouse";
}
function remote(){
    window.location.href = "/";
}

const joystick = document.getElementById("joystick");
const stick = document.getElementById("stick");

let centerX = joystick.offsetLeft + joystick.offsetWidth / 2;
let centerY = joystick.offsetTop + joystick.offsetHeight / 2;
let active = false;


window.addEventListener("resize", () => {
  centerX = joystick.offsetLeft + joystick.offsetWidth / 2;
  centerY = joystick.offsetTop + joystick.offsetHeight / 2;
});

function sendMove(dx, dy) {
  // Normalizza un po' (perché altrimenti valori troppo grandi)
  let speedX = Math.round(dx / 10);
  let speedY = Math.round(dy / 10);

  // Invia al server
  fetch("/mouse_move", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ dx: speedX, dy: speedY })
  });
}

joystick.addEventListener("touchstart", (e) => {
  active = true;
});

joystick.addEventListener("touchmove", (e) => {
  if (!active) return;

  let touch = e.touches[0];
  let dx = touch.clientX - centerX;
  let dy = touch.clientY - centerY;

  // Limitiamo il raggio massimo
  let maxRadius = joystick.offsetWidth / 2 - stick.offsetWidth / 2;
  let dist = Math.sqrt(dx * dx + dy * dy);

  if (dist > maxRadius) {
    dx = (dx / dist) * maxRadius;
    dy = (dy / dist) * maxRadius;
  }

  stick.style.transform = `translate(${dx}px, ${dy}px) translate(-50%, -50%)`;

  sendMove(dx, dy);
});

joystick.addEventListener("touchend", (e) => {
  active = false;
  stick.style.transform = "translate(-50%, -50%)";

  // Ferma movimento
  sendMove(0, 0);
});
