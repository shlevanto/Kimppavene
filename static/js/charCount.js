var textId = document.currentScript.getAttribute('textField');
var countId = document.currentScript.getAttribute('charCount');

var myText = document.getElementById('boat_description');
var charCount = document.getElementById(countId)

const max = parseInt(document.currentScript.getAttribute('max'))


myText.addEventListener("keyup", function() {
  var characters = myText.value.split('');
  charCount.innerText = characters.length;
  
  if(characters.length > max) {
    myText.value = myText.value.substring(0, max);
    charCount.innerText = max;
  }
})