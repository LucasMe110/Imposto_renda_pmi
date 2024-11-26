let selectedImageElement = null;

function filterImages(category) {
  alert(`Filtrando imagens da categoria: ${category}`);
}

function goBack() {
  alert("Você clicou em voltar!");
}

function openModal() {
  document.getElementById('uploadModal').style.display = 'flex';
}

function closeModal() {
  document.getElementById('uploadModal').style.display = 'none';
}

function showFileName() {
  const fileInput = document.getElementById('fileInput');
  const fileName = fileInput.files[0] ? fileInput.files[0].name : "Nenhum arquivo escolhido";
  document.getElementById('fileName').textContent = fileName;
}

function uploadFile() {
  const fileInput = document.getElementById('fileInput');
  const file = fileInput.files[0];
  const gallery = document.getElementById('imageGallery');
  const noFilesMessage = document.getElementById('noFilesMessage');

  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      const div = document.createElement('div');
      div.className = 'image-item';
      div.innerHTML = `
        <img src="${e.target.result}" onclick="viewImage(this)">
      `;
      gallery.appendChild(div);
      noFilesMessage.style.display = 'none';
    };
    reader.readAsDataURL(file);
    closeModal();
  } else {
    alert("Por favor, selecione um arquivo.");
  }
}

function viewImage(imageElement) {
  selectedImageElement = imageElement;
  const modal = document.getElementById('imageModal');
  const modalImage = document.getElementById('modalImage');
  modalImage.src = imageElement.src;
  modal.style.display = 'flex';
}

function closeImageModal() {
  document.getElementById('imageModal').style.display = 'none';
}

function deleteCurrentImage() {
  if (selectedImageElement) {
    selectedImageElement.parentElement.remove();
    document.getElementById('imageModal').style.display = 'none';
    const gallery = document.getElementById('imageGallery');
    if (!gallery.children.length) {
      document.getElementById('noFilesMessage').style.display = 'block';
    }
  }
}

function triggerFileInput() {
  document.getElementById('fileInput').click();
}
