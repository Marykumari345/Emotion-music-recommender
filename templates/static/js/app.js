async function uploadImage() {
  const file = document.getElementById('imageInput').files[0];
  if (!file) return alert("Please upload an image.");

  const formData = new FormData();
  formData.append('image', file);

  const res = await fetch('/analyze', { method: 'POST', body: formData });
  const data = await res.json();

  document.getElementById('result').innerHTML = `<h2>Detected Emotion: ${data.emotion}</h2>`;
  
  let songsHTML = "<h3>Recommended Songs:</h3><ul>";
  data.songs.forEach(song => {
    songsHTML += `<li><a href="${song.url}" target="_blank">${song.title}</a></li>`;
  });
  songsHTML += "</ul>";

  document.getElementById('songs').innerHTML = songsHTML;
}
