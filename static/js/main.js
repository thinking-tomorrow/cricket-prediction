var i = 0;
var txt=[];
var speed = 100;

function type(text, id){
  typeWriter(text, document.getElementById(id));
}

function typeWriter(text, element) {
  if (i < text.length) {
    element.innerHTML += text.charAt(i);
    i++;
    setTimeout(typeWriter, speed, text, element);
  }
}
